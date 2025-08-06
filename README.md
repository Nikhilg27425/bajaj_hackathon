# Document Q&A API

A FastAPI-based application that parses documents and answers questions using AI. This API replicates the functionality of the Streamlit app but provides RESTful endpoints for integration.

## Features

- 📄 Document parsing (PDF, DOCX, TXT)
- 🤖 AI-powered question answering using Groq LLM
- 🔍 Vector-based document retrieval
- 📊 Structured JSON responses
- 🚀 FastAPI with automatic API documentation
- 🐳 Docker containerization
- 🔒 CORS support for web applications

## API Endpoints

### 1. Health Check
```
GET /
```
Returns API status and health information.

### 2. Main Q&A Endpoint
```
POST /hackrx/run
```
Main endpoint for answering questions about documents via URL.

**Request Body:**
```json
{
  "documents": "https://example.com/document.pdf",
  "questions": [
    "What is the grace period for premium payment?",
    "What is the waiting period for pre-existing diseases?",
    "Does this policy cover maternity expenses?"
  ]
}
```

**Response:**
```json
{
  "answers": [
    "A grace period of thirty days is provided for premium payment...",
    "There is a waiting period of thirty-six (36) months...",
    "Yes, the policy covers maternity expenses..."
  ]
}
```

### 3. File Upload Endpoint
```
POST /upload-and-ask
```
Alternative endpoint for uploading files and asking questions.

**Form Data:**
- `files`: Multiple file uploads (PDF, DOCX, TXT)
- `questions`: JSON array or comma-separated questions

## Quick Start

### Prerequisites
- Python 3.11+
- Docker (optional)
- Groq API key

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd bajaj
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GROQ_API_KEY=your_groq_api_key_here" > .env
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the API**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Or build and run manually**
   ```bash
   docker build -t document-qa-api .
   docker run -p 8000:8000 -e GROQ_API_KEY=your_key document-qa-api
   ```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Groq API key for LLM access | Required |
| `DEFAULT_MODEL` | Default LLM model | `llama3-70b-8192` |
| `DEFAULT_TEMPERATURE` | Model creativity | `0.5` |
| `DEFAULT_MAX_TOKENS` | Max response length | `3072` |

## API Usage Examples

### Using curl

```bash
# Health check
curl http://localhost:8000/

# Q&A with document URL
curl -X POST "http://localhost:8000/hackrx/run" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_token_here" \
  -d '{
    "documents": "https://example.com/policy.pdf",
    "questions": [
      "What is the grace period for premium payment?",
      "What is the waiting period for pre-existing diseases?"
    ]
  }'

# File upload
curl -X POST "http://localhost:8000/upload-and-ask" \
  -F "files=@document.pdf" \
  -F "questions=[\"What is the main topic?\", \"What are the key points?\"]"
```

### Using Python

```python
import requests

# Q&A request
url = "http://localhost:8000/hackrx/run"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer your_token_here"
}
data = {
    "documents": "https://example.com/policy.pdf",
    "questions": [
        "What is the grace period for premium payment?",
        "What is the waiting period for pre-existing diseases?"
    ]
}

response = requests.post(url, json=data, headers=headers)
answers = response.json()["answers"]
print(answers)
```

## Deployment Options

### 1. Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### 2. Render
- Connect your GitHub repository
- Set environment variables
- Deploy automatically

### 3. Heroku
```bash
# Create Procfile
echo "web: uvicorn app:app --host=0.0.0.0 --port=\$PORT" > Procfile

# Deploy
heroku create your-app-name
heroku config:set GROQ_API_KEY=your_key
git push heroku main
```

### 4. AWS/GCP/Azure
- Use the Dockerfile for container deployment
- Set up environment variables
- Configure load balancer and auto-scaling

## Architecture

The application follows a modular architecture:

```
app.py
├── FastAPI Application
├── Document Processing
│   ├── PDF/DOCX/TXT Loaders
│   ├── Text Chunking
│   └── Vector Embeddings
├── AI Processing
│   ├── Groq LLM Integration
│   ├── Prompt Templates
│   └── Retrieval Chains
└── API Endpoints
    ├── Health Check
    ├── Q&A with URL
    └── File Upload
```

## Performance Optimization

- **Caching**: Implement Redis for response caching
- **Async Processing**: Use background tasks for long-running operations
- **Load Balancing**: Deploy multiple instances behind a load balancer
- **Database**: Add PostgreSQL for storing processed documents and responses

## Security Considerations

- ✅ Input validation with Pydantic
- ✅ CORS configuration
- ✅ Environment variable management
- ✅ Non-root Docker user
- ⚠️ Add rate limiting
- ⚠️ Implement authentication/authorization
- ⚠️ Add request logging and monitoring

## Monitoring and Logging

Add these for production:

```python
import logging
from fastapi import Request
import time

# Add to app.py
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logging.info(f"{request.method} {request.url} - {response.status_code} - {process_time:.2f}s")
    return response
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details. 