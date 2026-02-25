"""
Hackathon: Banking Receptionist Chatbot — Backend

This is YOUR file. Build your receptionist system here.

The chatbot_ui.py imports handle_message() from this file.
Your job: classify the user's intent, route to the right sub-agent,
and return a response.

Available resources:
    building-blocks/    — Agent templates (raw, receptionist, multi-agent, LangGraph, Strands)
    tools/              — Pre-built tools (calculator, sentiment, summarizer, database, etc.)
    data/faq_data.json  — 20 banking FAQs
    data/product_catalog.json — 8 banking products
    data/sample_queries.json  — 20 labeled test queries
"""


def handle_message(user_message: str) -> dict:
    """
    Process a user message and return a response.

    Args:
        user_message: The customer's message.

    Returns:
        dict with keys:
        - "response": str — the agent's answer
        - "intent": str — which sub-agent handled it (faq, account, payments, products, complaints)
        - "confidence": float — classifier confidence (0.0 to 1.0)
    """
    # ──────────────────────────────────────────────────────────
    # Build your receptionist system here!
    #
    # Suggested architecture:
    #   1. Classify intent with Haiku (fast, cheap)
    #   2. Route to the right specialist agent (Sonnet, quality)
    #   3. Each specialist can have its own tools
    #
    # See building-blocks/receptionist_template.py for a starting point.
    # ──────────────────────────────────────────────────────────
    return {
        "response": "I'm not set up yet. Build me! Edit backend.py to get started.",
        "intent": "none",
        "confidence": 0.0,
    }
