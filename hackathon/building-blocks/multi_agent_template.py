"""
Hackathon Building Block: Multi-Agent Supervisor Template
A supervisor agent delegates to specialist worker agents.
Customize the agents, their prompts, and tools.

Based on Lab 06.
"""

import boto3

import json
import time

CLAUDE_SONNET = "us.anthropic.claude-sonnet-4-20250514"
CLAUDE_HAIKU = "us.anthropic.claude-haiku-4-20250514"
REGION = "ap-south-1"

client = boto3.client("bedrock-runtime", region_name=REGION)


def extract_text(message):
    for block in message.get("content", []):
        if "text" in block:
            return block["text"]
    return ""


class Agent:
    """Simple agent wrapper around Bedrock Converse."""

    def __init__(self, name, model_id, system_prompt):
        self.name = name
        self.model_id = model_id
        self.system_prompt = system_prompt

    def run(self, prompt):
        print(f"  [{self.name}] Running with {self.model_id}...")
        start = time.time()
        response = client.converse(
            modelId=self.model_id,
            system=[{"text": self.system_prompt}],
            messages=[{"role": "user", "content": [{"text": prompt}]}],
        )
        result = extract_text(response["output"]["message"])
        elapsed = time.time() - start
        print(f"  [{self.name}] Done ({elapsed:.1f}s)")
        return result


# --- Customize your agents ---
researcher = Agent(
    name="Researcher",
    model_id=CLAUDE_HAIKU,  # Fast/cheap for research
    system_prompt="You are a research specialist. Find and summarize key information on the given topic. Be thorough but concise.",
)

writer = Agent(
    name="Writer",
    model_id=CLAUDE_SONNET,  # Quality for writing
    system_prompt="You are a professional writer. Create well-structured, clear content based on the research provided.",
)

reviewer = Agent(
    name="Reviewer",
    model_id=CLAUDE_HAIKU,  # Fast for review
    system_prompt="You are a content reviewer. Critique the writing for accuracy, clarity, and completeness. Suggest specific improvements.",
)


def run_pipeline(task):
    """Run the multi-agent pipeline: research -> write -> review."""
    print(f"\nTask: {task}\n{'='*60}")

    # Step 1: Research
    research = researcher.run(f"Research the following topic: {task}")
    print(f"\n--- Research Output ---\n{research[:300]}...\n")

    # Step 2: Write
    writer_prompt = f"Based on this research, write a clear report:\n\n{research}\n\nOriginal task: {task}"
    draft = writer.run(writer_prompt)
    print(f"\n--- Draft Output ---\n{draft[:300]}...\n")

    # Step 3: Review
    review_prompt = f"Review this draft and suggest improvements:\n\n{draft}"
    review = reviewer.run(review_prompt)
    print(f"\n--- Review Output ---\n{review[:300]}...\n")

    return {"research": research, "draft": draft, "review": review}


if __name__ == "__main__":
    result = run_pipeline("Key requirements for AML compliance in UK banking")
