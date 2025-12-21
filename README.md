# 📄 AI-Powered CV Analyzer

An AI-powered web application that analyzes PDF resumes and evaluates candidates objectively against a given job description.

The system extracts text from uploaded CVs, evaluates professional experience, skills, education, and overall fit for a specific role, and generates a structured hiring recommendation using Large Language Models.

---

## 🚀 Features

- Upload and analyze CVs in PDF format
- Extract text from resumes (text-based PDFs)
- Compare candidate profiles against job descriptions
- Objective scoring (0–100% fit)
- Structured evaluation:
  - Candidate name
  - Years of experience
  - Education
  - Key technical skills
  - Strengths and improvement areas
- Interactive UI built with Streamlit

---

## 🧰 Tech Stack

- **Python**
- **Streamlit** – Web UI
- **LangChain** – Prompt orchestration and LLM integration
- **OpenAI API** – LLM-powered analysis
- **Pydantic** – Structured output validation
- **PyPDF2** – PDF text extraction
- **uv** – Fast Python dependency manager
- **Docker & Docker Compose** – Containerized deployment

---

## 🔐 Environment Variables

The app requires an OpenAI-compatible API key.

Create a `.env` file in the project root with:

```bash
API_KEY=your_api_key_here
```
---

## 🧑‍💻 Run Locally (without Docker, using `uv`)

This option is recommended for local development.

### 1️⃣ Install `uv` (if you don’t have it)

Using **Git Bash**, Linux, or macOS:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Restart your terminal after installation.

### 2️⃣ Install dependencies

```bash
uv sync
```

### 3️⃣ Set environment variables

Ensure your `.env` file exists and contains your API key.

### 4️⃣ Run the app

```bash
uv run streamlit run app.py
```

Then open:

👉 http://localhost:8501

---

## 🐳 Run with Docker (Recommended)

### 1️⃣ Build the image

```bash
docker compose build
```

### 2️⃣ Start the container

```bash
docker compose up -d
```

Then open:

👉 http://localhost:8501

### 3️⃣ Stop the container

```bash
docker compose down
```

### 🔁 Rebuild After Code Changes

If you modify any Python file, prompt, or dependency:

```bash
docker compose build
docker compose up -d
```

### 📌 Notes & Limitations

- The PDF must contain selectable text (scanned/image-only PDFs are not supported).

- The evaluation is fully based on the content found in the CV.

- If key information is missing, the model makes reasonable assumptions and reflects them in the output.