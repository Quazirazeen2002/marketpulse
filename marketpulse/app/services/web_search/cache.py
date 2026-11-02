"""
Web search caching and query deduplication service for MARKETPULSE.
Provides L1 (in-memory) and L2 (SQLite-backed) caching with configurable TTL.
Prevents duplicate API calls within and across research runs, saving credits.
"""

import json
import time
import hashlib
import logging
import threading
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional, Set

from app.config import settings

logger = logging.getLogger(__name__)


def normalize_query_string(query: str) -> str:
    """Normalize query text for deterministic hashing."""
    return " ".join(query.strip().lower().split())


def generate_cache_key(
    query: str,
    search_depth: str = "basic",
    topic: str = "general",
    include_domains: Optional[List[str]] = None,
    exclude_domains: Optional[List[str]] = None,
    max_results: int = 8,
) -> str:
    """Generate SHA-256 hash key covering all search parameter dimensions."""
    norm_query = normalize_query_string(query)
    inc_str = ",".join(sorted(include_domains or []))
    exc_str = ",".join(sorted(exclude_domains or []))
    raw_key = f"{norm_query}|{search_depth}|{topic}|{inc_str}|{exc_str}|{max_results}"
    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()


class SearchCache:
    """
    Thread-safe dual-tier cache with TTL expiration.
    Also tracks query deduplication within individual research runs.
    """

    def __init__(self, ttl_hours: int = 24, enabled: bool = True):
        self.ttl_hours = ttl_hours
        self.enabled = enabled
        self._lock = threading.Lock()

        # In-memory L1 cache: cache_key -> (timestamp, results)
        self._memory_cache: Dict[str, Dict[str, Any]] = {}

        # Per-run query deduplication: research_id -> Set of normalized queries
        self._run_queries: Dict[str, Set[str]] = {}

        # Telemetry metrics
        self.hits: int = 0
        self.misses: int = 0

    def is_query_executed_in_run(self, research_id: str, query: str) -> bool:
        """Check if identical query was already run within this research session."""
        if not research_id:
            return False
        norm = normalize_query_string(query)
        with self._lock:
            return norm in self._run_queries.get(research_id, set())

    def record_run_query(self, research_id: str, query: str):
        """Mark query as executed for this research run."""
        if not research_id:
            return
        norm = normalize_query_string(query)
        with self._lock:
            if research_id not in self._run_queries:
                self._run_queries[research_id] = set()
            self._run_queries[research_id].add(norm)

    def get(self, cache_key: str) -> Optional[List[Dict[str, Any]]]:
        """Retrieve results from L1 or L2 cache if not expired."""
        if not self.enabled:
            return None

        now = time.time()

        # 1. Check L1 in-memory cache
        with self._lock:
            entry = self._memory_cache.get(cache_key)
            if entry:
                if entry["expires_at"] > now:
                    self.hits += 1
                    logger.debug("Search cache L1 HIT for key=%s", cache_key[:12])
                    return [dict(r) for r in entry["results"]]
                else:
                    # Expired
                    del self._memory_cache[cache_key]

        # 2. Check L2 SQLite cache
        try:
            from app.database.db import get_db_session
            from app.database.models import SearchCacheRecord
            from sqlmodel import select

            with get_db_session() as session:
                stmt = select(SearchCacheRecord).where(SearchCacheRecord.cache_key == cache_key)
                record = session.exec(stmt).first()
                if record:
                    exp_timestamp = record.expires_at.replace(tzinfo=timezone.utc).timestamp()
                    if exp_timestamp > now:
                        with self._lock:
                            self.hits += 1
                            # Populate L1
                            self._memory_cache[cache_key] = {
                                "expires_at": exp_timestamp,
                                "results": record.results,
                            }
                        logger.debug("Search cache L2 (SQLite) HIT for key=%s", cache_key[:12])
                        return [dict(r) for r in record.results]
                    else:
                        # Clean up expired row
                        session.delete(record)
                        session.commit()
        except Exception as exc:
            logger.debug("L2 cache read failed (fallback to miss): %s", exc)

        with self._lock:
            self.misses += 1
        return None

    def set(
        self,
        cache_key: str,
        query: str,
        results: List[Dict[str, Any]],
        search_depth: str = "basic",
        topic: str = "general",
    ):
        """Store search results in L1 and L2 caches."""
        if not self.enabled or not results:
            return

        expires_at = time.time() + (self.ttl_hours * 3600)
        dt_expires = datetime.now(timezone.utc) + timedelta(hours=self.ttl_hours)

        # Store in L1
        with self._lock:
            self._memory_cache[cache_key] = {
                "expires_at": expires_at,
                "results": [dict(r) for r in results],
            }

        # Store in L2 SQLite
        try:
            from app.database.db import get_db_session
            from app.database.models import SearchCacheRecord
            from sqlmodel import select

            with get_db_session() as session:
                existing = session.exec(
                    select(SearchCacheRecord).where(SearchCacheRecord.cache_key == cache_key)
                ).first()
                if existing:
                    existing.results = results
                    existing.result_count = len(results)
                    existing.expires_at = dt_expires
                    session.add(existing)
                else:
                    new_rec = SearchCacheRecord(
                        cache_key=cache_key,
                        query=query,
                        search_depth=search_depth,
                        topic=topic,
                        results=results,
                        result_count=len(results),
                        search_provider="tavily",
                        expires_at=dt_expires,
                    )
                    session.add(new_rec)
                session.commit()
        except Exception as exc:
            logger.debug("L2 cache write failed (retained in L1): %s", exc)

    def clear(self):
        """Clear memory cache and resets hit counters."""
        with self._lock:
            self._memory_cache.clear()
            self._run_queries.clear()
            self.hits = 0
            self.misses = 0

    def stats(self) -> Dict[str, Any]:
        """Return cache health metrics."""
        with self._lock:
            total = self.hits + self.misses
            rate = round((self.hits / total * 100), 1) if total > 0 else 0.0
            return {
                "enabled": self.enabled,
                "ttl_hours": self.ttl_hours,
                "hits": self.hits,
                "misses": self.misses,
                "hit_rate_pct": rate,
                "l1_entries": len(self._memory_cache),
            }


# Singleton cache instance configured from settings
search_cache = SearchCache(
    ttl_hours=settings.SEARCH_CACHE_TTL_HOURS,
    enabled=settings.SEARCH_CACHE_ENABLED,
)
