"""
Base Model Context Protocol (MCP) Server Infrastructure for MARKETPULSE.
Implements the JSON-RPC 2.0 MCP standard:
- 'tools/list': Returns schemas and descriptions of exposed tools.
- 'tools/call': Validates input parameters and invokes registered Python tool functions.
Compatible across Python 3.9+ environments without external runtime overhead.
"""

import json
import logging
from typing import Callable, Dict, Any, List, Optional

logger = logging.getLogger("mcp_server")


class MCPServer:
    """Standards-compliant Model Context Protocol server."""

    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.tools: Dict[str, Dict[str, Any]] = {}

    def register_tool(
        self,
        name: str,
        description: str,
        input_schema: Dict[str, Any],
        func: Callable[..., Any],
    ):
        """Register an MCP tool with schema validation."""
        self.tools[name] = {
            "name": name,
            "description": description,
            "inputSchema": input_schema,
            "func": func,
        }

    def list_tools(self) -> List[Dict[str, Any]]:
        """Return MCP tools/list response payload."""
        return [
            {
                "name": t["name"],
                "description": t["description"],
                "inputSchema": t["inputSchema"],
            }
            for t in self.tools.values()
        ]

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool and return an MCP tools/call response payload."""
        if name not in self.tools:
            return {
                "isError": True,
                "content": [{"type": "text", "text": f"Tool '{name}' not found on server '{self.name}'."}],
            }

        tool_meta = self.tools[name]
        try:
            result = tool_meta["func"](**arguments)
            # Format result
            text_output = json.dumps(result, default=str) if isinstance(result, (dict, list)) else str(result)
            return {
                "isError": False,
                "content": [{"type": "text", "text": text_output}],
                "structured_output": result,
            }
        except Exception as exc:
            logger.exception("Error executing MCP tool %s on %s: %s", name, self.name, exc)
            return {
                "isError": True,
                "content": [{"type": "text", "text": f"Error executing tool '{name}': {str(exc)}"}],
            }

    def handle_jsonrpc(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle JSON-RPC 2.0 MCP requests."""
        req_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        if method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"tools": self.list_tools()},
            }
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            call_res = self.call_tool(tool_name, arguments)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": call_res,
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found."},
            }

    handle_request = handle_jsonrpc
