import pytest
from app.services.source_acquisition.html_extractor import extract_html_content


SAMPLE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Bangladesh Fashion E-commerce Market Trends 2026</title>
    <meta name="author" content="Business Analyst">
    <meta name="date" content="2026-03-15">
    <meta property="og:site_name" content="Retail Daily">
</head>
<body>
    <header><nav><a href="/">Home</a><a href="/news">News</a></nav></header>
    <main>
        <article>
            <h1>Bangladesh Fashion E-commerce Surges</h1>
            <p>The fashion e-commerce sector in Bangladesh is expanding rapidly driven by younger demographics in urban hubs like Dhaka and Chittagong. Leading platforms have introduced same-day delivery services and streamlined cash-on-delivery options.</p>
            <p>Major competitive players such as Daraz and local fashion labels like Aarong and Fabrilife are diversifying seasonal campaign offerings.</p>
        </article>
    </main>
    <footer><p>&copy; 2026 Retail Daily. All rights reserved.</p></footer>
</body>
</html>
"""


def test_html_extraction_main_content():
    text, meta, status = extract_html_content(SAMPLE_HTML, base_url="https://retaildaily.com/fashion-trends")
    assert status == "retrieved_full_text"
    assert "Bangladesh Fashion E-commerce" in text
    assert "Daraz" in text
    # Navigation and footer should be stripped
    assert "Home" not in text
    assert "All rights reserved" not in text


def test_html_extraction_metadata():
    _, meta, _ = extract_html_content(SAMPLE_HTML, base_url="https://retaildaily.com/fashion-trends")
    assert "Fashion E-commerce" in meta.get("title", "")
    assert meta.get("sitename") == "Retail Daily" or "Retail Daily" in str(meta)
