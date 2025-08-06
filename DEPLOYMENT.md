# Quick Deployment Guide

## 🚀 Fast Deployment Options

### Option 1: Railway (Recommended - Free Tier Available)

1. **Fork/Clone this repository to GitHub**
2. **Go to [Railway](https://railway.app/)**
3. **Connect your GitHub account**
4. **Create new project from GitHub repo**
5. **Add environment variable:**
   - Key: `GROQ_API_KEY`
   - Value: Your Groq API key
6. **Deploy automatically**

### Option 2: Render (Free Tier Available)

1. **Fork/Clone this repository to GitHub**
2. **Go to [Render](https://render.com/)**
3. **Create new Web Service**
4. **Connect your GitHub repository**
5. **Configure:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
6. **Add environment variable:**
   - Key: `GROQ_API_KEY`
   - Value: Your Groq API key
7. **Deploy**

### Option 3: Heroku

1. **Install Heroku CLI**
2. **Login to Heroku:**
   ```bash
   heroku login
   ```
3. **Create app:**
   ```bash
   heroku create your-app-name
   ```
4. **Set environment variable:**
   ```bash
   heroku config:set GROQ_API_KEY=your_groq_api_key
   ```
5. **Deploy:**
   ```bash
   git push heroku main
   ```

### Option 4: Local Development

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd bajaj
   ```

2. **Create .env file:**
   ```bash
   echo "GROQ_API_KEY=your_groq_api_key_here" > .env
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the API:**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs

### Option 5: Docker (Local/Cloud)

1. **Build and run with Docker Compose:**
   ```bash
   # Set your API key
   export GROQ_API_KEY=your_groq_api_key_here
   
   # Deploy
   docker-compose up --build
   ```

2. **Or use the deployment script:**
   ```bash
   # Make script executable
   chmod +x deploy.sh
   
   # Deploy with Docker
   ./deploy.sh docker
   
   # Or deploy locally
   ./deploy.sh local
   ```

## 🔑 Getting Your Groq API Key

1. **Go to [Groq Console](https://console.groq.com/)**
2. **Sign up/Login**
3. **Navigate to API Keys**
4. **Create a new API key**
5. **Copy the key and use it in your deployment**

## 📝 Testing Your Deployment

Once deployed, test your API:

```bash
# Health check
curl https://your-app-url.com/

# Test Q&A endpoint
curl -X POST "https://your-app-url.com/hackrx/run" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": "https://example.com/document.pdf",
    "questions": ["What is the main topic?"]
  }'
```

## 🌐 API Endpoints

- **Health Check:** `GET /`
- **Main Q&A:** `POST /hackrx/run`
- **File Upload:** `POST /upload-and-ask`
- **Documentation:** `GET /docs`

## 🔧 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | ✅ | Your Groq API key |
| `DEFAULT_MODEL` | ❌ | LLM model (default: llama3-70b-8192) |
| `DEFAULT_TEMPERATURE` | ❌ | Model creativity (default: 0.5) |
| `DEFAULT_MAX_TOKENS` | ❌ | Max response length (default: 3072) |

## 🚨 Troubleshooting

### Common Issues:

1. **API Key Error:**
   - Ensure `GROQ_API_KEY` is set correctly
   - Check for extra spaces or characters

2. **Port Issues:**
   - Use `$PORT` environment variable for cloud platforms
   - Default local port is 8000

3. **Dependencies Error:**
   - Ensure all requirements are installed
   - Check Python version (3.11+ recommended)

4. **Document Loading Error:**
   - Check if document URL is accessible
   - Ensure document format is supported (PDF, DOCX, TXT)

### Getting Help:

- Check the logs: `docker-compose logs` or platform logs
- Test locally first: `./deploy.sh local`
- Run tests: `./deploy.sh test`

## 📊 Monitoring

For production deployments, consider adding:

- **Logging:** Request/response logging
- **Monitoring:** Health checks and metrics
- **Rate Limiting:** API usage limits
- **Authentication:** API key validation
- **Caching:** Response caching for better performance 