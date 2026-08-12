# 🧠 Meeting Memory Agent

An AI-powered meeting preparation agent that remembers a client's past interactions, concerns, preferences, and commitments.

Instead of starting from zero before every meeting, the agent uses **Hindsight** as a long-term memory layer to retrieve relevant client history and generate personalized meeting preparation.

## 🎯 Problem

Client relationships contain valuable information spread across multiple meetings:

- Previous concerns and objections
- Pricing discussions
- Security and compliance requirements
- Promises and follow-ups
- Decisions and commitments

A normal AI assistant may only see the current conversation and miss this history.

## 💡 Solution

Meeting Memory Agent gives each client a dedicated memory bank.

When a meeting note is added:

```text
Meeting Note
     │
     ▼
Hindsight retain()
     │
     ▼
Client Memory Bank
