import re
from typing import List, Tuple


def evaluate_relevance(
    content: str,
    objective: str,
    industry: str = "",
    geography: str = "",
    research_questions: List[str] = None,
) -> Tuple[float, str]:
    """
    Evaluate content relevance on a 0-100 scale by measuring topical alignment,
    industry keyword presence, and geographic specificity.
    """
    if not content or len(content.strip()) < 20:
        return 15.0, "Extracted content is too short to establish strong relevance."

    lower_content = content.lower()
    score = 40.0
    matches = []

    # 1. Geographic Alignment
    if geography and geography.lower() in lower_content:
        score += 20.0
        matches.append(f"mentions target geography '{geography}'")
    else:
        score -= 5.0

    # 2. Industry Alignment
    if industry:
        ind_words = [w for w in re.split(r"[\s/&,-]+", industry.lower()) if len(w) > 3]
        matched_ind = [w for w in ind_words if w in lower_content]
        if matched_ind:
            score += 20.0
            matches.append(f"contains industry keywords: {', '.join(matched_ind)}")

    # 3. Objective & Topic Keywords
    obj_words = set(re.findall(r"\b[a-z]{4,}\b", objective.lower()))
    stop_words = {"this", "that", "with", "from", "your", "what", "which", "analyze", "identify", "investigate"}
    substantive_words = [w for w in obj_words if w not in stop_words]

    matched_obj_count = sum(1 for w in substantive_words if w in lower_content)
    if substantive_words:
        coverage = matched_obj_count / len(substantive_words)
        obj_bonus = min(20.0, coverage * 25.0)
        score += obj_bonus
        if obj_bonus > 10:
            matches.append(f"high research objective keyword alignment ({int(coverage*100)}%)")

    final_score = max(0.0, min(100.0, score))
    rationale = f"Relevance score {final_score:.1f}: " + ("; ".join(matches) if matches else "general topical alignment.")
    return final_score, rationale
