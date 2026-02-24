"""
Agent execution trace logging utilities.
Provides pretty-printing of tool calls, LLM interactions, and timing.
"""

import time
import json


def log_tool_call(tool_name, tool_input, tool_output, duration_ms=None):
    """Print a formatted tool call log entry.

    Args:
        tool_name: Name of the tool that was called.
        tool_input: Dict of input parameters.
        tool_output: The tool's return value (string or dict).
        duration_ms: Optional execution time in milliseconds.
    """
    duration_str = f" ({duration_ms:.0f}ms)" if duration_ms else ""
    print(f"  [TOOL] {tool_name}{duration_str}")
    print(f"    Input:  {json.dumps(tool_input, indent=2)[:200]}")
    output_str = json.dumps(tool_output) if isinstance(tool_output, dict) else str(tool_output)
    print(f"    Output: {output_str[:200]}")


def log_llm_call(model_id, input_tokens=None, output_tokens=None, latency_ms=None):
    """Print a formatted LLM call log entry.

    Args:
        model_id: The Bedrock model identifier.
        input_tokens: Number of input tokens (if available).
        output_tokens: Number of output tokens (if available).
        latency_ms: Response latency in milliseconds.
    """
    parts = [f"[LLM] {model_id}"]
    if input_tokens is not None:
        parts.append(f"in={input_tokens}")
    if output_tokens is not None:
        parts.append(f"out={output_tokens}")
    if latency_ms is not None:
        parts.append(f"{latency_ms:.0f}ms")
    print(f"  {' | '.join(parts)}")


def print_agent_trace(steps):
    """Pretty-print a full agent execution trace.

    Args:
        steps: List of dicts, each with keys like:
            - type: "llm" or "tool"
            - model_id / tool_name
            - input / output
            - duration_ms
    """
    print("\n" + "=" * 60)
    print("AGENT EXECUTION TRACE")
    print("=" * 60)

    for i, step in enumerate(steps, 1):
        step_type = step.get("type", "unknown")
        print(f"\nStep {i} [{step_type.upper()}]")
        print("-" * 40)

        if step_type == "llm":
            log_llm_call(
                step.get("model_id", "unknown"),
                step.get("input_tokens"),
                step.get("output_tokens"),
                step.get("duration_ms"),
            )
            if "text" in step:
                preview = step["text"][:300]
                print(f"    Response: {preview}")

        elif step_type == "tool":
            log_tool_call(
                step.get("tool_name", "unknown"),
                step.get("input", {}),
                step.get("output", ""),
                step.get("duration_ms"),
            )

    print("\n" + "=" * 60)
    total_ms = sum(s.get("duration_ms", 0) for s in steps if s.get("duration_ms"))
    print(f"Total steps: {len(steps)} | Total time: {total_ms:.0f}ms")
    print("=" * 60)
