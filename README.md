# ResearchGPT Assistant – Capstone Project

An intelligent research tool that processes academic papers, generates summaries, analyses, and metadata, and supports advanced prompting and retrieval.

---

## 📋 Project Plan & Status

**Owner:** Ibrahim (abe4x4)  
**Repo:** `research-gpt-assistant`

### ✅ Completed
- [x] Create project structure (`data/`, `results/`, `prompts/`)
- [x] Create and activate virtual environment with `uv`
- [x] Install requirements from `requirements.txt`
- [x] Configure `.env` with `MISTRAL_API_KEY`
- [x] Verify Mistral API via `test_mistral.py`
- [x] Add sample PDF (`attention_is_all_you_need.pdf`)
- [x] Implement PDF → text chunks → **summary** (`results/summaries/*.md`)
- [x] Implement analysis output (methods, key results, limitations) (`results/analyses/*.md`)
- [x] Push repo to GitHub (`abe4x4/research-gpt-assistant`)

### 🚧 In Progress
- [ ] Improve metadata extraction (title, authors, abstract) and save standalone **metadata JSON** (`results/metadata/*.json`)

### 🔜 Next Up
- [ ] Prompt library in `prompts/` (contributions / limitations / explain-like-I’m-5)
- [ ] TF-IDF search across multiple PDFs
- [ ] CLI options: `--pdf <path>`, `--out <dir>`, `--model <id>`
- [ ] Export consolidated `results/index.json` (title, authors, abstract, files)
- [ ] README polish with screenshots of outputs

---

## 🧪 How to Run (Quick)

```bash
# Activate environment
source .venv/bin/activate

# Install dependencies (if needed)
uv pip install -r requirements.txt

# Run with query
RGPT_TOP_K=8 RGPT_QUERY="Summarize contributions and limitations." python main.py
