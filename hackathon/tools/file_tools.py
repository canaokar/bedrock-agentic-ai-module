"""
Hackathon Tool: File Operations
Read, write, and search files for agents.
"""

import json
import glob as glob_module

READ_TOOL_SCHEMA = {
    "toolSpec": {
        "name": "read_file",
        "description": "Read the contents of a file.",
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file to read"}
                },
                "required": ["path"]
            }
        }
    }
}

WRITE_TOOL_SCHEMA = {
    "toolSpec": {
        "name": "write_file",
        "description": "Write content to a file.",
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to write to"},
                    "content": {"type": "string", "description": "Content to write"}
                },
                "required": ["path", "content"]
            }
        }
    }
}

SEARCH_TOOL_SCHEMA = {
    "toolSpec": {
        "name": "search_files",
        "description": "Search for files matching a pattern in a directory.",
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Glob pattern (e.g., '*.py', '**/*.json')"},
                    "directory": {"type": "string", "description": "Directory to search in (default: current)"}
                },
                "required": ["pattern"]
            }
        }
    }
}

ALL_TOOLS = [READ_TOOL_SCHEMA, WRITE_TOOL_SCHEMA, SEARCH_TOOL_SCHEMA]


def read_file(path):
    """Read a file and return its contents."""
    try:
        with open(path, "r") as f:
            content = f.read()
        return json.dumps({"path": path, "content": content[:5000]})
    except Exception as e:
        return json.dumps({"error": str(e)})


def write_file(path, content):
    """Write content to a file."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
        with open(path, "w") as f:
            f.write(content)
        return json.dumps({"status": "success", "path": path, "bytes_written": len(content)})
    except Exception as e:
        return json.dumps({"error": str(e)})


def search_files(pattern, directory="."):
    """Search for files matching a glob pattern."""
    try:
        full_pattern = os.path.join(directory, pattern)
        matches = glob_module.glob(full_pattern, recursive=True)
        return json.dumps({"pattern": pattern, "matches": matches[:50], "count": len(matches)})
    except Exception as e:
        return json.dumps({"error": str(e)})


TOOL_DISPATCH = {
    "read_file": read_file,
    "write_file": write_file,
    "search_files": search_files,
}
