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

### In Progress
- [ ] Add `--pdf` flag to target a single PDF file
- [ ] Add `--data-dir` flag to scan custom folders

### Future Enhancements
- [ ] Multi-PDF semantic search and cross-paper summaries
- [ ] Richer metadata (citations, venues, year)
- [ ] Export results to CSV/JSONL
- [ ] Evaluation metrics (ROUGE, BLEU)

---

## 📖 Project Overview

ResearchGPT Assistant is an intelligent research tool that leverages advanced AI techniques to help researchers process academic documents, generate insights, and automate research workflows.  

This project is the **capstone project** and demonstrates the integration of:
- Python fundamentals  
- NLP preprocessing  
- Information retrieval  
- AI summarization  

---

## ✨ Features

### Core Capabilities
- **Document Processing**: Extract and process text from PDF research papers.
- **Intelligent Search**: TF-IDF based similarity search for relevant chunk retrieval.
- **Summarization**: Generate concise summaries of papers guided by user query or custom prompt file.
- **Analysis**: Deeper breakdowns of methodology, contributions, and limitations.
- **Metadata Extraction**: Save paper metadata (title, authors, abstract) into structured JSON.
- **Prompt Library**: Reusable prompt templates to control summarization style.
- **Research Automation**: End-to-end workflow from PDF → cleaned text → summaries, analyses, and metadata.

### Advanced Prompting Techniques
- **Custom Prompt Steering**: Use external text files (e.g., “Summarize contributions”, “Explain like I’m 5”).
- **Flexible Querying**: Override default queries with CLI arguments (`--query`).
- **Chunked Processing**: Clean and split papers into overlapping text chunks for retrieval-based summarization.

---

## 📂 Project Structure

research_gpt_assistant/
├── data/
│ └── sample_papers/ # Place your PDFs here
├── results/
│ ├── summaries/ # Generated summaries (.md)
│ ├── analyses/ # Generated analyses (.md)
│ └── metadata/ # Extracted metadata (.json)
├── prompts/ # Optional prompt steering files
│ ├── summarize_contributions.txt
│ ├── summarize_limitations.txt
│ └── explain_like_im_5.txt
├── src/ # Utility modules
│ ├── pdf_utils.py
│ ├── text_utils.py
│ ├── indexer.py
│ ├── summarizer.py
│ ├── analyst.py
│ ├── io_utils.py
│ └── metadata_utils.py
├── main.py # Entry point
├── requirements.txt
└── README.md

yaml
Copy code

---

## ⚙️ Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/abe4x4/research-gpt-assistant.git
   cd research-gpt-assistant
Create a virtual environment with uv

bash
Copy code
uv venv .venv
source .venv/bin/activate
Install dependencies

bash
Copy code
uv pip install -r requirements.txt
Configure your API key

Add to .env:

ini
Copy code
MISTRAL_API_KEY=your_api_key_here
Reload into shell:

bash
Copy code
export $(grep -v '^#' .env | xargs)
▶️ Usage Examples
Default run (process all PDFs in data/sample_papers/):

bash
Copy code
python main.py
Custom query & top-k retrieval:

bash
Copy code
python main.py --k 8 --query "Summarize contributions and limitations."
Use a custom prompt file:

bash
Copy code
python main.py --k 8 \
  --query "Summarize contributions only." \
  --prompt prompts/summarize_contributions.txt
Check outputs:

Summaries → results/summaries/

Analyses → results/analyses/

Metadata → results/metadata/

📊 Example Output
Metadata JSON (results/metadata/attention_is_all_you_need_meta.json)
json
Copy code
{
  "file": "attention_is_all_you_need.pdf",
  "pdf_path": "data/sample_papers/attention_is_all_you_need.pdf",
  "title": "Attention Is All You Need",
  "authors": "Unknown",
  "abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...",
  "query_used": "Summarize contributions and limitations.",
  "prompt_file": "prompts/summarize_contributions.txt",
  "outputs": {
    "summary_md": "results/summaries/attention_is_all_you_need_summary.md",
    "analysis_md": "results/analyses/attention_is_all_you_need_analysis.md"
  }
}
📚 Prompt Library
Examples of included prompt files:

summarize_contributions.txt: Focus only on novel contributions.

summarize_limitations.txt: Highlight weaknesses, assumptions, and limitations.

explain_like_im_5.txt: Explain the paper in simple terms.

Add your own .txt files inside prompts/ to extend the library.

✍️ Author
Built by Ibrahim Abouzeid (@abe4x4) as a capstone project for mastering Python, NLP, and AI-assisted research workflows.