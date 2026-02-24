# Agentic AI Labs -- Participant Guide

> Everything you need to set up, run, and complete all labs for the Agentic AI module.

---

## Table of Contents

- [Environment Setup](#environment-setup)
- [Quick Reference](#quick-reference)
- [Lab Overview](#lab-overview)
- [Lab Details](#lab-details)
- [Useful Commands](#useful-commands)
- [Troubleshooting](#troubleshooting)
- [File Structure](#file-structure)

---

## Environment Setup

### 1. AWS Bedrock Authentication

We use a **Bedrock API key** (bearer token) — no IAM access keys needed.

Get your token from your instructor, then export it in your terminal:

```bash
export AWS_BEARER_TOKEN_BEDROCK=bedrock-api-key-...
```

That's it. boto3 picks it up automatically.

> **Note:** Tokens expire. When yours expires, get a fresh one from your instructor and re-export.

### 2. Model Access

You need access to these models in your AWS Bedrock console (ap-south-1):

| Model | ID | Used in |
|-------|----|---------|
| Claude Sonnet | `global.anthropic.claude-sonnet-4-6` | All labs (generation) |
| Claude Haiku | `anthropic.claude-3-haiku-20240307-v1:0` | Labs 04+ (classification) |

Request access in the [AWS Bedrock Console](https://console.aws.amazon.com/bedrock/) under **Model access**.

### 3. Python Environment

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate    # macOS/Linux
# venv\Scripts\activate     # Windows

# Install all dependencies
pip install -r shared/requirements.txt
```

### 4. Verify Everything

```bash
python -c "
import boto3
client = boto3.client('bedrock-runtime', region_name='ap-south-1')
response = client.converse(
    modelId='anthropic.claude-3-haiku-20240307-v1:0',
    messages=[{'role': 'user', 'content': [{'text': 'Say hello in 5 words'}]}],
)
print(response['output']['message']['content'][0]['text'])
print('Setup OK!')
"
```

---

## Quick Reference

| Item | Value |
|------|-------|
| Region | `ap-south-1` |
| Sonnet model ID | `global.anthropic.claude-sonnet-4-6` |
| Haiku model ID | `anthropic.claude-3-haiku-20240307-v1:0` |
| boto3 client | `boto3.client("bedrock-runtime", region_name="ap-south-1")` |
| Converse API | `client.converse(modelId=..., messages=..., system=..., toolConfig=...)` |

---

## Lab Overview

| Lab | Topic | Type | Duration | Key Concept |
|-----|-------|------|----------|-------------|
| 01 | Hello Bedrock | Core | 20 min | Converse API, model comparison |
| 02 | First Agent | Core | 45 min | Agent loop, tool use, tool dispatch |
| 03 | Smart Agent | Core | 40 min | ReAct prompting, error handling |
| 04 | Receptionist | Core | 60 min | Intent classification, routing, SLM vs LLM |
| 05a | LangGraph | Core | 45 min | StateGraph, nodes, conditional edges |
| 05c | Strands SDK | Core | 30 min | @tool decorator, minimal agent code |
| 06 | Multi-Agent | Core | 50 min | Supervisor pattern, mixed models |
| 07 | MCP | Core | 50 min | Tool discovery, MCP server/client |
| 08 | A2A | Stretch | 50 min | Agent-to-agent protocol, agent cards |

---

## Lab Details

### Lab 01: Hello Bedrock

| | |
|---|---|
| **Folder** | `lab-01-hello-bedrock/` |
| **Files** | `start/main.py` → `solution/main.py` |
| **Run** | `python start/main.py` |
| **Key concept** | Converse API, Sonnet vs Haiku |

### Lab 02: Build Your First Agent

| | |
|---|---|
| **Folder** | `lab-02-first-agent/` |
| **Files** | `start/tools.py`, `start/main.py` → solutions |
| **Run** | `python start/main.py` |
| **Key concept** | The agent loop (toolConfig → tool_use → dispatch → toolResult) |

### Lab 03: Smart Agent

| | |
|---|---|
| **Folder** | `lab-03-smart-agent/` |
| **Files** | `start/main.py` → `solution/main.py` |
| **Run** | `python start/main.py` |
| **Key concept** | ReAct prompting, error handling, summarization |

### Lab 04: Build a Receptionist

| | |
|---|---|
| **Folder** | `lab-04-receptionist/` |
| **Files** | `start/main.py`, `start/specialists.py` → solutions |
| **Run** | `python start/main.py` |
| **Key concept** | Intent classification (Haiku), specialist routing (Sonnet) |

### Lab 05a: LangGraph Agent

| | |
|---|---|
| **Folder** | `lab-05a-langgraph/` |
| **Files** | `start/main.py` → `solution/main.py` |
| **Run** | `pip install -r start/requirements.txt && python start/main.py` |
| **Key concept** | StateGraph, conditional edges, graph compilation |

### Lab 05c: Strands Agent

| | |
|---|---|
| **Folder** | `lab-05c-strands/` |
| **Files** | `start/main.py` → `solution/main.py` |
| **Run** | `pip install -r start/requirements.txt && python start/main.py` |
| **Key concept** | @tool decorator, Agent class, minimal code |

### Lab 06: Multi-Agent System

| | |
|---|---|
| **Folder** | `lab-06-multi-agent/` |
| **Files** | `start/agents.py`, `start/main.py` → solutions |
| **Run** | `python start/main.py` |
| **Key concept** | Supervisor pattern, mixed models (Haiku + Sonnet) |

### Lab 07: MCP Server & Client

| | |
|---|---|
| **Folder** | `lab-07-mcp/` |
| **Files** | `start/server.py`, `start/client.py` → solutions |
| **Run** | `pip install -r start/requirements.txt && python start/client.py` |
| **Key concept** | MCP protocol, tool discovery, dynamic tool loading |

### Lab 08: A2A Agent Network (Stretch)

| | |
|---|---|
| **Folder** | `lab-08-a2a/` |
| **Files** | `start/a2a_server.py`, `start/a2a_client.py`, `start/agent_card.json` → solutions |
| **Run** | `pip install -r start/requirements.txt` then run server + client separately |
| **Key concept** | Agent cards, task lifecycle, agent interoperability |

---

## Useful Commands

### AWS CLI

```bash
# Check your identity
aws sts get-caller-identity

# List available Bedrock models
aws bedrock list-foundation-models --region ap-south-1 --query "modelSummaries[?contains(modelId, 'claude')].[modelId,modelName]" --output table
```

### Python Quick Tests

```bash
# Test Bedrock connection
python -c "import boto3; c=boto3.client('bedrock-runtime',region_name='ap-south-1'); print('Connected!')"

# Test a specific lab
cd lab-02-first-agent && python solution/main.py
```

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| `NoCredentialError` | AWS credentials not configured | Run `aws configure` or set env vars |
| `AccessDeniedException` | Model access not enabled | Request access in Bedrock Console |
| `ThrottlingException` | Too many API calls | Wait a few seconds and retry |
| `ValidationException: model not found` | Wrong model ID or region | Check model ID and region (ap-south-1) |
| `ModuleNotFoundError` | Missing Python package | Run `pip install -r shared/requirements.txt` |
| `ResourceNotFoundException` | Model not available in region | Verify model is available in ap-south-1 |

---

## File Structure

```
labs/
├── README.md                          ← You are here
├── shared/
│   ├── requirements.txt               # All Python dependencies
│   ├── bedrock_client.py              # Shared Bedrock helper utilities
│   └── logging_utils.py              # Agent trace logging
├── lab-01-hello-bedrock/
│   ├── readme.md
│   ├── start/main.py                  # 6 TODOs
│   └── solution/main.py
├── lab-02-first-agent/
│   ├── readme.md
│   ├── start/main.py                  # 3 TODOs (agent loop)
│   ├── start/tools.py                 # 4 TODOs (tool schemas)
│   ├── solution/main.py
│   └── solution/tools.py
├── lab-03-smart-agent/
│   ├── readme.md
│   ├── start/main.py                  # 5 TODOs
│   └── solution/main.py
├── lab-04-receptionist/
│   ├── readme.md
│   ├── start/main.py                  # 8 TODOs
│   ├── start/specialists.py           # 3 specialists to implement
│   ├── solution/main.py
│   └── solution/specialists.py
├── lab-05a-langgraph/
│   ├── readme.md
│   ├── start/main.py                  # 8 TODOs
│   ├── start/requirements.txt
│   └── solution/main.py
├── lab-05c-strands/
│   ├── readme.md
│   ├── start/main.py                  # 6 TODOs
│   ├── start/requirements.txt
│   └── solution/main.py
├── lab-06-multi-agent/
│   ├── readme.md
│   ├── start/main.py                  # 7 TODOs
│   ├── start/agents.py               # Agent class skeleton
│   ├── solution/main.py
│   └── solution/agents.py
├── lab-07-mcp/
│   ├── readme.md
│   ├── start/server.py               # 3 TODOs
│   ├── start/client.py               # 5 TODOs
│   ├── start/requirements.txt
│   ├── solution/server.py
│   └── solution/client.py
├── lab-08-a2a/
│   ├── readme.md
│   ├── start/agent_card.json
│   ├── start/a2a_server.py            # 4 TODOs
│   ├── start/a2a_client.py            # 5 TODOs
│   ├── start/requirements.txt
│   ├── solution/agent_card.json
│   ├── solution/a2a_server.py
│   └── solution/a2a_client.py
└── hackathon/
    ├── readme.md
    ├── building-blocks/               # 5 templates from lab solutions
    ├── tools/                         # 8 pre-built tools
    ├── mcp-servers/                   # 2 MCP servers
    ├── a2a/                           # A2A templates
    └── data/                          # Sample datasets (FAQ, products, queries)
```
