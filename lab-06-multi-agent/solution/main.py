"""
Lab 06: Multi-Agent System (Solution)
"""

import os
from pathlib import Path
import json
import time
from agents import Agent, CLAUDE_SONNET, CLAUDE_HAIKU

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

SEARCH_WEB_TOOL = {"toolSpec": {"name": "search_web", "description": "Search the web.", "inputSchema": {"json": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}}}
SEARCH_DB_TOOL = {"toolSpec": {"name": "search_database", "description": "Search internal database.", "inputSchema": {"json": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}}}

def search_web(query):
    return json.dumps({"results": [
        f"FCA guidance on {query}: banks must implement risk-based approach",
        f"Recent enforcement: {query} fines totalled 500M",
        f"Best practices for {query} include automated monitoring",
    ]})

def search_database(query):
    return json.dumps({"results": [
        f"Policy 4.2: {query} procedures reviewed annually",
        f"Bulletin: updated {query} requirements effective Q2 2025",
    ]})

researcher = Agent(
    name="Researcher",
    model_id=CLAUDE_HAIKU,
    system_prompt="You are a research specialist. Use your tools to find relevant information. Summarize findings clearly.",
    tools=[SEARCH_WEB_TOOL, SEARCH_DB_TOOL],
    tool_dispatch={"search_web": search_web, "search_database": search_database},
)

writer = Agent(
    name="Writer",
    model_id=CLAUDE_SONNET,
    system_prompt="You are a professional writer. Create clear, well-structured reports based on research provided.",
)

reviewer = Agent(
    name="Reviewer",
    model_id=CLAUDE_HAIKU,
    system_prompt="You are a content reviewer. Critique the writing for accuracy, completeness, and clarity. Suggest specific improvements.",
)


def run_pipeline(task):
    print(f"\nTask: {task}")
    print("=" * 60)
    overall_start = time.time()

    # Step 1: Research
    print("\n--- Step 1: Research ---")
    research = researcher.run(f"Research the following topic thoroughly: {task}")
    print(f"  Research output: {research[:200]}...\n")

    # Step 2: Write
    print("--- Step 2: Write ---")
    draft = writer.run(f"Based on this research, write a clear, professional report.\n\nResearch:\n{research}\n\nOriginal task: {task}")
    print(f"  Draft output: {draft[:200]}...\n")

    # Step 3: Review
    print("--- Step 3: Review ---")
    review = reviewer.run(f"Review this draft report and suggest improvements:\n\n{draft}")
    print(f"  Review output: {review[:200]}...\n")

    total = time.time() - overall_start
    print(f"Pipeline complete in {total:.1f}s")
    print(f"  Researcher: Haiku (fast/cheap)")
    print(f"  Writer: Sonnet (quality)")
    print(f"  Reviewer: Haiku (fast/cheap)")

    return {"research": research, "draft": draft, "review": review}


if __name__ == "__main__":
    result = run_pipeline("Key AML compliance requirements for UK banking in 2025")
