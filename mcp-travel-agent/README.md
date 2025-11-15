# MCP Travel Agent (starter)

## Overview
This is a starter scaffold for a Travel Planning Agent using a local MCP server (mock). The MCP server exposes endpoints for searching flights/hotels and booking flights. The orchestration agent demonstrates tool-calling and simple planning.

## Run MCP server
cd mcp_server
pip install -r ../requirements.txt
uvicorn app:app --reload --port 8000

## Run Orchestrator
cd ..
python agent/orchestrator.py

## Next steps
- Replace mock providers with real API integrations (Amadeus / Skyscanner / Booking)
- Swap parse_user_request with LLM parsing (OpenAI/other)
- Add secure booking flows and payment integration (use test/sandbox)
- Add memory store (vector DB) and user profiles
