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
- [x] Add batch report logging (CSV with timing + word counts)  
- [x] Add CLI flags for `--pdf`, `--data-dir`, and `--timeout`

### In Progress
- [ ] Implement retry logic for unstable network connections  
- [ ] Add option to export all results to a single combined Markdown report  

### Future Enhancements
- [ ] Multi-PDF semantic search and cross-paper summaries  
- [ ] Richer metadata (citations, venues, year)  
- [ ] Evaluation metrics (ROUGE, BLEU)  

---

## 📖 Project Overview

**ResearchGPT Assistant** is an intelligent research automation tool designed to process academic papers, generate structured summaries and analyses, and organize all results automatically — ideal for students, researchers, and AI developers.

It demonstrates:
- **Python fundamentals**  
- **NLP preprocessing and vector search**  
- **LLM-powered summarization**  
- **Structured data export and reporting**

---

## ✨ Features

### Core Capabilities
- 🧩 **Document Processing:** Extract and process text from PDFs using PyMuPDF.  
- 🧠 **Intelligent Search:** TF-IDF similarity search retrieves most relevant text chunks.  
- 🗒 **Summarization:** Auto-generates summaries guided by a query or prompt file.  
- 🔍 **Analysis:** Produces deeper insights into methodology, contributions, and limitations.  
- 🧾 **Metadata Extraction:** Extracts title, authors, and abstract from PDFs into JSON.  
- 🧮 **Batch CSV Report:** Logs each processed paper with duration and word counts.  
- 🗂 **Prompt Library:** Flexible text prompts (contributions, limitations, ELI5, etc.).  

---

## 🧱 Project Structure

research_gpt_assistant/
├── notebooks/
│   └── quickstart.ipynb             # Interactive demo
│
├── data/
│   └── sample_papers/               # Place PDFs here
│
├── results/
│   ├── summaries/                   # Generated summaries (.md)
│   ├── analyses/                    # Generated analyses (.md)
│   ├── metadata/                    # Extracted metadata (.json)
│   └── batch_report.csv             # NEW: CSV summary report
│
├── prompts/                         # Custom prompt templates
│   ├── summarize_contributions.txt
│   ├── summarize_limitations.txt
│   └── explain_like_im_5.txt
│
├── src/
│   ├── pdf_utils.py
│   ├── text_utils.py
│   ├── indexer.py
│   ├── summarizer.py
│   ├── analyst.py
│   ├── io_utils.py
│   ├── metadata_utils.py
│   └── report_utils.py              # NEW: timing + CSV helpers
│
├── main.py                          # Entry point (CLI)
├── requirements.txt
└── README.md

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repo
git clone https://github.com/abe4x4/research-gpt-assistant.git
cd research-gpt-assistant

### 2️⃣ Create and Activate Virtual Environment
uv venv .venv
source .venv/bin/activate

### 3️⃣ Install Dependencies
uv pip install -r requirements.txt

### 4️⃣ Configure `.env` with Mistral API Key
Create a `.env` file in the project root:
MISTRAL_API_KEY=your_api_key_here

Load it into your environment:
export $(grep -v '^#' .env | xargs)

---

## ▶️ Usage Examples

### ✅ Default Run — Process All PDFs
python main.py

### 🧩 Specify Data Folder
python main.py --data-dir data/sample_papers

### 📄 Single PDF Processing
python main.py --pdf data/sample_papers/attention_is_all_you_need.pdf

### 🧠 Custom Query
python main.py --k 8 --query "Summarize contributions and limitations."

### ⏱ Timeout Control (default 45s)
python main.py --timeout 60

---

## 📊 New Feature — Batch Report CSV

Every batch run now creates:
results/batch_report.csv

Each row contains:
Timestamp | File Name | Title | Query | Summary File | Analysis File | Summary Words | Analysis Words | Duration (s)

Example:
2025-10-11 14:20:55,attention_is_all_you_need.pdf,Attention Is All You Need,What problem does this paper solve?,results/summaries/attention_is_all_you_need_summary.md,results/analyses/attention_is_all_you_need_analysis.md,412,367,11.92

---

## 📚 Prompt Library

Each `.txt` file in `/prompts/` can steer summarization:
- summarize_contributions.txt → Focus on novel findings  
- summarize_limitations.txt → Highlight weaknesses  
- explain_like_im_5.txt → Simplify technical concepts  

To use one:
python main.py --query "Summarize contributions only." \
  --prompt prompts/summarize_contributions.txt

---

## 🧠 Example Output

### JSON Metadata (results/metadata/attention_is_all_you_need_meta.json)
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

## 🧩 Troubleshooting

Q: Server disconnected without sending a response  
→ Check internet connection or reduce concurrency.

Q: MISTRAL_API_KEY missing  
→ Run `source .venv/bin/activate` then `export $(grep -v '^#' .env | xargs)` again.

Q: No PDFs found  
→ Ensure your `.pdf` files are inside `data/sample_papers/`.

---

## ✍️ Author
Ibrahim Abouzeid (@abe4x4)  
Blockchain & AI Developer | Neurophysiologist | Python Engineer  
Capstone Project — Code:You AI & Python Program

---

## 📅 Version History
Date | Version | Notes
-----|----------|-------
2025-10-02 | 1.0 | Initial release
2025-10-07 | 1.1 | Added Notebook + Metadata export
2025-10-11 | 1.2 | Added Batch CSV + Timeout flags + README upgrade
