# Clone your project
git clone <your-repo>
cd project-root

# Install dependencies
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# For GPU acceleration with your RTX 4060, install these separately:
pip install llama-cpp-python --prefer-binary --extra-index-url=https://jllllll.github.io/llama-cpp-python-cuBLAS-wheels/AVX2/cu118

# Set up Ollama (if not installed)
# Follow instructions from https://ollama.ai/download
ollama pull qwen3:8b

# Ingest documents (optional):
python ingest.py

# Start FastAPI server:
uvicorn app.main:app --reload --port 8000

# Test with curl:
# For PDF files
curl -X POST "http://localhost:8000/api/v1/ingest/pdf" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/file.pdf"

# For text files
curl -X POST "http://localhost:8000/api/v1/ingest/text" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/file.txt"

# For Querying
curl -X POST "http://localhost:8000/api/v1/ask" \
-H "Content-Type: application/json" \
-d '{"question": "What is Task Decomposition?"}'

# For production, you should add:
Authentication/authorization
Rate limiting
File size restrictions
Proper error logging
Input validation for file types