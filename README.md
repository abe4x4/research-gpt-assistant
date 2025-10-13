# 🧠 ResearchGPT Assistant

## 📘 Project Overview

ResearchGPT Assistant is an intelligent research tool that leverages advanced AI techniques to help researchers process academic documents, generate insights, and automate research workflows.

This project is the **capstone project** and demonstrates the integration of:
- Python fundamentals
- NLP preprocessing
- Information retrieval
- AI summarization
- Research automation

---

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
- [x] Implement batch report CSV logging
- [x] Add timeout flag and error handling for API calls

### In Progress
- [ ] Improve interactive notebook visualizations
- [ ] Add multi-PDF semantic search demo in notebook

### Future Enhancements
- [ ] Richer metadata (citations, venues, year)
- [ ] Export results to CSV/JSONL
- [ ] Evaluation metrics (ROUGE, BLEU)
- [ ] Add frontend visualization for batch report

---

## ✨ Features

### Core Capabilities
- **Document Processing**: Extract and process text from PDF research papers.
- **Intelligent Search**: TF-IDF based similarity search for relevant chunk retrieval.
- **Summarization**: Generate concise summaries guided by custom prompts or queries.
- **Analysis**: Deeper breakdowns of methodology, contributions, and limitations.
- **Metadata Extraction**: Save paper metadata (title, authors, abstract) into structured JSON.
- **Prompt Library**: Reusable templates for research reasoning and QA.
- **Batch Reporting**: Generate per-run CSV summaries of all processed PDFs.
- **Timeout Handling**: Graceful termination when network/API stalls.

---

## 📂 Project Structure

research_gpt_assistant/
├── notebooks/
│   └── quickstart.ipynb
├── data/
│   └── sample_papers/
├── results/
│   ├── summaries/
│   ├── analyses/
│   ├── metadata/
│   └── batch_report.csv
├── prompts/
│   ├── basic_qa.txt
│   ├── chain_of_thought.txt
│   ├── document_summary.txt
│   ├── qa_with_context.txt
│   ├── react_research.txt
│   ├── self_consistency.txt
│   ├── verify_answer.txt
│   ├── workflow_conclusion.txt
│   ├── summarize_contributions.txt
│   ├── summarize_limitations.txt
│   ├── explain_like_im_5.txt
│   └── system.md
├── src/
│   ├── pdf_utils.py
│   ├── text_utils.py
│   ├── indexer.py
│   ├── summarizer.py
│   ├── analyst.py
│   ├── io_utils.py
│   ├── metadata_utils.py
│   └── report_utils.py
├── main.py
├── requirements.txt
└── README.md

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repo
git clone https://github.com/abe4x4/research-gpt-assistant.git
cd research-gpt-assistant

### 2️⃣ Create virtual environment
uv venv .venv
source .venv/bin/activate

### 3️⃣ Install dependencies
uv pip install -r requirements.txt

### 4️⃣ Configure your API key
Create `.env` file:
MISTRAL_API_KEY=your_api_key_here

Then load it:
export $(grep -v '^#' .env | xargs)

### 5️⃣ Test connectivity
python - <<'PY'
import os, requests
key = os.getenv("MISTRAL_API_KEY")
resp = requests.get("https://api.mistral.ai/v1/models", headers={"Authorization": f"Bearer {key}"})
print(resp.status_code, resp.text[:200])
PY

✅ You should see a `200` response.

---

## ▶️ Usage Examples

### Process a single PDF
python main.py --pdf data/sample_papers/attention_is_all_you_need.pdf

### Process all PDFs in folder
python main.py --data-dir data/sample_papers

### Add custom query
python main.py --data-dir data/sample_papers --query "Summarize contributions and limitations"

### Use a specific prompt file
python main.py --data-dir data/sample_papers --prompt prompts/chain_of_thought.txt

### Generate batch report CSV
python main.py --data-dir data/sample_papers --report

### Adjust API timeout
python main.py --data-dir data/sample_papers --timeout 60

---

## 📊 Example Output

Metadata JSON (`results/metadata/attention_is_all_you_need_meta.json`):
{
  "file": "attention_is_all_you_need.pdf",
  "pdf_path": "data/sample_papers/attention_is_all_you_need.pdf",
  "title": "Attention Is All You Need",
  "authors": "Vaswani et al.",
  "abstract": "The dominant sequence transduction models...",
  "query_used": "Summarize contributions and limitations.",
  "prompt_file": "prompts/chain_of_thought.txt",
  "outputs": {
    "summary_md": "results/summaries/attention_is_all_you_need_summary.md",
    "analysis_md": "results/analyses/attention_is_all_you_need_analysis.md"
  }
}

Batch Report (`results/batch_report.csv`):
timestamp,file,query_used,summary_path,analysis_path,duration_sec
2025-10-11T16:12:06,attention_is_all_you_need.pdf,Summarize contributions and limitations.,results/summaries/attention_is_all_you_need_summary.md,results/analyses/attention_is_all_you_need_analysis.md,11.46

---

## 📚 Prompt Library

The ResearchGPT Assistant includes a library of reusable prompt templates used to control summarization, analysis, reasoning, and research workflow behavior.

### 🟢 Basic Prompts (Original Set)
summarize_contributions.txt → Focus on key contributions of the paper  
summarize_limitations.txt → Highlight weaknesses or assumptions  
explain_like_im_5.txt → Simplify technical content for general audiences  

### 🔵 Advanced Mentor-Style Prompts (Extended Set)
chain_of_thought.txt → Step-by-step logical reasoning for complex questions  
self_consistency.txt → Encourages alternative reasoning paths for diversity  
react_research.txt → Uses the “Thought → Action → Observation” reasoning loop  
document_summary.txt → Produces structured summaries with key sections  
qa_with_context.txt → Context-based research question answering  
verify_answer.txt → Quality control: evaluates answer accuracy and completeness  
basic_qa.txt → Simple contextual question-answer prompt  
workflow_conclusion.txt → Determines if the research workflow has sufficient information  

### 🧠 Internal Prompt
system.md → Internal system prompt for maintaining consistent AI behavior  

These templates are automatically discovered from the `prompts/` directory at runtime and can be customized without modifying the codebase.

---

## 🧩 Developer Notes

- `main.py` supports both single and batch PDF processing.
- All results are saved in timestamped subfolders for traceability.
- Batch report generation ensures reproducibility for large-scale testing.
- Jupyter notebook (`quickstart.ipynb`) demonstrates full pipeline step-by-step.

---

## ✍️ Author

Built by **Ibrahim Abouzeid (@abe4x4)**  
As a capstone project to master **Python**, **NLP**, and **AI-assisted research workflows**.

---
