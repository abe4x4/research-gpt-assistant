# 🧠 ResearchGPT Assistant

## ✅ Capstone Progress Checklist

### Completed
- [x] Create GitHub repo and initialize project
- [x] Set up virtual environment (`uv venv .venv`)
- [x] Install dependencies from `requirements.txt`
- [x] Configure `.env` with `MISTRAL_API_KEY` and test connectivity
- [x] Add sample paper (`attention_is_all_you_need.pdf`)
- [x] Implement PDF text extraction and cleaning
- [x] Implement chunking + TF-IDF index + retrieval
- [x] Summarization pipeline (guided by query)
- [x] Analysis pipeline (contributions, limitations, etc.)
- [x] Save summaries (`results/summaries/`)
- [x] Save analyses (`results/analyses/`)
- [x] Save per-PDF metadata JSON (`results/metadata/`)
- [x] Add prompt library (`prompts/`)
- [x] Record `prompt_file` used in metadata JSON
- [x] Add `--timeout` flag for API stability
- [x] Add CSV batch reporting (`--report`)
- [x] Add Jupyter Notebook dashboard (Quickstart demo)

### In Progress
- [ ] Add `--pdf` flag to target a single file (enhanced)
- [ ] Add `--data-dir` flag for custom folders (batch mode improvements)

### Future Enhancements
- [ ] Multi-PDF semantic search and cross-paper summaries
- [ ] Richer metadata (citations, year, venue)
- [ ] Export results to CSV/JSONL with summary stats
- [ ] Evaluation metrics (ROUGE, BLEU, cosine similarity)

---

## 📖 Project Overview

ResearchGPT Assistant is an intelligent research automation tool that processes academic papers, extracts key insights, and produces structured summaries and analyses — all powered by the Mistral API and modern NLP techniques.

This capstone project demonstrates:
- Python fundamentals  
- NLP preprocessing  
- Information retrieval (TF-IDF search)  
- LLM-powered summarization and analysis  
- Structured metadata and CSV reporting

---

## ✨ Features

### Core Capabilities
- Document Processing: Extract and clean text from PDFs  
- Chunking & Indexing: Split documents into searchable text chunks using TF-IDF retrieval  
- Summarization: Generate concise paper summaries guided by user queries or prompt files  
- Analysis: Deep breakdown of contributions, methods, and limitations  
- Metadata Extraction: Structured output (title, authors, abstract) in JSON format  
- Prompt Library: Reusable prompt templates in `/prompts`  
- Batch Reporting: Optional CSV summary of all runs  
- Timeout Handling: Safe API execution with user-defined timeout

### Advanced Prompting
- Use text files like `prompts/summarize_contributions.txt` or `prompts/explain_like_im_5.txt`  
- Control summary style directly from the CLI  
- Combine with custom queries for precise control

---

## 📂 Project Structure

research_gpt_assistant/
├── notebooks/
│   └── quickstart.ipynb        ← Interactive demo notebook
├── data/
│   └── sample_papers/          ← Place your PDFs here
├── results/
│   ├── summaries/              ← Generated summaries (.md)
│   ├── analyses/               ← Generated analyses (.md)
│   ├── metadata/               ← Per-PDF metadata (.json)
│   └── batch_report.csv        ← Optional batch summary (CSV)
├── prompts/
│   ├── summarize_contributions.txt
│   ├── summarize_limitations.txt
│   └── explain_like_im_5.txt
├── src/
│   ├── pdf_utils.py
│   ├── text_utils.py
│   ├── indexer.py
│   ├── summarizer.py
│   ├── analyst.py
│   ├── io_utils.py
│   ├── metadata_utils.py
│   └── report_utils.py         ← NEW: CSV report utilities
├── main.py                     ← Main entry point
├── requirements.txt
└── README.md

---

## ⚙️ Setup Instructions

1️⃣ Clone the Repository  
git clone https://github.com/abe4x4/research-gpt-assistant.git  
cd research-gpt-assistant

2️⃣ Create and Activate Virtual Environment  
uv venv .venv  
source .venv/bin/activate

3️⃣ Install Dependencies  
uv pip install -r requirements.txt

4️⃣ Configure API Key  
Create a `.env` file in the project root:  
MISTRAL_API_KEY=your_api_key_here  

Load it into your shell:  
export $(grep -v '^#' .env | xargs)

