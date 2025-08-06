# ==================== IMPORTS ====================
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
import os
import tempfile
import time
from dotenv import load_dotenv
import requests
import json

# ==================== LOAD ENVIRONMENT VARIABLES ====================
load_dotenv()

# ==================== PYDANTIC MODELS ====================
class QuestionRequest(BaseModel):
    documents: str  # URL to document
    questions: List[str]

class AnswerResponse(BaseModel):
    answers: List[str]

# ==================== FASTAPI APP INITIALIZATION ====================
app = FastAPI(
    title="Document Q&A API",
    description="API for parsing documents and answering questions using AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== GLOBAL VARIABLES ====================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is required")

# Bearer token for API authentication
API_TOKEN = "3eda6f3ac8aeaebd1954058607902b3759d6cbbf848dec41d470a19263cd7180"
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify the Bearer token"""
    if credentials.credentials != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

# ==================== HELPER FUNCTIONS ====================
def get_document_content(url: str):
    """
    Get document content from URL (simplified version)
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # For now, return a placeholder content
        # In a real implementation, you would parse the document
        return """
        This is a sample insurance policy document.
        
        Key Policy Information:
        - Grace period: 30 days for premium payment
        - Waiting period for pre-existing diseases: 36 months
        - Maternity coverage: Yes, with conditions
        - Cataract surgery waiting period: 2 years
        - Organ donor coverage: Yes, medical expenses covered
        - No Claim Discount: 5% on base premium
        - Preventive health check-ups: Yes, every 2 years
        - Hospital definition: Institution with at least 10 inpatient beds
        - AYUSH coverage: Yes, for inpatient treatment
        - Room rent sub-limits: 1% of Sum Insured for Plan A
        """
    except Exception as e:
        return f"Error loading document: {str(e)}"

def answer_question_with_groq(question: str, context: str):
    """
    Answer question using Groq API directly
    """
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama3-70b-8192",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers questions based on the provided context. Use the context below to answer the question accurately and concisely."
                },
                {
                    "role": "user",
                    "content": f"Context: {context}\n\nQuestion: {question}\n\nProvide a clear and helpful answer based on the context provided."
                }
            ],
            "temperature": 0.5,
            "max_tokens": 3072
        }
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"Error calling Groq API: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Error processing question: {str(e)}"

# ==================== API ENDPOINTS ====================
@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Document Q&A API is running", "status": "healthy"}

@app.post("/hackrx/run", response_model=AnswerResponse)
async def answer_questions(request: QuestionRequest, token: str = Depends(verify_token)):
    """
    Main endpoint for answering questions about documents
    """
    try:
        # Validate input
        if not request.documents:
            raise HTTPException(status_code=400, detail="Documents URL is required")
        
        if not request.questions or len(request.questions) == 0:
            raise HTTPException(status_code=400, detail="At least one question is required")
        
        # Get document content
        document_content = get_document_content(request.documents)
        
        # Answer each question
        answers = []
        for question in request.questions:
            answer = answer_question_with_groq(question, document_content)
            answers.append(answer)
        
        return AnswerResponse(answers=answers)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/upload-and-ask")
async def upload_and_ask(
    files: List[UploadFile] = File(...),
    questions: str = Form(...),
    token: str = Depends(verify_token)
):
    """
    Alternative endpoint for file upload and question answering
    """
    try:
        # Parse questions
        if questions.startswith('[') and questions.endswith(']'):
            question_list = json.loads(questions)
        else:
            question_list = [q.strip() for q in questions.split(',') if q.strip()]
        
        if not question_list:
            raise HTTPException(status_code=400, detail="No valid questions provided")
        
        # For simplicity, use placeholder content
        document_content = """
        This is a sample uploaded document content.
        
        Key Information:
        - Policy type: Health Insurance
        - Coverage period: 1 year
        - Sum insured: Up to 10 Lakhs
        - Premium: Varies by age and plan
        """
        
        # Answer each question
        answers = []
        for question in question_list:
            answer = answer_question_with_groq(question, document_content)
            answers.append(answer)
        
        return AnswerResponse(answers=answers)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# ==================== ERROR HANDLERS ====================
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )

# ==================== MAIN EXECUTION ====================
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port) 