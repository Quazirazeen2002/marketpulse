"""
MCP Servers Package for MARKETPULSE Stage 2.
"""

from app.mcp_servers.base import MCPServer
from app.mcp_servers.academic_intelligence_server import academic_server
from app.mcp_servers.document_intelligence_server import document_server
from app.mcp_servers.customer_intelligence_server import customer_mcp_server
from app.mcp_servers.business_analytics_server import analytics_server

customer_server = customer_mcp_server

__all__ = [
    "MCPServer",
    "academic_server",
    "document_server",
    "customer_mcp_server",
    "customer_server",
    "analytics_server",
]
