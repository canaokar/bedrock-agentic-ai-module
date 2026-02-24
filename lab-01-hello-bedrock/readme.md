# Lab 01: Hello Bedrock

Get comfortable with the AWS Bedrock Converse API by making your first LLM calls, comparing models, and building a multi-turn chat.

## Objectives

- Initialize a boto3 Bedrock runtime client
- Call the Converse API with system prompts and user messages
- Extract response text from the Bedrock response structure
- Compare Claude Sonnet vs Haiku (speed, quality, cost)
- Build a multi-turn conversation with message history

---

## Prerequisites

- AWS credentials configured (`aws configure` or environment variables)
- Python packages: `boto3`
- Model access enabled for Claude Sonnet and Claude Haiku in your AWS account

---

## Step 1: Make Your First LLM Call

Open `start/main.py` and implement TODOs 1-3.

### What you are building

A function that calls the Bedrock Converse API with a system prompt and user message, then extracts the response text.

### Key concepts

- **boto3 client**: `boto3.client("bedrock-runtime", region_name="ap-south-1")` creates the API client
- **Converse API**: unified interface for calling any model on Bedrock
- **Message structure**: `[{"role": "user", "content": [{"text": "..."}]}]`
- **System prompt**: passed as `system=[{"text": "..."}]` to set the model's behavior
- **Response path**: `response["output"]["message"]["content"][0]["text"]`

### Checkpoint

Run `python start/main.py` and verify:
- You see a response about AML compliance components
- No errors about credentials or model access

---

## Step 2: Compare Models

Implement TODO 4 in `start/main.py`.

### What you are building

A function that calls the same prompt with both Claude Sonnet and Claude Haiku, timing each call to show the speed vs quality trade-off.

### Key concepts

- **Claude Sonnet**: more capable, better for complex reasoning and generation
- **Claude Haiku**: faster and cheaper, good for classification, routing, simple tasks
- **Cost difference**: Haiku is significantly cheaper per token than Sonnet
- **When to use which**: use Haiku for fast/cheap tasks (classification, routing), Sonnet for quality tasks (generation, reasoning)

### Checkpoint

- Both models return meaningful responses
- Haiku responds noticeably faster than Sonnet
- Sonnet's response may be more detailed

---

## Step 3: Multi-Turn Chat

Implement TODO 5 in `start/main.py`.

### What you are building

An interactive chat loop that maintains conversation history across turns, so the model remembers what was said earlier.

### Key concepts

- **Message history**: append each user and assistant message to a growing list
- **Context window**: the model sees all previous messages on each call
- **Memory pattern**: this is how agents maintain conversational context

### Checkpoint

Uncomment the chat loop in `__main__` and test:
- Ask "What is KYC?" then follow up with "Who enforces it?" — the model should understand "it" refers to KYC

---

## Step 4 (Stretch): Streaming Responses

Implement TODO 6 in `start/main.py`.

### What you are building

A streaming call using `converse_stream()` that prints tokens as they arrive, providing a more responsive user experience.

### Key concepts

- **converse_stream()**: returns a stream of events instead of waiting for the full response
- **contentBlockDelta**: event type that contains partial text tokens
- **Use case**: better UX for long responses, real-time display

### Checkpoint

Uncomment the streaming section and verify tokens print incrementally.

---

## Recap

| Step | What you built | Key takeaway |
|------|---------------|--------------|
| 1 | Basic Converse call | Bedrock API structure and response format |
| 2 | Model comparison | Sonnet for quality, Haiku for speed/cost |
| 3 | Multi-turn chat | Message history is how agents remember |
| 4* | Streaming | Better UX with real-time token output |
