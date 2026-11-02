import hashlib
from typing import List, Dict, Tuple, Any, Optional
from rapidfuzz import fuzz
from app.schemas import SourceDocument, EvidenceGroup


def cluster_and_deduplicate_sources(
    sources: List[SourceDocument],
    near_dup_threshold: float = 88.0,
) -> Tuple[List[SourceDocument], List[EvidenceGroup]]:
    """
    Cluster duplicate sources using exact URLs, content hashes, and RapidFuzz near-duplicate matching.
    Preserves all source records while tagging duplicates with a canonical group_id.
    """
    if not sources:
        return [], []

    groups: Dict[str, EvidenceGroup] = {}
    content_map: Dict[str, str] = {}  # group_id -> sample content for near-duplicate check

    for src in sources:
        # 1. Exact URL / Canonical URL match
        norm_url = (src.canonical_url or src.url).strip().lower()
        url_hash = hashlib.sha256(norm_url.encode("utf-8")).hexdigest()[:12]

        matched_group_id = None
        match_method = "exact_url"
        match_score = 100.0

        # Check existing groups for exact hash or near-duplicate content
        for gid, grp in groups.items():
            if grp.canonical_url.strip().lower() == norm_url:
                matched_group_id = gid
                match_method = "canonical_url"
                break
            # Check content hash if available
            existing_text = content_map.get(gid, "")
            if src.content_hash and grp.canonical_source_id:
                # Find canonical source
                can_src = next((s for s in sources if s.source_id == grp.canonical_source_id), None)
                if can_src and can_src.content_hash and can_src.content_hash == src.content_hash:
                    matched_group_id = gid
                    match_method = "content_hash"
                    break

            # Near-duplicate fuzzy matching on first 1500 chars of extracted text
            if existing_text and src.extracted_text and len(src.extracted_text) > 100 and len(existing_text) > 100:
                similarity = fuzz.token_set_ratio(src.extracted_text[:1500], existing_text[:1500])
                if similarity >= near_dup_threshold:
                    matched_group_id = gid
                    match_method = "near_duplicate_fuzzy"
                    match_score = float(similarity)
                    break

        if matched_group_id:
            # Add as duplicate under existing group
            src.duplicate_group_id = matched_group_id
            src.is_canonical = False
            groups[matched_group_id].duplicate_source_ids.append(src.source_id)
        else:
            # Create new canonical group
            gid = f"grp_{url_hash}"
            src.duplicate_group_id = gid
            src.is_canonical = True
            groups[gid] = EvidenceGroup(
                group_id=gid,
                canonical_source_id=src.source_id,
                canonical_url=src.url,
                duplicate_source_ids=[],
                similarity_score=match_score,
                detection_method=match_method,
            )
            content_map[gid] = src.extracted_text[:1500]

    return sources, list(groups.values())


def cluster_sources_and_evidence(
    sources: List[Any],
    evidence: Optional[List[Any]] = None,
    near_dup_threshold: float = 88.0,
) -> List[EvidenceGroup]:
    """
    Cluster sources and tag evidence records with canonical duplicate group IDs.
    """
    src_objects = []
    for s in sources:
        if isinstance(s, SourceDocument):
            src_objects.append(s)
        elif isinstance(s, dict):
            src_objects.append(SourceDocument(**s))

    clustered_srcs, groups = cluster_and_deduplicate_sources(
        src_objects,
        near_dup_threshold=near_dup_threshold,
    )

    # Tag evidence if provided
    if evidence:
        src_group_map = {s.source_id: s.duplicate_group_id for s in clustered_srcs}
        for ev in evidence:
            s_id = getattr(ev, "source_id", "") or (ev.get("source_id") if isinstance(ev, dict) else "")
            gid = src_group_map.get(s_id)
            if gid:
                if isinstance(ev, dict):
                    ev["duplicate_group_id"] = gid
                elif hasattr(ev, "duplicate_group_id"):
                    ev.duplicate_group_id = gid

    return groups


class DeduplicationEngine:
    """Class wrapper for deduplication and clustering operations."""

    def __init__(self, near_dup_threshold: float = 88.0):
        self.near_dup_threshold = near_dup_threshold

    def cluster(self, sources: List[SourceDocument]) -> Tuple[List[SourceDocument], List[EvidenceGroup]]:
        return cluster_and_deduplicate_sources(sources, near_dup_threshold=self.near_dup_threshold)

    def cluster_all(self, sources: List[Any], evidence: Optional[List[Any]] = None) -> List[EvidenceGroup]:
        return cluster_sources_and_evidence(sources, evidence, near_dup_threshold=self.near_dup_threshold)
