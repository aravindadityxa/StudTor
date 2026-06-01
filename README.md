# StudTor — Offline AI Learning Companion

StudTor is a lightweight AI-powered learning assistant that runs entirely on your own machine.

No cloud APIs. No subscriptions. No usage limits. Just fast, private, and reliable AI assistance for learning, studying, coding, and everyday knowledge exploration.

---

# Why StudTor?

Most AI assistants depend on internet connectivity and paid API services.

StudTor takes a different approach.

By using local Large Language Models (LLMs) through Ollama, StudTor delivers an AI experience that is:

* Completely private
* Free to run
* Fast and responsive
* Multi-language capable
* Built specifically for students and learners
* Fully functional without internet access

Everything stays on your device.

---

# Features

## Local AI Assistant

Run modern language models directly on your computer using Ollama.

## Privacy First

Your conversations, learning history, and data never leave your machine.

## Learning-Oriented Experience

Designed for:

* Students
* Self-learners
* Programmers
* Exam preparation
* Educational assistance

## Multi-Language Support

Ask questions and learn in multiple languages.

## Local Storage

Chat history and user data are stored locally using SQLite.

## No API Costs

* No OpenAI credits
* No Gemini billing
* No monthly subscriptions

---

# Tech Stack

## Backend

* FastAPI
* SQLite
* JWT Authentication
* Ollama Integration

## Frontend

* HTML
* CSS
* JavaScript

## AI Layer

* Ollama
* Qwen 2.5 (1.5B) by default

---

# Project Structure

```text
StudTor/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── studtor.db
│   └── .env
│
├── frontend/
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── assets/
│
└── README.md
```

---

# Installation

## 1. Install Ollama

Download and install Ollama:

https://ollama.com

Verify installation:

```bash
ollama --version
```

---

## 2. Create Virtual Environment

```bash
python -m venv studtor_env
```

Activate it:

### Windows

```bash
studtor_env\Scripts\activate
```

### Linux / macOS

```bash
source studtor_env/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

---

## 4. Download AI Model

Recommended model:

```bash
ollama pull qwen2.5:1.5b
```

---

## 5. Configure Environment

Create:

```env
backend/.env
```

Add:

```env
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:1.5b
```

---

## 6. Start Ollama

```bash
ollama serve
```

---

## 7. Start Backend

```bash
cd backend

uvicorn main:app --reload
```

Backend runs at:

```text
http://localhost:8000
```

---

## 8. Start Frontend

```bash
cd frontend

python -m http.server 5500
```

Open:

```text
http://localhost:5500
```

---

# Supported Models

StudTor works with any Ollama-compatible model.

### Lightweight (Recommended)

```bash
qwen2.5:1.5b
```

### Better Quality

```bash
mistral
```

### Conversational

```bash
neural-chat
```

### Coding

```bash
deepseek-coder
```

To switch models:

```env
OLLAMA_MODEL=mistral
```

Restart the backend after making changes.

---

# API Endpoints

## Public Endpoints

| Method | Endpoint     | Description        |
| ------ | ------------ | ------------------ |
| POST   | /chat/public | Public chat access |
| GET    | /health      | Health check       |
| GET    | /ai/status   | AI provider status |

## Authentication Endpoints

| Method | Endpoint         |
| ------ | ---------------- |
| POST   | /register        |
| POST   | /login           |
| POST   | /forgot-password |

## User Endpoints

| Method | Endpoint      |
| ------ | ------------- |
| POST   | /chat         |
| GET    | /chat/history |
| DELETE | /chat/history |

---

# System Requirements

## Minimum

* 4 GB RAM
* Dual-Core CPU
* 5 GB Free Storage

## Recommended

* 8 GB or more RAM
* Modern Quad-Core CPU
* SSD Storage

No dedicated GPU is required.

---

# Privacy

StudTor is built around local-first computing.

* No external AI APIs
* No hidden analytics
* No tracking
* No data collection
* No cloud dependency

Your conversations remain on your device.

---

# Troubleshooting

## Ollama Not Running

```bash
ollama serve
```

Ensure Ollama is installed and running.

---

## Model Not Found

```bash
ollama pull qwen2.5:1.5b
```

---

## Backend Fails to Start

Verify dependencies:

```bash
pip install -r backend/requirements.txt
```

Check Python version:

```bash
python --version
```

Python 3.8 or later is required.

---

# Contributing

Contributions, improvements, bug fixes, and feature suggestions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

---

# License

This project is licensed under the terms provided in the LICENSE file.

---

# Vision

StudTor aims to make AI-powered learning accessible to everyone without requiring subscriptions, cloud services, or sacrificing privacy.

Learn smarter. Stay private. Own your AI.
