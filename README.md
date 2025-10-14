ResearchGPT Assistant — Capstone Project

Capstone Progress Checklist
Completed
- Create GitHub repo and initialize project
- Set up virtual environment (uv venv .venv)
- Install dependencies from requirements.txt
- Configure .env with MISTRAL_API_KEY and test connectivity
- Add sample papers (attention_is_all_you_need.pdf, another_paper.pdf)
- Implement PDF text extraction and cleaning
- Implement chunking + TF-IDF index + retrieval
- Summarization pipeline (guided by query)
- Analysis pipeline (contributions, limitations, etc.)
- Save summaries (results/summaries/)
- Save analyses (results/analyses/)
- Save per-PDF metadata JSON (results/metadata/)
- Generate CSV report (results/batch_report.csv)
- Add prompt library (prompts/)
- Record prompt_file used in metadata JSON
- Add Jupyter notebook for testing (notebooks/quickstart.ipynb)
- Implement bonus paper comparison feature
- Implement demo runner script (demo_run.py)

Future Enhancements
- Multi-PDF semantic search and cross-paper summaries
- Richer metadata (citations, venues, year)
- Export results to CSV/JSONL/HTML
- Evaluation metrics (ROUGE, BLEU)
- Visual report generation (charts, graphs)
- Streamlit or web-based UI

Project Overview
ResearchGPT Assistant is an intelligent AI-powered research analysis tool that processes academic papers, extracts insights, and automates summarization workflows. It demonstrates a full end-to-end AI project pipeline built in Python for the Code:You Capstone Project.

Goals
- Streamline research paper summarization and analysis
- Build reusable NLP utilities for PDF text processing
- Showcase modular Python design and practical AI integration
- Exceed capstone requirements with bonus functionality

Features
Core Capabilities
- Document Processing: Extract and clean text from PDF research papers.
- Intelligent Search: TF-IDF based chunk retrieval for focused summaries.
- Summarization: Generate high-quality summaries using Mistral AI.
- Analysis: Provide structured breakdowns (methods, contributions, limitations).
- Metadata Extraction: Save structured metadata JSON for each paper.
- Batch Processing: Handle multiple PDFs at once with a CSV report.
- Prompt Library: Supports multiple prompt styles for different research tasks.

Advanced Prompting Techniques
- Chain-of-Thought Reasoning
- Self-Consistency and ReAct Workflows
- Verification and Editing Prompts
- Explain Like I’m 5 Mode
- Question-Answer Contextual Summaries

Project Structure
research_gpt_assistant/
├── data/
│   └── sample_papers/
│       ├── attention_is_all_you_need.pdf
│       └── another_paper.pdf
│
├── results/
│   ├── summaries/
│   ├── analyses/
│   ├── metadata/
│   ├── comparisons/
│   └── batch_report.csv
│
├── prompts/
│   ├── chain_of_thought.txt
│   ├── self_consistency.txt
│   ├── react_research.txt
│   ├── document_summary.txt
│   ├── qa_with_context.txt
│   ├── verify_answer.txt
│   ├── workflow_conclusion.txt
│   └── basic_qa.txt
│
├── src/
│   ├── pdf_utils.py
│   ├── text_utils.py
│   ├── indexer.py
│   ├── summarizer.py
│   ├── analyst.py
│   ├── io_utils.py
│   ├── metadata_utils.py
│   └── report_utils.py
│
├── notebooks/
│   └── quickstart.ipynb
│
├── main.py
├── demo_run.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md

Setup Instructions
1. Clone the repo
git clone https://github.com/abe4x4/research-gpt-assistant.git
cd research-gpt-assistant

2. Create and activate a virtual environment
uv venv .venv
source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Configure your API key
Create a .env file in the project root:
MISTRAL_API_KEY=your_api_key_here
Then reload:
export $(grep -v '^#' .env | xargs)

Usage Examples
Single PDF mode
python main.py --pdf data/sample_papers/attention_is_all_you_need.pdf

Batch processing mode
python main.py --data-dir data/sample_papers --report

Custom query
python main.py --pdf data/sample_papers/attention_is_all_you_need.pdf --query "Summarize contributions and limitations."

Bonus Feature: Paper Comparison
Compare two research papers directly using Mistral AI’s latest SDK:
python main.py --compare data/sample_papers/attention_is_all_you_need.pdf data/sample_papers/another_paper.pdf
Output:
A Markdown comparison file is created in:
results/comparisons/compare_attention_is_all_you_need_vs_another_paper.md

Project Demonstration (demo_run.py)
A single file to run all project stages automatically — perfect for presentation and grading.
Run the demo:
python demo_run.py
What it does:
1. Runs single-PDF summarization
2. Runs batch mode + generates CSV report
3. Runs the bonus comparison feature
4. Confirms all result files exist
Example output:
=== STEP 1: Single PDF Summarization & Analysis ===
✅ Summary → results/summaries/attention_is_all_you_need_summary.md
✅ Analysis → results/analyses/attention_is_all_you_need_analysis.md
=== STEP 2: Batch Mode with CSV Report ===
✅ batch_report.csv created
=== STEP 3: Bonus - Compare Two Papers ===
✅ Comparison saved to results/comparisons/...
=== STEP 4: Validate Outputs ===
✅ summaries/ → 1 files
✅ analyses/ → 1 files
✅ metadata/ → 1 files
✅ comparisons/ → 1 files
✅ CSV Report found
🎓 Demo completed successfully!

Example Output
Example metadata JSON (results/metadata/attention_is_all_you_need_meta.json):
{
  "file": "attention_is_all_you_need.pdf",
  "pdf_path": "data/sample_papers/attention_is_all_you_need.pdf",
  "title": "Attention Is All You Need",
  "authors": "Unknown",
  "abstract": "The dominant sequence transduction models...",
  "query_used": "Summarize contributions and limitations.",
  "outputs": {
    "summary_md": "results/summaries/attention_is_all_you_need_summary.md",
    "analysis_md": "results/analyses/attention_is_all_you_need_analysis.md"
  }
}

Prompt Library Overview
Each file in prompts/ defines a reusable research assistant template:
chain_of_thought.txt — step-by-step reasoning
self_consistency.txt — alternate perspectives
react_research.txt — reasoning with Thought-Action-Observation
document_summary.txt — full structured summary
qa_with_context.txt — contextual Q&A
verify_answer.txt — validate AI output
workflow_conclusion.txt — determine sufficiency
basic_qa.txt — minimal query-response
These templates enable flexible AI behavior for different research goals.

Author
Ibrahim Abouzeid (@abe4x4)
Built as part of the Code:You AI Developer Program Capstone Project.
Demonstrates advanced Python, NLP, and AI workflow automation.

Notes
This version uses the new mistralai SDK (v1.9+) with modern Mistral() client.
Older versions (MistralClient) are deprecated.
This project:
- Exceeds minimum capstone requirements
- Demonstrates clean modular design
- Supports bonus research comparison
- Includes automated testing and reporting
