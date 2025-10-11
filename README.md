An intelligent research assistant that reads academic PDFs, extracts metadata, summarizes them, and performs AI-based analysis of their methods, contributions, and limitations. This project represents an advanced stage of your AI/ML capstone, demonstrating integration of Python fundamentals, NLP, retrieval-based summarization, and automated research workflows.

✅ Capstone Progress Checklist
Completed

 Create GitHub repo and initialize project

 Set up virtual environment (uv venv .venv)

 Install dependencies (requirements.txt)

 Configure .env with MISTRAL_API_KEY and verify connectivity

 Add sample paper (attention_is_all_you_need.pdf)

 Implement PDF text extraction and cleaning

 Implement chunking + TF-IDF index + retrieval

 Summarization pipeline (guided by custom query)

 Analysis pipeline (contributions, limitations, etc.)

 Save summaries → results/summaries/

 Save analyses → results/analyses/

 Save per-paper metadata JSON → results/metadata/

 Add prompt library → prompts/

 Added fail-safe Mistral API retries + timeout flag

 Added CLI flags for --pdf, --data-dir, --k, --query, and --timeout

 Created and tested Jupyter Quickstart notebook (notebooks/quickstart.ipynb)

In Progress

 Implement multi-file batch summarization reporting

 Add --prompt flag for external prompt templates

 Improve error messages for malformed PDFs

Future Enhancements

 Multi-PDF semantic search & cross-paper summaries

 Metadata enrichment (citations, venue, year)

 Evaluation metrics (ROUGE, BLEU)

 Export results to CSV or JSONL

 Parallel PDF processing for speedup

📖 Overview

ResearchGPT Assistant automates the research paper review process:

Loads and cleans research PDFs

Extracts metadata (title, authors, abstract)

Chunks the text into analyzable segments

Runs retrieval-based summarization via Mistral API

Performs analytical breakdowns (methods, contributions, limitations)

Saves results (summaries, analyses, metadata)

It combines Python + NLP preprocessing + AI summarization + automation for a robust capstone demonstration.

✨ Features
Core Capabilities

Document Processing: Extracts text from academic PDFs.

TF-IDF Search: Retrieves the most relevant chunks for a given query.

AI Summarization: Generates context-rich summaries using Mistral models.

AI Analysis: Evaluates contributions, methods, and limitations.

Metadata Extraction: Extracts and saves structured metadata in JSON format.

Prompt Library: Enables custom steering (e.g. “Explain Like I’m 5”, “Summarize Contributions”).

Robust Networking: Automatic retries, clear logging, and user-settable timeouts.

Advanced Prompting & Retrieval

Custom Queries via --query

Top-K Chunk Retrieval via --k

Automatic Retry Logic with --timeout

Fail-fast Checks if MISTRAL_API_KEY is missing

End-to-end Automation from PDF → Text → Summary → Analysis → Metadata

📂 Project Structure

research_gpt_assistant/
├── data/
│ └── sample_papers/
│ └── attention_is_all_you_need.pdf
│
├── results/
│ ├── summaries/ # Markdown summaries
│ ├── analyses/ # Analytical breakdowns
│ └── metadata/ # JSON metadata outputs
│
├── prompts/ # Prompt steering library
│ ├── summarize_contributions.txt
│ ├── summarize_limitations.txt
│ └── explain_like_im_5.txt
│
├── notebooks/
│ └── quickstart.ipynb # Interactive demo notebook
│
├── src/ # Modular backend code
│ ├── pdf_utils.py
│ ├── text_utils.py
│ ├── indexer.py
│ ├── summarizer.py
│ ├── analyst.py
│ ├── io_utils.py
│ └── metadata_utils.py
│
├── main.py # CLI entry point (current version)
├── requirements.txt
└── README.md

⚙️ Setup Instructions
1. Clone the repository

git clone https://github.com/abe4x4/research-gpt-assistant.git

cd research-gpt-assistant

2. Create and activate the virtual environment

uv venv .venv
source .venv/bin/activate

3. Install dependencies

uv pip install -r requirements.txt

4. Configure the Mistral API key

Create a .env file in the project root:

MISTRAL_API_KEY=your_api_key_here

Reload into your shell:
export $(grep -v '^#' .env | xargs)

5. (Optional) Test API connectivity

python - <<'PY'
import os, requests
key = os.getenv("MISTRAL_API_KEY")
resp = requests.get("https://api.mistral.ai/v1/models
", headers={"Authorization": f"Bearer {key}"})
print(resp.status_code, resp.text[:200])
PY

Expected output:
200 {...list of available models...}

▶️ CLI Usage Examples
Default (process all PDFs in data/sample_papers)

python main.py

Process a single paper

python main.py --pdf data/sample_papers/attention_is_all_you_need.pdf

Custom query and top-k retrieval

python main.py --k 8 --query "Summarize contributions and limitations."

Custom timeout (e.g. 30 seconds per API call)

python main.py --pdf data/sample_papers/attention_is_all_you_need.pdf --timeout 30

Custom data directory

python main.py --data-dir /path/to/your/pdfs

📊 Example Outputs
Metadata JSON

results/metadata/attention_is_all_you_need_meta.json

{
"file": "attention_is_all_you_need.pdf",
"pdf_path": "data/sample_papers/attention_is_all_you_need.pdf",
"title": "Attention Is All You Need",
"authors": "Unknown",
"abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...",
"query_used": "Summarize contributions and limitations.",
"timeout": 45,
"outputs": {
"summary_md": "results/summaries/attention_is_all_you_need_summary.md",
"analysis_md": "results/analyses/attention_is_all_you_need_analysis.md"
}
}

🧩 Prompt Library
Prompt File	Description
summarize_contributions.txt	Focuses on novel ideas and core contributions
summarize_limitations.txt	Extracts limitations, assumptions, weaknesses
explain_like_im_5.txt	Simplifies technical content into plain language

You can add your own .txt prompt templates to extend the system.

🧠 Notebook: quickstart.ipynb

An interactive demonstration notebook that:

Loads sample papers

Shows metadata extraction

Displays first text chunks

Runs summarization and analysis

Shows resulting JSON output

Run it inside VS Code or JupyterLab for an educational walkthrough of the entire pipeline.

🧾 Logging & Error Handling

Auto Retries: Network errors automatically retry up to 3 times.

Timeouts: Each API call respects the user-set timeout (--timeout).

Fail-Fast: If MISTRAL_API_KEY is missing or invalid, execution stops immediately.

Progress Feedback: Console shows clear messages for each operation:
🧠 Summarizing...
🔍 Analyzing...
✅ Summary saved → results/summaries/...
✅ Analysis saved → results/analyses/...

✍️ Author

Ibrahim Abouzeid (@abe4x4)
Blockchain Developer • AI Research Engineer • Code:You Capstone Participant
Built as a guided exploration of AI, NLP, and automation best practices.

🧭 License

MIT License © 2025 Ibrahim Abouzeid
You are free to use, modify, and distribute with attribution.