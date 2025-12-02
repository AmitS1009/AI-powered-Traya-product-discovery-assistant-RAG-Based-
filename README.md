# 🛍️ Neusearch AI - The Intelligent Product Discovery Assistant

![Home Page](screenshots/home_page.png)

> **"Search shouldn't just match keywords; it should understand intent."**

Neusearch AI is a next-generation e-commerce assistant that bridges the gap between what users *say* ("I have dry hair") and what they *need* (Hydrating Shampoo). Built with a modern RAG (Retrieval-Augmented Generation) pipeline, it delivers semantic product recommendations in milliseconds.

---

## 🚀 Features

-   **🧠 Semantic Understanding**: Uses `sentence-transformers` to encode user queries and find products based on meaning, not just keywords.
-   **💬 AI-Powered Chat**: A conversational interface that feels like talking to a knowledgeable sales associate.
-   **🎨 Premium UI/UX**: A responsive, aesthetically pleasing interface built with **React** and **Tailwind CSS v3**.
-   **⚡ Real-Time Data**: Custom Python scraper fetches live product data (Title, Price, Features) from the web.
-   **🐳 Production Ready**: Fully containerized with **Docker** and **Docker Compose**.

---

## 🛠️ Tech Stack

| Component | Technology | Why? |
| :--- | :--- | :--- |
| **Frontend** | React + Vite | Blazing fast HMR and component-based architecture. |
| **Styling** | Tailwind CSS | Utility-first CSS for rapid, consistent UI development. |
| **Backend** | FastAPI | High-performance, async Python framework perfect for ML apps. |
| **Database** | PostgreSQL | Robust relational storage for product metadata. |
| **Vector DB** | ChromaDB | Efficient local vector storage for semantic search. |
| **ML Model** | `all-MiniLM-L6-v2` | Lightweight, high-speed embedding model. |

---

## 🏗️ Architecture

```mermaid
graph TD
    User[User Query] -->|POST /chat| API[FastAPI Backend]
    API -->|Encode Query| Model[Embedding Model]
    Model -->|Vector| Chroma[ChromaDB]
    Chroma -->|Top K Matches| API
    API -->|Format Response| Frontend[React UI]
    Scraper[Python Scraper] -->|Raw Data| Postgres[PostgreSQL]
    Postgres -->|Sync| Chroma
```

---

## 🔧 Engineering Journey & Debugging Highlights

Building robust software is rarely a straight line. Here are some of the technical hurdles I overcame to build Neusearch AI:

### 1. The "Invisible" Environment Variables (Windows Encoding)
**The Challenge:** The backend refused to start, claiming `DATABASE_URL` was `None`, even though the `.env` file existed.
**The Investigation:**
-   I added debug prints to `database.py` and discovered the file path was resolving correctly.
-   However, `python-dotenv` failed to parse it.
-   **The Culprit:** PowerShell created the `.env` file with a specific encoding (UTF-16 LE BOM) that Python's standard reader choked on, causing a `UnicodeDecodeError`.
**The Fix:** I wrote a Python script to explicitly rewrite the `.env` file with `utf-8` encoding, ensuring cross-platform compatibility.

### 2. The CORS Labyrinth
**The Challenge:** The frontend (port 5173) couldn't talk to the backend (port 8000).
**The Fix:** I implemented a robust `CORSMiddleware` configuration in FastAPI, explicitly allowlisting development ports (`5173`, `5174`, `5175`) while preparing for a stricter production setup.

### 3. Tailwind CSS Build Pipeline
**The Challenge:** Styles were not applying, leaving the app looking "broken."
**The Fix:** I diagnosed a mismatch between the PostCSS configuration and Tailwind v3. I reset the `postcss.config.js` and correctly configured the `content` paths in `tailwind.config.js` to scan all React components.

---

## 🔮 Future Roadmap

If I had more time, here is where I would take Neusearch AI next:

-   **🔐 User Authentication**: Implement JWT-based login to save user preferences and chat history.
-   **🧠 LLM Integration**: Replace the template-based response with a real LLM (GPT-4 or Gemini) to generate empathetic, personalized advice explaining *why* a product was recommended.
-   **🛒 Cart Functionality**: Allow users to add products directly to a cart from the chat interface.
-   **☁️ Cloud Deployment**: Deploy the Docker containers to AWS ECS or Render for global accessibility.

---

## 🏃‍♂️ How to Run Locally

### Prerequisites
-   Docker & Docker Compose

### Quick Start
1.  **Clone the repo**
2.  **Setup Environment**:
    Ensure you have a `.env` file in the root directory:
    ```env
    DATABASE_URL=postgresql://user:pass@host/db
    ```
3.  **Run with Docker**:
    ```bash
    docker-compose up --build
    ```
4.  **Access the App**:
    -   Frontend: `http://localhost:3000`
    -   Backend Docs: `http://localhost:8000/docs`

---

*Built by AMIT KUSHWAHA*
