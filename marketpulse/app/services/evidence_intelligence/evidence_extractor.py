import hashlib
import re
from typing import List, Optional
from app.schemas import SourceDocument, EvidenceRecord, SourceAcquisitionStatus


def extract_evidence_from_source(
    source: SourceDocument,
    research_question_id: Optional[str] = None,
    search_query: str = "",
    max_excerpts: int = 4,
) -> List[EvidenceRecord]:
    """
    Extract atomic factual evidence records from a SourceDocument.
    Extracts exact excerpts with section headings and page references.
    Marks snippet-only sources clearly.
    """
    evidence_records: List[EvidenceRecord] = []
    text = source.extracted_text or ""
    is_snippet = source.extraction_status == SourceAcquisitionStatus.SNIPPET_ONLY

    if not text.strip():
        return []

    # 1. Handle Snippet-only source
    if is_snippet or len(text) < 250:
        ev_id = hashlib.sha256(f"{source.source_id}_snip_{text[:40]}".encode()).hexdigest()[:16]
        evidence_records.append(
            EvidenceRecord(
                evidence_id=ev_id,
                source_id=source.source_id,
                research_question_id=research_question_id,
                source_url=source.url,
                source_title=source.title,
                publisher=source.publisher,
                published_at=source.publication_date,
                exact_excerpt=text[:400].strip(),
                normalized_statement=f"Search snippet from {source.publisher}: {text[:200].strip()}...",
                page_number=None,
                section_heading="Search Engine Snippet",
                evidence_type="snippet_lead",
                search_provider=getattr(source, "search_provider", "tavily") or "tavily",
                extraction_status=source.extraction_status.value if hasattr(source.extraction_status, "value") else str(source.extraction_status),
                extraction_quality="snippet_derived",
                confidence_score=0.60,
                is_cited=False,
                search_query=search_query,
                duplicate_group_id=source.duplicate_group_id,
            )
        )
        return evidence_records

    # 2. Handle PDF Document (look for Page Markers)
    if source.content_type == "application/pdf":
        page_chunks = re.split(r"--- \[Page (\d+)\] ---", text)
        if len(page_chunks) > 1:
            for i in range(1, len(page_chunks), 2):
                if len(evidence_records) >= max_excerpts:
                    break
                p_num = int(page_chunks[i])
                p_text = page_chunks[i + 1].strip()
                # Find informative paragraph
                paragraphs = [p.strip() for p in p_text.split("\n\n") if len(p.strip()) > 80]
                for p in paragraphs[:2]:
                    if len(evidence_records) >= max_excerpts:
                        break
                    ev_id = hashlib.sha256(f"{source.source_id}_p{p_num}_{p[:30]}".encode()).hexdigest()[:16]
                    evidence_records.append(
                        EvidenceRecord(
                            evidence_id=ev_id,
                            source_id=source.source_id,
                            research_question_id=research_question_id,
                            source_url=source.url,
                            source_title=source.title,
                            publisher=source.publisher,
                            published_at=source.publication_date,
                            exact_excerpt=p[:500].strip(),
                            normalized_statement=p[:220].strip(),
                            page_number=p_num,
                            section_heading=f"Page {p_num}",
                            evidence_type="document_text",
                            search_provider=getattr(source, "search_provider", "tavily") or "tavily",
                            extraction_status=source.extraction_status.value if hasattr(source.extraction_status, "value") else str(source.extraction_status),
                            extraction_quality="high",
                            confidence_score=0.90,
                            is_cited=False,
                            search_query=search_query,
                            duplicate_group_id=source.duplicate_group_id,
                        )
                    )
            if evidence_records:
                return evidence_records

    # 3. Handle HTML Full-Text Articles
    # Split by section / paragraphs
    paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 70]

    # Prioritize paragraphs with numerical metrics or market terms
    scored_paragraphs = []
    for idx, p in enumerate(paragraphs):
        weight = 0
        if re.search(r"\b\d+(?:\.\d+)?%|\b(?:BDT|USD|Tk|\$)\b|\b\d{4}\b", p):
            weight += 3
        if any(term in p.lower() for term in ["market", "competitor", "growth", "customer", "sale", "share", "trend"]):
            weight += 2
        scored_paragraphs.append((weight, idx, p))

    scored_paragraphs.sort(key=lambda x: (x[0], -x[1]), reverse=True)

    for _, p_idx, p in scored_paragraphs[:max_excerpts]:
        ev_id = hashlib.sha256(f"{source.source_id}_p{p_idx}_{p[:30]}".encode()).hexdigest()[:16]
        evidence_records.append(
            EvidenceRecord(
                evidence_id=ev_id,
                source_id=source.source_id,
                research_question_id=research_question_id,
                source_url=source.url,
                source_title=source.title,
                publisher=source.publisher,
                published_at=source.publication_date,
                exact_excerpt=p[:500].strip(),
                normalized_statement=p[:200].strip(),
                page_number=None,
                section_heading=f"Section {p_idx + 1}",
                evidence_type="article_text",
                search_provider=getattr(source, "search_provider", "tavily") or "tavily",
                extraction_status=source.extraction_status.value if hasattr(source.extraction_status, "value") else str(source.extraction_status),
                extraction_quality="high",
                confidence_score=0.85,
                is_cited=False,
                search_query=search_query,
                duplicate_group_id=source.duplicate_group_id,
            )
        )

    return evidence_records


class EvidenceExtractor:
    """Class wrapper for extracting atomic evidence records from sources."""

    def __init__(self, max_excerpts: int = 4):
        self.max_excerpts = max_excerpts

    def extract_from_source(
        self,
        source: SourceDocument,
        research_questions: Optional[List[str]] = None,
        search_query: str = "",
        max_evidence_per_source: Optional[int] = None,
    ) -> List[EvidenceRecord]:
        limit = max_evidence_per_source or self.max_excerpts
        return extract_evidence_from_source(
            source=source,
            research_question_id=research_questions[0] if research_questions else None,
            search_query=search_query,
            max_excerpts=limit,
        )
