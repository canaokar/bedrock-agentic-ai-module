"""
Lab 06: Multi-Agent System
Build a 3-agent supervisor pattern with delegation and orchestration.
"""

import os
from pathlib import Path
import json
import time
from agents import Agent

# Load .env file if it exists (so you don't have to export every time)
for _candidate in [
    Path(".env"),
    Path(__file__).resolve().parent / ".env",
    Path(__file__).resolve().parent.parent / ".env",
    Path(__file__).resolve().parent.parent.parent / "shared" / ".env",
]:
    if _candidate.exists():
        with open(_candidate) as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _key, _val = _line.split("=", 1)
                    os.environ.setdefault(_key.strip(), _val.strip())
        break

CLAUDE_SONNET = "global.anthropic.claude-sonnet-4-6"
CLAUDE_HAIKU = "anthropic.claude-3-haiku-20240307-v1:0"

# --- Mock research tools ---
SEARCH_WEB_TOOL = {"toolSpec": {"name": "search_web", "description": "Search the web for information.", "inputSchema": {"json": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}}}
SEARCH_DB_TOOL = {"toolSpec": {"name": "search_database", "description": "Search internal policy database.", "inputSchema": {"json": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}}}

def search_web(query):
    return json.dumps({"results": [
        f"FCA guidance on {query}: banks must implement risk-based approach",
        f"Recent enforcement actions related to {query} totalled 500M in fines",
        f"Industry best practices for {query} include automated monitoring",
    ]})

def search_database(query):
    return json.dumps({"results": [
        f"Internal policy 4.2: {query} procedures must be reviewed annually",
        f"Compliance bulletin: updated {query} requirements effective Q2 2025",
    ]})

RESEARCH_TOOLS = [SEARCH_WEB_TOOL, SEARCH_DB_TOOL]
RESEARCH_DISPATCH = {"search_web": search_web, "search_database": search_database}


# TODO 1: Define the supervisor agent
# System prompt should instruct it to:
# - Analyze the user's request
# - Break it into subtasks for research, writing, and review
# - Coordinate the workflow and produce a final output
# Model: CLAUDE_SONNET (quality reasoning)
# No tools — supervisor delegates verbally
supervisor = ...

# TODO 2: Define the research agent
# System prompt: "You are a research specialist. Find relevant information using your tools."
# Model: CLAUDE_HAIKU (fast/cheap for research)
# Tools: RESEARCH_TOOLS, dispatch: RESEARCH_DISPATCH
researcher = ...

# TODO 3: Define the writer agent
# System prompt: "You are a professional writer. Create clear, well-structured content."
# Model: CLAUDE_SONNET (quality writing)
# No tools — just generation
writer = ...


def run_pipeline(task):
    """Run the multi-agent pipeline: research -> write -> review.

    Args:
        task: The user's task/request string.

    Returns:
        Dict with research, draft, and review results.
    """
    print(f"\nTask: {task}")
    print("=" * 60)

    # TODO 4: Implement the orchestration loop
    # 1. Call researcher.run() with the research task
    # 2. Feed research results to writer.run() with writing instructions
    # 3. Return results dict
    # Hint:
    #   research = researcher.run(f"Research: {task}")
    #   draft = writer.run(f"Based on this research, write a clear report:\n\n{research}\n\nOriginal task: {task}")
    ...

    # TODO 5: Add a reviewer agent
    # Model: CLAUDE_HAIKU (fast for review)
    # System prompt: "Critique the writing for accuracy and completeness."
    # Call reviewer.run() with the draft
    ...

    # TODO 6: Print timing summary showing which model each agent used
    # Example: "[Researcher] Haiku - 1.2s | [Writer] Sonnet - 3.5s | [Reviewer] Haiku - 0.8s"
    ...


# TODO 7 (BONUS): Parallel execution
# Use concurrent.futures.ThreadPoolExecutor to run independent agents simultaneously.
# For example, if you had two research agents, run them in parallel.
# Hint:
#   from concurrent.futures import ThreadPoolExecutor
#   with ThreadPoolExecutor(max_workers=2) as executor:
#       future1 = executor.submit(agent1.run, "task 1")
#       future2 = executor.submit(agent2.run, "task 2")
#       result1 = future1.result()
#       result2 = future2.result()


if __name__ == "__main__":
    result = run_pipeline("Write a brief report on the key AML compliance requirements for UK banking")
    if result:
        print(f"\n=== Final Output ===")
        print(f"Research: {str(result.get('research', ''))[:200]}...")
        print(f"Draft: {str(result.get('draft', ''))[:200]}...")
        if 'review' in result:
            print(f"Review: {str(result.get('review', ''))[:200]}...")