Test Connectivity:  
python - <<'PY'
import os, requests
key = os.getenv("MISTRAL_API_KEY")
resp = requests.get("https://api.mistral.ai/v1/models", headers={"Authorization": f"Bearer {key}"})
print(resp.status_code, resp.text[:200])
PY

---

## ▶️ Usage Examples

Process All PDFs (Default):  
python main.py  

Custom Query and Top-K Retrieval:  
python main.py --k 8 --query "Summarize contributions and limitations."

Process a Single PDF:  
python main.py --pdf data/sample_papers/attention_is_all_you_need.pdf  

Add Timeout (in seconds):  
python main.py --timeout 120  

Generate CSV Batch Report:  
python main.py --data-dir data/sample_papers --report  

Output File:  
results/batch_report.csv

---

## 📊 Example Output

Metadata JSON (results/metadata/attention_is_all_you_need_meta.json):  
{
  "file": "attention_is_all_you_need.pdf",
  "pdf_path": "data/sample_papers/attention_is_all_you_need.pdf",
  "title": "Attention Is All You Need",
  "authors": "Unknown",
  "abstract": "The dominant sequence transduction models are based on complex recurrent...",
  "query_used": "Summarize contributions and limitations.",
  "outputs": {
    "summary_md": "results/summaries/attention_is_all_you_need_summary.md",
    "analysis_md": "results/analyses/attention_is_all_you_need_analysis.md"
  }
}

---

## 📗 Quickstart Notebook Demo

Open `notebooks/quickstart.ipynb` to visualize your full workflow interactively.

Steps:
1. Load a sample PDF  
2. Extract metadata and clean text  
3. Chunk and index content  
4. Run summarization and analysis  
5. Generate metadata JSON  
6. View CSV report dashboard  
7. Review summary insights cell  

Example Output:
✅ Batch Report Loaded Successfully!

📊 Summary Insights:
Total PDFs processed: 1  
Average runtime: 11.46 seconds  
Fastest run: 11.46 seconds  
Slowest run: 11.46 seconds

---

## 📚 Prompt Library

- summarize_contributions.txt → Focus on novel contributions  
- summarize_limitations.txt → Highlight weaknesses and limitations  
- explain_like_im_5.txt → Explain in simple terms  

You can create your own `.txt` prompts in the `/prompts` folder and reference them via CLI.

---

## 🧾 CSV Report Fields

| Column | Description |
|--------|--------------|
| Timestamp | Run time (ISO format) |
| File Name | PDF processed |
| Title | Extracted title |
| Query Used | User query |
| Summary File / Analysis File | Output paths |
| Word Counts | Approximate word count |
| Duration (s) | Total processing time |

---

## ✍️ Author

Built by Ibrahim Abouzeid (@abe4x4)  
Capstone project demonstrating Python, NLP, and AI-assisted research automation.

---

## 🏁 Final Notes

✔️ Full summarization and analysis pipeline  
✔️ Batch CSV reporting and dashboard visualization  
✔️ Ready for grading and extension  
✔️ Compatible with any academic PDF using TF-IDF + Mistral API

🏁 Final Capstone Submission Summary

The ResearchGPT Assistant project demonstrates a complete end-to-end AI research pipeline built in Python. It automates the process of analyzing academic papers by extracting text from PDFs, cleaning and chunking content, retrieving relevant sections via TF-IDF search, and generating AI-powered summaries and analytical insights using the Mistral API.

This project showcases key technical competencies including:

Advanced Python scripting and modular design (src/ package structure)

Environment management (uv venv, .env, direnv)

PDF parsing, text preprocessing, and metadata extraction

TF-IDF indexing, semantic retrieval, and prompt-based summarization

AI integration via the Mistral LLM API

CSV batch reporting, metadata tracking, and notebook-based analytics (quickstart.ipynb)

Testing and validation were completed successfully:
✅ End-to-end run via python main.py --pdf ...
✅ Batch processing with reporting (--data-dir ... --report)
✅ Jupyter notebook walkthrough with clean execution
✅ Results stored under results/summaries/, analyses/, and metadata/
✅ Verified runtime tracking and correct CSV export

This final version (v1.0) is fully functional, reproducible, and submission-ready, representing a complete AI-assisted research analysis pipeline built from scratch and verified through real API interaction and notebook visualization.
