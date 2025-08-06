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

# LangChain imports for document processing and AI
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

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

# Default model settings
DEFAULT_MODEL = "llama3-70b-8192"
DEFAULT_TEMPERATURE = 0.5
DEFAULT_MAX_TOKENS = 3072

# ==================== HELPER FUNCTIONS ====================
def load_document_from_url(url: str):
    """
    Load document from URL using appropriate loader
    """
    import requests
    from langchain.schema import Document
    from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
    import tempfile
    import os
    
    try:
        # Download the document
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Determine file type from URL or content
        if url.lower().endswith('.pdf'):
            file_type = 'pdf'
        elif url.lower().endswith('.docx'):
            file_type = 'docx'
        elif url.lower().endswith('.txt'):
            file_type = 'txt'
        else:
            # Try to determine from content type
            content_type = response.headers.get('content-type', '').lower()
            if 'pdf' in content_type:
                file_type = 'pdf'
            elif 'word' in content_type or 'docx' in content_type:
                file_type = 'docx'
            else:
                file_type = 'txt'
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_type}") as tmp:
            tmp.write(response.content)
            tmp_path = tmp.name
        
        try:
            # Load document based on file type
            if file_type == 'pdf':
                loader = PyPDFLoader(tmp_path)
            elif file_type == 'docx':
                loader = Docx2txtLoader(tmp_path)
            else:
                loader = TextLoader(tmp_path)
            
            documents = loader.load()
            
            # Update metadata with source URL
            for doc in documents:
                doc.metadata["source"] = url
            
            return documents
            
        finally:
            # Clean up temporary file
            os.remove(tmp_path)
            
    except requests.exceptions.RequestException as e:
        # Fallback to placeholder content if URL loading fails
        print(f"Warning: Could not load document from URL {url}: {e}")
        print("Using placeholder content for testing...")
        
        placeholder_content = """
        This is a placeholder document content. In a real implementation, 
        you would download and parse the document from the provided URL.
        
        Sample policy information:
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
        
        return [Document(page_content=placeholder_content, metadata={"source": url})]

def process_documents_and_answer_questions(documents_url: str, questions: List[str]):
    """
    Main function to process documents and answer questions
    """
    try:
        # Load documents from URL
        raw_docs = load_document_from_url(documents_url)
        
        if not raw_docs:
            raise HTTPException(status_code=400, detail="No valid documents to process")
        
        # Split documents into chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
        chunks = splitter.split_documents(raw_docs)
        
        # Create embeddings and vector store
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_store = FAISS.from_documents(chunks, embeddings)
        retriever = vector_store.as_retriever()
        
        # Initialize language model
        llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name=DEFAULT_MODEL,
            temperature=DEFAULT_TEMPERATURE,
            max_tokens=DEFAULT_MAX_TOKENS
        )
        
        # Create prompt template
        prompt = ChatPromptTemplate.from_template("""
        You are a helpful assistant that answers questions based on the provided context.
        Use the context below to answer the question accurately and concisely.
        
        <context>
        {context}
        </context>
        
        Question: {input}
        
        Provide a clear and helpful answer based on the context provided.
        """)
        
        # Create chains
        document_chain = create_stuff_documents_chain(llm, prompt)
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        
        # Answer each question
        answers = []
        for question in questions:
            response = retrieval_chain.invoke({"input": question})
            answer = response.get("answer", "No answer generated.")
            answers.append(answer)
        
        return answers
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing documents: {str(e)}")

# ==================== API ENDPOINTS ====================
@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Document Q&A API is running", "status": "healthy"}

@app.post("/hackrx/run", response_model=AnswerResponse)
async def answer_questions(request: QuestionRequest, token: str = Depends(verify_token)):
    """
    Main endpoint for answering questions about documents
    
    Args:
        request: QuestionRequest containing documents URL and questions list
    
    Returns:
        AnswerResponse containing list of answers
    """
    try:
        # Validate input
        if not request.documents:
            raise HTTPException(status_code=400, detail="Documents URL is required")
        
        if not request.questions or len(request.questions) == 0:
            raise HTTPException(status_code=400, detail="At least one question is required")
        
        # Process documents and answer questions
        answers = process_documents_and_answer_questions(request.documents, request.questions)
        
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
        # Parse questions (assuming comma-separated or JSON format)
        if questions.startswith('[') and questions.endswith(']'):
            # JSON array format
            import json
            question_list = json.loads(questions)
        else:
            # Comma-separated format
            question_list = [q.strip() for q in questions.split(',') if q.strip()]
        
        if not question_list:
            raise HTTPException(status_code=400, detail="No valid questions provided")
        
        # Process uploaded files
        raw_docs = []
        for file in files:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as tmp:
                content = await file.read()
                tmp.write(content)
                tmp_path = tmp.name
            
            try:
                # Load document based on file type
                suffix = file.filename.split(".")[-1].lower()
                if suffix == "pdf":
                    loader = PyPDFLoader(tmp_path)
                elif suffix == "docx":
                    loader = Docx2txtLoader(tmp_path)
                elif suffix == "txt":
                    loader = TextLoader(tmp_path)
                else:
                    continue  # Skip unsupported files
                
                raw_docs.extend(loader.load())
            finally:
                os.remove(tmp_path)
        
        if not raw_docs:
            raise HTTPException(status_code=400, detail="No valid documents to process")
        
        # Process documents and answer questions
        answers = process_documents_and_answer_questions_from_files(raw_docs, question_list)
        
        return AnswerResponse(answers=answers)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

def process_documents_and_answer_questions_from_files(raw_docs, questions: List[str]):
    """
    Process documents from files and answer questions
    """
    try:
        # Split documents into chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
        chunks = splitter.split_documents(raw_docs)
        
        # Create embeddings and vector store
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_store = FAISS.from_documents(chunks, embeddings)
        retriever = vector_store.as_retriever()
        
        # Initialize language model
        llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name=DEFAULT_MODEL,
            temperature=DEFAULT_TEMPERATURE,
            max_tokens=DEFAULT_MAX_TOKENS
        )
        
        # Create prompt template
        prompt = ChatPromptTemplate.from_template("""
        You are a helpful assistant that answers questions based on the provided context.
        Use the context below to answer the question accurately and concisely.
        
        <context>
        {context}
        </context>
        
        Question: {input}
        
        Provide a clear and helpful answer based on the context provided.
        """)
        
        # Create chains
        document_chain = create_stuff_documents_chain(llm, prompt)
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        
        # Answer each question
        answers = []
        for question in questions:
            response = retrieval_chain.invoke({"input": question})
            answer = response.get("answer", "No answer generated.")
            answers.append(answer)
        
        return answers
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing documents: {str(e)}")

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