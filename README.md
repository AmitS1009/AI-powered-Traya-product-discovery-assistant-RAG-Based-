# 🛍️ Neusearch AI - Product Discovery Assistant

![Home Page]

<img width="1901" height="864" alt="image" src="https://github.com/user-attachments/assets/799fe615-a80f-4a4c-b04a-34574132e165" />


Neusearch AI is a mini AI-powered product discovery assistant designed to help users find the right products using natural language queries. It combines a robust scraping pipeline, a FastAPI backend with vector search capabilities, and a modern React frontend to deliver a seamless user experience.

## 🚀 Features

-   **Semantic Search**: Understands abstract queries like "I have dry hair" and recommends relevant products.
-   **RAG Pipeline**: Uses Retrieval-Augmented Generation principles to interpret user intent and fetch the best matches.
-   **Modern UI**: A responsive, premium-feel interface built with React and Tailwind CSS.
-   **Automated Scraping**: Custom Python scraper to fetch real-time product data.
-   **Containerized**: Fully Dockerized for easy deployment.

---

## 🛠️ Tech Stack & Architecture

### **Frontend**
-   **Framework**: React (Vite)
-   **Styling**: Tailwind CSS v3 (Custom configuration for premium aesthetics)
-   **Routing**: React Router DOM

### **Backend**
-   **Framework**: FastAPI (High performance, easy async support)
-   **Database**: PostgreSQL (Structured data), ChromaDB (Vector embeddings)
-   **ORM**: SQLAlchemy
-   **ML/AI**: `sentence-transformers/all-MiniLM-L6-v2` for generating embeddings.

### **Data Pipeline**
-   **Scraper**: Python (`requests`, `BeautifulSoup`) with robust error handling and heuristic feature extraction.

---

## 🏃‍♂️ How to Run Locally

### Prerequisites
-   Docker & Docker Compose (Recommended)
-   **OR** Python 3.9+ and Node.js 16+

### Option 1: Using Docker (Easiest)
1.  Clone the repository.
2.  Run the following command:
    ```bash
    docker-compose up --build
    ```
3.  Access the application:
    -   Frontend: `http://localhost:3000`
    -   Backend API: `http://localhost:8000/docs`

### Option 2: Manual Setup

#### 1. Backend Setup
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt

# Set up Database (Update DATABASE_URL in app/database.py if needed)
# Run Data Ingestion & Vector Indexing
export PYTHONPATH=.
python ingest_data.py
python build_vector_db.py

# Start Server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Access the frontend at the URL shown in the terminal (usually `http://localhost:5173`).

---

## 🧠 RAG Pipeline Design

The core of the recommendation engine is a Retrieval-Augmented Generation (RAG) pipeline:

1.  **Ingestion**: Product data (Title, Description, Features) is concatenated into a single context string.
2.  **Embedding**: We use `sentence-transformers/all-MiniLM-L6-v2` to convert this text into 384-dimensional vectors.
3.  **Storage**: Vectors are stored in **ChromaDB**, a local vector database, alongside metadata (Price, Image URL).
4.  **Retrieval**:
    -   User query (e.g., "hair fall solution") is embedded using the same model.
    -   ChromaDB performs a similarity search (Cosine Similarity) to find the top `k` matches.
5.  **Response**: The system formats the retrieved results into a structured response for the frontend.

![Chat Response]

<img width="1917" height="865" alt="image" src="https://github.com/user-attachments/assets/3fb1ee30-cc3f-406a-81eb-1d573db35224" />

![Product Detail]

<img width="1919" height="866" alt="image" src="https://github.com/user-attachments/assets/48cca30a-551a-4c20-acb8-3aeebe177025" />
---

## 🕷️ Scraping Approach

The scraper (`data/scraper/scrape_traya.py`) is designed to be resilient and polite:

-   **Discovery**: It first crawls the "All Products" collection page to gather unique product URLs.
-   **Extraction**: It visits each product page to extract:
    -   **Title & Price**: Standard CSS selectors.
    -   **Features**: Uses heuristic patterns (bullet points, specific classes) to extract key benefits, falling back to description text if needed.
    -   **Images**: Prioritizes high-res images.
-   **Politeness**: Includes random delays between requests to avoid overwhelming the target server.

---

## ⚖️ Challenges & Trade-offs

1.  **Dynamic Content**: Some product details were hard to scrape due to inconsistent HTML structures across pages.
    -   *Trade-off*: Used a heuristic approach for "Features" which is robust but might miss some edge cases.
2.  **Vector DB Choice**: Chosen **ChromaDB** for simplicity and local development speed.
    -   *Trade-off*: For a massive scale (millions of products), a managed solution like Pinecone or Weaviate might be better.
3.  **LLM Integration**: Currently using a retrieval-based response generation.
    -   *Trade-off*: Fast and free, but lacks the conversational nuance of a full LLM (like GPT-4) generating custom advice.

---

## 🌟 Future Improvements

If I had more time, I would:

1.  **Integrate a Generative LLM**: Connect the retrieval output to OpenAI's GPT-4 or Gemini to generate personalized, empathetic advice explaining *why* a product is good for the user.
2.  **Hybrid Search**: Combine vector search with keyword search (BM25) to handle specific product name queries better.
3.  **User Personalization**: Store user preferences or quiz results to tailor recommendations further.
4.  **Production Deployment**: Set up a CI/CD pipeline to deploy to AWS (ECS for containers, RDS for DB).

---



