"""
Hackathon MCP Server: File System
Exposes file system operations as MCP tools.
"""

from mcp.server.fastmcp import FastMCP
import json
import glob as glob_module

mcp = FastMCP("file-server")


@mcp.tool()
def read_file(path: str) -> str:
    """Read the contents of a file.

    Args:
        path: Path to the file to read.
    """
    try:
        with open(path, "r") as f:
            content = f.read(10000)
        return json.dumps({"path": path, "content": content})
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def write_file(path: str, content: str) -> str:
    """Write content to a file.

    Args:
        path: Path to write to.
        content: Content to write.
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
        with open(path, "w") as f:
            f.write(content)
        return json.dumps({"status": "success", "path": path})
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def list_directory(path: str = ".") -> str:
    """List files and directories at the given path.

    Args:
        path: Directory path to list (default: current directory).
    """
    try:
        entries = os.listdir(path)
        items = []
        for entry in sorted(entries):
            full = os.path.join(path, entry)
            items.append({"name": entry, "type": "dir" if os.path.isdir(full) else "file"})
        return json.dumps({"path": path, "items": items[:100]})
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def search_files(pattern: str, directory: str = ".") -> str:
    """Search for files matching a glob pattern.

    Args:
        pattern: Glob pattern (e.g., '*.py', '**/*.json').
        directory: Directory to search in.
    """
    try:
        matches = glob_module.glob(os.path.join(directory, pattern), recursive=True)
        return json.dumps({"pattern": pattern, "matches": matches[:50]})
    except Exception as e:
        return json.dumps({"error": str(e)})


if __name__ == "__main__":
    mcp.run(transport="stdio")
