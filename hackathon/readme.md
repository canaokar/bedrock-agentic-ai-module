# Hackathon: Banking Receptionist Chatbot

Build a **banking chatbot** with a receptionist that classifies customer intent and routes to 5 specialist sub-agents. You get a working Streamlit chat UI — your job is to build the brain behind it.

---

## Quick Start

```bash
# 1. Install Streamlit (if not already)
pip install streamlit

# 2. Run the chatbot
streamlit run chatbot_ui.py

# 3. It will say "I'm not set up yet" — that's expected!
#    Open backend.py and build your receptionist system.
```

---

## The Challenge

Build a `handle_message()` function in **`backend.py`** that:

1. **Classifies** the customer's intent using Haiku (fast, cheap)
2. **Routes** to the right specialist sub-agent using Sonnet (quality)
3. **Returns** a response with the intent label and confidence score

### Required Sub-Agents

| Sub-Agent | Handles | Data / Tools |
|-----------|---------|--------------|
| **FAQ** | Opening hours, card loss, general questions | `data/faq_data.json` |
| **Account** | Balance, transactions, account settings | Mock tools (check_balance, get_transactions) |
| **Payments** | Transfers, standing orders, direct debits | Mock tools (initiate_transfer, check_status) |
| **Products** | Product recommendations, comparisons | `data/product_catalog.json` |
| **Complaints** | Customer complaints, escalations | Empathetic responses, escalation logic |

### Requirements

- Receptionist uses **Haiku** for classification (fast/cheap)
- Specialists use **Sonnet** for quality responses
- At least **2 sub-agents must have tools** (not just prompt-only)
- Handle **off-topic queries** and **low confidence** gracefully
- Return the dict format that `chatbot_ui.py` expects: `{"response": ..., "intent": ..., "confidence": ...}`

### Bonus Challenges

- Add **conversation memory** (multi-turn within a specialist)
- Add a **"transfer to human"** escalation path for complaints
- Use **extended thinking** for complex queries
- Serve one data source via an **MCP server**
- Expose your chatbot as an **A2A agent** that other teams can call

---

## Rules

1. **Time:** 2.5 hours to build, then 5 min demo + 3 min Q&A per team
2. **Use what you learned:** Your system must use at least 2 patterns from the labs (tool use, routing, multi-agent, MCP, etc.)
3. **Start from building blocks:** Use the templates in `building-blocks/` — don't reinvent the wheel
4. **Plug in tools:** Use pre-built tools from `tools/` or write your own
5. **Mixed models:** Use Haiku for fast/cheap tasks, Sonnet for quality tasks

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
# 1. Open backend.py — this is YOUR file
# 2. Look at building-blocks/receptionist_template.py for the routing pattern
# 3. Look at building-blocks/agent_template_raw.py for tool-calling agents
# 4. Load data from data/faq_data.json and data/product_catalog.json
# 5. Build your classify → route → respond pipeline
# 6. Test with: streamlit run chatbot_ui.py
# 7. Try the sample queries from data/sample_queries.json
```
