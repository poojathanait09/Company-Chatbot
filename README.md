# 🤖 AI-Powered Role-Based Company Chatbot (RAG + LLM)

## 📌 Overview

The AI-Powered Role-Based Company Chatbot is a secure internal knowledge assistant that enables employees to retrieve company-specific information using natural language queries.

The system leverages **Retrieval-Augmented Generation (RAG)**, **semantic search**, and **Large Language Models (LLMs)** to provide context-aware answers while enforcing **Role-Based Access Control (RBAC)** to ensure users only access information authorized for their role.

---

## 🚀 Features

* 🔐 JWT-based User Authentication
* 👥 Role-Based Access Control (RBAC)
* 🧠 Retrieval-Augmented Generation (RAG)
* 🔍 Semantic Search using Vector Embeddings
* 📚 Source Attribution and Citations
* 📊 Confidence Scoring
* 💬 Interactive Streamlit Chat Interface
* ⚡ FastAPI Backend APIs
* 📂 Support for Markdown and CSV Documents
* 🛡️ Department-Level Data Isolation

---

## 🏗️ System Architecture

```text
User
 │
 ▼
Streamlit Frontend
 │
 ▼
FastAPI Backend
 │
 ├── JWT Authentication
 ├── RBAC Middleware
 ├── Semantic Search
 │
 ▼
Vector Database (ChromaDB)
 │
 ▼
Retrieved Context
 │
 ▼
Groq LLaMA 3
 │
 ▼
Generated Response + Source Attribution
```

---

## 🛠️ Tech Stack

| Component       | Technology                               |
| --------------- | ---------------------------------------- |
| Language        | Python                                   |
| Backend         | FastAPI                                  |
| Frontend        | Streamlit                                |
| Authentication  | JWT (PyJWT)                              |
| Vector Database | ChromaDB                                 |
| Embeddings      | Sentence Transformers (all-MiniLM-L6-v2) |
| LLM             | Groq LLaMA 3                             |
| Database        | SQLite                                   |
| RAG Framework   | LangChain                                |
| Version Control | Git & GitHub                             |

---

## 👥 User Roles

| Role        | Access Level             |
| ----------- | ------------------------ |
| Employee    | General Company Policies |
| HR          | Employee Data + Policies |
| Finance     | Financial Reports        |
| Engineering | Technical Documents      |
| Marketing   | Marketing Reports        |
| C-Level     | Full Access              |

---

## 📂 Project Structure

```text
company-chatbot/
│
├── backend/
│   ├── routes/
│   ├── auth/
│   ├── llm/
│   ├── database.py
│   └── main.py
│
├── embeddings/
│   └── indexer.py
│
├── preprocessing/
│   ├── loader.py
│   ├── cleaner.py
│   ├── metadata.py
│   └── pipeline.py
│
├── search/
│   └── rbac.py
│
├── data/
│   └── Fintech-data/
│
├── frontend/
│   └── app.py
│
├── chroma_db/
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone <your-github-repository-url>
cd company-chatbot
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
```

---

## 📥 Data Indexing

Load and index company documents into the vector database.

```bash
python main.py
```

Expected Output:

```text
Total chunks: XXX
DB Created & Data Stored!
```

---

## 🚀 Running the Backend

Navigate to the backend directory:

```bash
cd backend
```

Start FastAPI:

```bash
uvicorn main:app --reload
```

Backend will run at:

```text
http://127.0.0.1:8000
```

Swagger API Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 💬 Running the Frontend

Open a new terminal and run:

```bash
streamlit run app.py
```

Frontend URL:

```text
http://localhost:8501
```

---

## 🔍 Sample Queries

### Finance

* What is the company revenue?
* What are the key financial ratios?
* Explain cash flow analysis.

### HR

* What is the leave policy?
* What are employee benefits?
* Show performance review process.

### Engineering

* Explain system architecture.
* What is the deployment pipeline?
* Describe caching strategy.

### Marketing

* What were the recent campaign results?
* Explain market analysis findings.

---

## 🔒 Security Features

* JWT Authentication
* Role-Based Access Control
* Protected API Endpoints
* Department-Level Data Access Restrictions
* Source Attribution for Transparency

---

## 📈 Future Improvements

* Conversation Memory
* Multi-turn Question Answering
* Advanced Document Ranking
* Hybrid Search (Keyword + Semantic)
* Admin Dashboard
* Deployment on AWS/Azure

---


