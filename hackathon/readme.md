# Hackathon: Build Your Own Multi-Agent System

Work in teams of 3-4 to build a multi-agent system using the patterns and tools from the past two days.

---

## Rules

1. **Time:** 2.5 hours to build, then 5 min demo + 3 min Q&A per team
2. **Use what you learned:** Your system must use at least 2 patterns from the labs (tool use, routing, multi-agent, MCP, etc.)
3. **Start from building blocks:** Copy and adapt the templates in `building-blocks/` -- don't start from scratch
4. **Plug in tools:** Use pre-built tools from `tools/` or write your own
5. **Mixed models encouraged:** Use Haiku for fast/cheap tasks, Sonnet for quality tasks
6. **Stretch goals:** MCP integration, A2A between teams, parallel agents

---

## Building Blocks

| Template | Description | Based on |
|----------|-------------|----------|
| `agent_template_raw.py` | Minimal raw Bedrock agent with agent loop | Lab 02 |
| `agent_template_langgraph.py` | Minimal LangGraph StateGraph agent | Lab 05a |
| `agent_template_strands.py` | Minimal Strands SDK agent | Lab 05c |
| `receptionist_template.py` | Intent classifier + specialist routing | Lab 04 |
| `multi_agent_template.py` | Supervisor + worker agents | Lab 06 |

## Pre-Built Tools

| Tool | File | What it does |
|------|------|-------------|
| Calculator | `tools/calculator.py` | Basic math operations |
| Web Search | `tools/web_search.py` | Mock web search results |
| Summarizer | `tools/summarizer.py` | Text summarization via Bedrock |
| Translator | `tools/translator.py` | Translation via Bedrock |
| Sentiment | `tools/sentiment.py` | Sentiment analysis via Bedrock |
| Code Executor | `tools/code_executor.py` | Safe Python code execution |
| Database | `tools/database.py` | SQLite query tool |
| File Tools | `tools/file_tools.py` | Read/write/search files |

## MCP Servers

| Server | File | What it exposes |
|--------|------|----------------|
| Database | `mcp-servers/database_server.py` | SQLite database as MCP tools |
| File System | `mcp-servers/file_server.py` | File system as MCP tools |

## Sample Data

| File | Contents |
|------|----------|
| `data/faq_data.json` | 20 FAQ entries for a banking service |
| `data/product_catalog.json` | Banking product descriptions |
| `data/sample_queries.json` | Test queries for evaluation |

---

## Suggested Themes

### 1. Smart Customer Support
A receptionist routes to FAQ agent, billing agent, and tech support agent. Each specialist has its own tools and knowledge base.
- **Patterns:** Receptionist (Lab 04) + Multi-agent (Lab 06)
- **Tools:** FAQ data, database, summarizer

### 2. Research & Report Pipeline
User asks a question. Research agent gathers info, analyst agent processes it, writer agent creates a report, reviewer agent QAs it.
- **Patterns:** Multi-agent supervisor (Lab 06)
- **Tools:** Web search, summarizer, file tools

### 3. Code Review Squad
User submits code. Style agent checks formatting, security agent checks vulnerabilities, logic agent checks correctness, lead agent aggregates feedback.
- **Patterns:** Multi-agent (Lab 06) + parallel execution
- **Tools:** Code executor, file tools

### 4. Data Pipeline Orchestrator
Supervisor agent manages: ingest agent pulls data, transform agent cleans it, validate agent checks quality, load agent stores results.
- **Patterns:** Multi-agent (Lab 06) + MCP (Lab 07)
- **Tools:** Database, file tools, calculator

### 5. Agentic Testing System
Test-generator agent creates test cases from requirements, executor agent runs them, reporter agent creates test reports.
- **Patterns:** Multi-agent (Lab 06)
- **Tools:** Code executor, file tools, summarizer

---

## Peer Review Rubric

| Criteria | Points | Description |
|----------|--------|-------------|
| Working system | 25 | Does it run? Can you demo it? |
| Multi-agent pattern | 25 | Did you use supervisor/routing/delegation? |
| Tool integration | 20 | MCP, custom tools, pre-built tools? |
| Creativity & ambition | 15 | Novel idea, stretch goals attempted? |
| Code quality | 15 | Clean architecture, error handling? |
| **Total** | **100** | |

---

## Getting Started

```bash
# 1. Pick a theme (or invent your own)
# 2. Copy the relevant building block template
cp building-blocks/multi_agent_template.py my_project.py

# 3. Add tools you need
# 4. Customize system prompts and agent logic
# 5. Test with sample queries from data/sample_queries.json
# 6. Iterate and improve!
```
