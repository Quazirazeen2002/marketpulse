import csv
import io
import json
from typing import Dict, Any, List


def export_markdown_report(report_data: Dict[str, Any]) -> str:
    """Export complete research brief as a clean, publication-ready Markdown report."""
    md = []
    objective = report_data.get("objective", "Autonomous Business Intelligence Investigation")
    industry = report_data.get("industry", "General Industry")
    geography = report_data.get("geography", "Global")
    generated_at = report_data.get("generated_at", "")
    run_id = report_data.get("research_id", "")
    quality = report_data.get("research_quality", "moderate")
    exec_status = report_data.get("execution_status", "completed")

    md.append(f"# MARKETPULSE — Executive Intelligence Report")
    md.append(f"**Research Run ID:** `{run_id}` | **Generated:** `{generated_at}`")
    md.append(f"**Industry:** {industry} | **Geography:** {geography} | **Quality Rating:** `{quality.upper()}`\n")
    md.append("---\n")

    # Executive Summary / Body
    exec_content = report_data.get("executive_report", "")
    if exec_content:
        md.append(exec_content)
    else:
        md.append("## Executive Summary\n*No executive synthesis available.*")

    # Commercial Opportunities
    opps = report_data.get("business_opportunities", [])
    if opps:
        md.append("\n## Prioritized Business Opportunities\n")
        for i, opp in enumerate(opps, 1):
            name = opp.get("opportunity_name", f"Opportunity {i}")
            prob = opp.get("problem_identified", "")
            target = opp.get("target_customer", "")
            val = opp.get("potential_commercial_value", "")
            diff = opp.get("implementation_difficulty", "Medium")
            ev_ids = ", ".join(f"`{e}`" for e in opp.get("supporting_evidence_ids", [])) or "None"

            md.append(f"### {i}. {name}")
            md.append(f"- **Problem Identified:** {prob}")
            md.append(f"- **Target Customer:** {target}")
            md.append(f"- **Potential Commercial Value:** {val} *(Qualitative Assessment)*")
            md.append(f"- **Implementation Difficulty:** `{diff}`")
            md.append(f"- **Supporting Evidence IDs:** {ev_ids}")
            risks = opp.get("main_risks", [])
            if risks:
                md.append(f"- **Key Commercial Risks:** {', '.join(risks)}")
            validations = opp.get("validation_required", [])
            if validations:
                md.append(f"- **Validation Required Before Investment:** {', '.join(validations)}")
            md.append("")

    # Strategic Recommendations
    recs = report_data.get("strategic_recommendations", [])
    if recs:
        md.append("\n## Strategic Recommendations\n")
        for i, rec in enumerate(recs, 1):
            title = rec.get("title", f"Recommendation {i}")
            desc = rec.get("description", "")
            cat = rec.get("category", "evidence_backed")
            ev_ids = ", ".join(f"`{e}`" for e in rec.get("supporting_evidence_ids", [])) or "Hypothesis"
            md.append(f"### {i}. {title} `[{cat.upper()}]`")
            md.append(f"{desc}")
            md.append(f"- *Evidence Grounding:* {ev_ids}\n")

    # Research Gaps & Limitations
    gaps = report_data.get("research_gaps", [])
    if gaps:
        md.append("\n## Research Knowledge Gaps\n")
        for gap in gaps:
            md.append(f"- ⚠️ {gap}")

    limitations = report_data.get("limitations", [])
    if limitations:
        md.append("\n## Methodological Limitations\n")
        for lim in limitations:
            md.append(f"- ℹ️ {lim}")

    # Evidence References
    evidence = report_data.get("evidence", [])
    if evidence:
        md.append("\n## Empirical Evidence Registry\n")
        for idx, ev in enumerate(evidence, 1):
            title = ev.get("source_title", "Untitled Source")
            url = ev.get("source_url", "#")
            pub = ev.get("publisher", "Web Domain")
            ev_id = ev.get("evidence_id", "")
            cited = "✅ Cited in Findings" if ev.get("is_cited") else "ℹ️ Background Lead"
            excerpt = ev.get("supporting_excerpt", "")
            md.append(f"{idx}. [{title}]({url}) — `{pub}` (ID: `{ev_id}`) [{cited}]")
            if excerpt:
                md.append(f"   > *\"{excerpt[:250]}\"*")

    return "\n".join(md)


def export_json_report(report_data: Dict[str, Any]) -> str:
    """Export complete research session as structured JSON."""
    return json.dumps(report_data, indent=2, ensure_ascii=False)


def export_evidence_csv(evidence_list: List[Dict[str, Any]]) -> str:
    """Export evidence records as CSV for external data analysis."""
    output = io.StringIO()
    fieldnames = [
        "evidence_id",
        "source_url",
        "source_title",
        "publisher",
        "published_at",
        "is_cited",
        "extraction_quality",
        "supporting_excerpt",
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    for item in evidence_list:
        writer.writerow(item)
    return output.getvalue()


def export_printable_html(report_data: Dict[str, Any]) -> str:
    """Generate standalone printable HTML document with clean styling."""
    md_content = export_markdown_report(report_data)
    # Convert markdown headers and paragraphs to clean HTML
    import html
    escaped = html.escape(md_content).replace("\n\n", "</p><p>").replace("\n", "<br>")

    html_doc = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>MARKETPULSE Report - {html.escape(report_data.get('objective', 'Deep Research'))}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; color: #002B36; max-width: 900px; margin: 40px auto; padding: 0 20px; }}
        h1 {{ color: #002B36; border-bottom: 2px solid #EA3829; padding-bottom: 8px; font-size: 24px; }}
        h2 {{ color: #073642; border-bottom: 1px solid #EADBCC; padding-bottom: 6px; font-size: 18px; margin-top: 30px; }}
        h3 {{ color: #002B36; font-size: 15px; margin-top: 20px; }}
        code {{ background: #FDF6E3; color: #CB4B16; padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }}
        blockquote {{ border-left: 4px solid #EA3829; background: #FAF9F6; margin: 12px 0; padding: 10px 16px; color: #586E75; }}
        .header {{ border-top: 5px solid #EA3829; background: #FFFFFF; border: 1px solid #EADBCC; border-radius: 8px; padding: 20px; margin-bottom: 30px; }}
        @media print {{ body {{ margin: 20px; max-width: 100%; }} }}
    </style>
</head>
<body>
    <div class="header">
        <h1>MARKET<span style="color: #EA3829;">PULSE</span></h1>
        <p><strong>Autonomous Deep Research & Business Intelligence Report</strong></p>
    </div>
    <div class="content">
        <p>{escaped}</p>
    </div>
</body>
</html>"""
    return html_doc
