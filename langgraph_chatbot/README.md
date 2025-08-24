# LangGraph Chatbot 🤖

A modular chatbot built with **LangGraph** and **Groq LLMs**, featuring logging, exception handling, graph visualization, REST API (FastAPI), and a Streamlit frontend. Now fully deployed on **Render** 🚀.

---

## 🌐 Live Deployment

* **Frontend (Streamlit UI):** [https://genai-course-langchain.onrender.com/](https://genai-course-langchain.onrender.com/)
* **Backend (FastAPI API):** [https://genai-course-langchain-1.onrender.com/](https://genai-course-langchain-1.onrender.com/)

  * Health check: [https://genai-course-langchain-1.onrender.com/health](https://genai-course-langchain-1.onrender.com/health)
  * Chat endpoint: [https://genai-course-langchain-1.onrender.com/chat](https://genai-course-langchain-1.onrender.com/chat)

---

## 📊 Graph Visualizations

The chatbot generates **two different visualizations**:

* **Static State Graph** (`graph.png`)
  ![Chatbot Graph](./langgraph_chatbot/static/graph.png)

* **Runtime Graph with Tools** (`graph_with_tools.png`)
  Generated dynamically when you run the chatbot.
  ![Graph with Tools](./langgraph_chatbot/static/graph_with_tools.png)

---

## 📌 Features

* **LangGraph State Machine** for managing chatbot flow.
* **Groq API Integration** (`deepseek-r1-distill-llama-70b`).
* **Memory Support** → Conversations now **remember history**.
* **Structured Logging** for debugging and monitoring.
* **Exception Handling** to keep the chatbot running smoothly.
* **Graph Visualization** (`graph.png` & `graph_with_tools.png`).
* **Tool Integration**:

  * 🔎 Wikipedia
  * 📄 Arxiv
* **Multi-Interface Support**:

  * ✅ Console-based chatbot
  * ✅ FastAPI backend (`/chat` endpoint)
  * ✅ Streamlit frontend UI
* **Console Output** (CLI mode):

  * Assistant responses (green).
  * Tool calls and results (yellow, with tool name shown).

---

## 📂 Project Structure

```
langgraph_chatbot/
│── __init__.py
│── config.py          # Environment variables & LangSmith setup
│── utils.py           # Logging & error handling
│── tools.py           # Wikipedia & Arxiv tool definitions
│── chatbot.py         # LangGraph chatbot definition (with history)
│── main.py            # Console entry point
│
├── backend/           # FastAPI backend
│   └── main.py        # Exposes chatbot as REST API
│
├── frontend/          # Streamlit frontend
│   └── app.py         # Web UI that calls FastAPI backend
│
└── static/            # Stores generated graphs
    │── graph.png          # Static graph visualization
    └── graph_with_tools.png  # Runtime graph visualization
```

---

## ⚙️ Installation (Local)

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key
LANGSMITH_API_KEY=your_langsmith_key   
```

---

## 🚀 Usage

### ▶️ Run in Console Mode

```bash
python -m langgraph_chatbot.main
```

Example:

```
👤 You: hi my name is Sushant
🤖 Assistant: Hello, Sushant! How can I help you today?

👤 You: who is Shah Rukh Khan?
🛠️ Tool Called: Wikipedia
Shah Rukh Khan is an Indian actor, film producer, and television personality...

🤖 Assistant: Shah Rukh Khan is a famous Indian actor, often called the "King of Bollywood."
```

Exit with:

```
👤 You: quit
```

### ▶️ Run as Web App (Local FastAPI + Streamlit)

From the **project root**:

1. Start backend (FastAPI):

```bash
uvicorn langgraph_chatbot.backend.main:app --reload --port 8000
```

This runs the chatbot API at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

2. Start frontend (Streamlit):

```bash
streamlit run langgraph_chatbot/frontend/app.py
```

This runs the web UI at: [http://localhost:8501](http://localhost:8501)

---

## ✅ Requirements

* Python **3.10+** recommended
* Dependencies managed via `pip` and `requirements.txt`

---

## 🛠️ Development Notes

* `graph.png` → created when building the graph in `chatbot.py`.
* `graph_with_tools.png` → generated dynamically at runtime.
* Both console & web interfaces share the same **LangGraph state machine**.

---

👉 This README now reflects:

* ✅ Backend (FastAPI)
* ✅ Frontend (Streamlit)
* ✅ Memory support
* ✅ Deployment on **Render** 🎉
* ✅ Updated project structure
