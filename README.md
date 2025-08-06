# Document Q&A API

A FastAPI-based webhook service that parses documents and answers questions using AI. Perfect for integration with webhook systems.

## 🚀 Quick Deploy to Render

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### Step 2: Deploy on Render
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name:** `document-qa-api`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python3 app.py`
5. Add Environment Variable:
   - **Key:** `GROQ_API_KEY`
   - **Value:** Your Groq API key
6. Click "Create Web Service"

### Step 3: Get Your Webhook URL
Your webhook URL will be:
```
https://your-app-name.onrender.com/hackrx/run
```

## 🔗 Webhook Usage

### Endpoint
```
POST /hackrx/run
```

### Headers
```
Content-Type: application/json
Accept: application/json
Authorization: Bearer 3eda6f3ac8aeaebd1954058607902b3759d6cbbf848dec41d470a19263cd7180
```

### Request Body
```json
{
  "documents": "https://example.com/policy.pdf",
  "questions": [
    "What is the grace period for premium payment?",
    "What is the waiting period for pre-existing diseases?"
  ]
}
```

### Response
```json
{
  "answers": [
    "A grace period of thirty days is provided for premium payment...",
    "There is a waiting period of thirty-six (36) months..."
  ]
}
```

## 🔑 Authentication

The API uses Bearer token authentication:
- **Token:** `3eda6f3ac8aeaebd1954058607902b3759d6cbbf848dec41d470a19263cd7180`
- **Required for all protected endpoints**

## 📋 Features

- ✅ Document parsing (PDF, DOCX, TXT) from URLs
- ✅ AI-powered Q&A using Groq LLM
- ✅ Vector-based document retrieval
- ✅ Bearer token authentication
- ✅ CORS support
- ✅ Automatic HTTPS (on Render)

## 🔧 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | ✅ | Your Groq API key |

## 🧪 Testing

Test your webhook:
```bash
curl -X POST "https://your-app-name.onrender.com/hackrx/run" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer 3eda6f3ac8aeaebd1954058607902b3759d6cbbf848dec41d470a19263cd7180" \
  -d '{
    "documents": "https://example.com/policy.pdf",
    "questions": ["What is the grace period for premium payment?"]
  }'
```

## 📚 API Documentation

Once deployed, visit:
- **Swagger UI:** `https://your-app-name.onrender.com/docs`
- **Health Check:** `https://your-app-name.onrender.com/`

## 🎯 Use Cases

- Insurance policy Q&A
- Document analysis
- Automated customer support
- Content summarization
- Legal document review

## 📄 Supported Document Types

- PDF files
- DOCX files
- TXT files
- URLs pointing to any of the above

## 🔒 Security

- Bearer token authentication
- Input validation
- Error handling
- CORS configuration
- Environment variable protection 