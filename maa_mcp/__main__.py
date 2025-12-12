"""
MCP Server entry point for module execution.

This file allows the MCP server to be run as a Python module:
    python -m maa_mcp

It imports and runs the main MCP server from main.py.
"""
from .main import mcp


def main():
    """Entry point for the maa-mcp command."""
    mcp.run()


if __name__ == "__main__":
    main()
