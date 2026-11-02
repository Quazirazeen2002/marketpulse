"""
Integration test for MCP Servers Architecture.
Verifies JSON-RPC 2.0 tools/list and tools/call protocol compliance across:
1. Academic Intelligence Server
2. Document Intelligence Server
3. Customer Intelligence Server
4. Business Analytics Server
"""

import pytest
from app.mcp_servers import (
    academic_server,
    document_server,
    customer_server,
    analytics_server,
)


def test_mcp_tools_list_protocol():
    """Verify all 4 servers implement tools/list and provide valid schemas."""
    servers = [academic_server, document_server, customer_server, analytics_server]

    for s in servers:
        response = s.handle_request({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        })
        assert response["jsonrpc"] == "2.0"
        assert "result" in response
        tools = response["result"]["tools"]
        assert len(tools) >= 3
        for t in tools:
            assert "name" in t
            assert "description" in t
            assert "inputSchema" in t


def test_business_analytics_mcp_tool_execution():
    """Verify Business Analytics MCP executes deterministic calculations."""
    req = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "calculate_unit_economics",
            "arguments": {
                "selling_price": 100.0,
                "cogs": 40.0,
                "delivery_cost": 5.0,
                "payment_fee": 2.5,
                "other_variable": 2.5,
            }
        }
    }
    response = analytics_server.handle_request(req)
    assert response["jsonrpc"] == "2.0"
    assert "result" in response
    res = response["result"].get("structured_output", response["result"])
    assert res["gross_profit"] == 60.0
    assert res["gross_margin_percent"] == 60.0
    assert res["contribution_margin"] == 50.0  # 100 - (40+5+2.5+2.5) = 50.0


def test_customer_intelligence_mcp_tool_execution():
    """Verify Customer Intelligence MCP extracts recurring complaints."""
    req = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "extract_customer_complaints",
            "arguments": {
                "reviews": [
                    "Dress size was way too small compared to chart. Delivery took 10 days.",
                    "Sizing is inaccurate, returned it immediately. Quality is okay.",
                    "Late delivery and impossible customer service."
                ]
            }
        }
    }
    response = customer_server.handle_request(req)
    assert response["jsonrpc"] == "2.0"
    res = response["result"].get("structured_output", response["result"])
    assert "pain_points" in res
    assert res["analyzed_reviews"] == 3


def test_document_intelligence_mcp_tool_execution():
    """Verify Document Intelligence MCP extracts content metadata."""
    req = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "inspect_document_metadata",
            "arguments": {
                "url": "https://example.com/annual-report.pdf"
            }
        }
    }
    response = document_server.handle_request(req)
    assert response["jsonrpc"] == "2.0"
    res = response["result"].get("structured_output", response["result"])
    assert "file_type" in res
    assert res["file_type"] == "pdf"
