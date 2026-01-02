# Customer Support Agent

---

## Architecture

![Customer Support Agent Architecture](architecture.png)

---

## About the project:

An AI-powered customer support agent that understands customer emails, extracts intent, generates and executes SQL when required, and drafts a resolved response email. The system is built with a clean separation between UI, API, and agent logic, and is production-ready for containerized deployment.

---

## 📂 Folder Structure

```
agent-backend/
    ├── data/                  # Data files
    ├── src/                   # Main package directory
    │   ├── application/       # Application layer
    │   ├── infrastructure/    # Infrastructure layer
    │   └── config.py          # Configuration settings
    ├── tools/                 # Entrypoint scripts that use the Python package
    ├── .env.example           # Environment variables template
    ├── .python-version        # Python version specification
    ├── Dockerfile             # API Docker image definition
    └── pyproject.toml         # Project dependencies
```

## 🧪 Observability & Evaluation

* Prompt versioning and traces using **Opik**
* SQL generation evaluation using expected SQL/output scoring

---

## 🩺 API Endpoints

* `GET /health` → Service health check
* `POST /response` → Agent response for customer email

---

## 📦 Deployment

* Dockerized backend
* Image pushed to **AWS ECR**
* Deployed via **AWS ECS (Fargate / EC2)**

---

## 🧠 Tech Stack

* Python, FastAPI
* Streamlit
* LangGraph, LLM APIs
* PostgreSQL
* Docker, AWS ECS

---

