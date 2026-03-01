# Architecture & Decision Log

This document records the major architectural choices, technical decisions, and constraints for the Business Intelligence (BI) Agent project.

## 1. Core Frameworks & Libraries
* **UI Framework:** [Streamlit](https://streamlit.io/)
  * *Reasoning:* Enables rapid development of conversational web interfaces entirely in Python without needing a separate frontend stack (e.g., React/Node.js). Streamlit natively supports chat interfaces (`st.chat_message`, `st.chat_input`).
* **Agent Orchestration:** [LangChain Classic](https://python.langchain.com/) (`langchain_classic.agents`)
  * *Reasoning:* Provides robust abstractions for tool-calling agents, memory management, and prompt handling, seamlessly integrating with Streamlit through `StreamlitCallbackHandler` for thought-process streaming.

## 2. LLM & Inference Engine
* **Model Engine:** `openai/gpt-oss-120b` running on [Groq](https://groq.com/)
  * *Reasoning:* Explicitly mandated by project requirements. Groq is used to provide ultra-fast inference speeds necessary for real-time natural language to API query translations.

## 3. Data Integration Strategy
* **Data Source:** [Monday.com GraphQL API](https://developer.monday.com/api-reference/docs)
  * *Decision:* Direct HTTP POST requests using the `requests` library to execute raw GraphQL queries targeting specific Boards (Deals: `5026874399`, Work Orders: `5026874265`).
  * *Reasoning:* Avoids the overhead of heavy third-party SDKs and provides strict control over the exact payloads retrieved.
* **Real-time vs. Cached Data:** Live Execution
  * *Decision:* The agent is instructed via system prompt to *never* rely on cached data. Every user query initiates a fresh API call.
  * *Reasoning:* BI dashboards require up-to-the-minute accuracy, particularly concerning sales pipeline values and operational status.

## 4. Deployment & Infrastructure
* **Containerization:** Docker & Docker Compose
  * *Reasoning:* Ensures environment parity across development, testing, and production. Docker simplifies dependency management (using `python:3.11-slim`) and resolves cross-platform deployment issues.
* **State Management:** Streamlit `st.session_state`
  * *Reasoning:* Used locally within the container memory to track conversation history `messages`. Simple and effective for stateless container deployments without needing an external database (like Redis) for the current MVP scale.

## 5. Security Practices
* **Secret Management:** `.env` files & `python-dotenv`
  * *Reasoning:* Prevents hardcoding of sensitive Monday.com and Groq API keys directly into the source code.
* **Git Configuration:** `.gitignore` & `.dockerignore`
  * *Reasoning:* Prevents accidental commitment of local virtual environments (`venv`), environment variable files (`.env`), and caching directories (`__pycache__`) to the repository and Docker image build context.
