"""
Hackathon Tool: Safe Code Executor
Executes Python code in a restricted environment.
"""

import json
import io
import contextlib

TOOL_SCHEMA = {
    "toolSpec": {
        "name": "execute_python",
        "description": "Execute Python code and return the output. Only basic operations are allowed.",
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Python code to execute"}
                },
                "required": ["code"]
            }
        }
    }
}

# Allowed built-in names for the sandbox
SAFE_BUILTINS = {
    "abs", "all", "any", "bool", "dict", "enumerate", "filter", "float",
    "int", "isinstance", "len", "list", "map", "max", "min", "print",
    "range", "reversed", "round", "set", "sorted", "str", "sum", "tuple",
    "type", "zip",
}


def execute_python(code):
    """Execute Python code in a restricted sandbox."""
    safe_globals = {"__builtins__": {k: __builtins__[k] if isinstance(__builtins__, dict)
                                     else getattr(__builtins__, k)
                                     for k in SAFE_BUILTINS
                                     if hasattr(__builtins__, k) or
                                     (isinstance(__builtins__, dict) and k in __builtins__)}}

    stdout_capture = io.StringIO()
    try:
        with contextlib.redirect_stdout(stdout_capture):
            exec(code, safe_globals)
        output = stdout_capture.getvalue()
        return json.dumps({"status": "success", "output": output or "(no output)"})
    except Exception as e:
        return json.dumps({"status": "error", "error": f"{type(e).__name__}: {e}"})
