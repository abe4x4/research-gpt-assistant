# ResearchGPT Assistant

Pipeline to parse PDFs, retrieve relevant chunks, and generate summaries + analyses via Mistral.

## Setup
```bash
uv venv --python 3.11 --seed --prompt research-gpt-assistant
source .venv/bin/activate
uv pip install -r requirements.txt
cp .env.example .env  # or: echo "MISTRAL_API_KEY=..." > .env
export $(grep -v "^#" .env | xargs -d "\n")
mkdir -p data/sample_papers
curl -L -o data/sample_papers/attention_is_all_you_need.pdf https://arxiv.org/pdf/1706.03762.pdf
python main.py --k 8 --query "Summarize contributions and limitations."
```
