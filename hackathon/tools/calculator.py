"""
Hackathon Tool: Calculator
Basic math operations as a Bedrock-compatible tool.
"""

import json

TOOL_SCHEMA = {
    "toolSpec": {
        "name": "calculator",
        "description": "Perform basic math operations: add, subtract, multiply, divide.",
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"],
                        "description": "The math operation to perform"
                    },
                    "a": {"type": "number", "description": "First operand"},
                    "b": {"type": "number", "description": "Second operand"}
                },
                "required": ["operation", "a", "b"]
            }
        }
    }
}


def calculator(operation, a, b):
    """Perform a basic math operation."""
    ops = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else "Error: division by zero",
    }
    if operation not in ops:
        return json.dumps({"error": f"Unknown operation: {operation}"})
    result = ops[operation](a, b)
    return json.dumps({"operation": operation, "a": a, "b": b, "result": result})
