#!/bin/bash

# Document Q&A API Deployment Script
# This script helps deploy the FastAPI application

set -e  # Exit on any error

echo "🚀 Starting Document Q&A API deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if .env file exists
if [ ! -f .env ]; then
    print_warning ".env file not found. Creating template..."
    cat > .env << EOF
# Groq API Key for LLM access
GROQ_API_KEY=your_groq_api_key_here

# Optional: Model configuration
DEFAULT_MODEL=llama3-70b-8192
DEFAULT_TEMPERATURE=0.5
DEFAULT_MAX_TOKENS=3072

# Optional: Server configuration
HOST=0.0.0.0
PORT=8000
EOF
    print_error "Please edit .env file and add your GROQ_API_KEY before continuing."
    exit 1
fi

# Check if GROQ_API_KEY is set
if ! grep -q "GROQ_API_KEY=.*[^your_groq_api_key_here]" .env; then
    print_error "Please set your GROQ_API_KEY in the .env file"
    exit 1
fi

# Function to check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
}

# Function to deploy with Docker
deploy_docker() {
    print_status "Deploying with Docker..."
    
    # Build and start containers
    docker-compose up --build -d
    
    print_status "Waiting for service to start..."
    sleep 10
    
    # Check if service is running
    if curl -f http://localhost:8000/ > /dev/null 2>&1; then
        print_status "✅ Service is running successfully!"
        print_status "🌐 API URL: http://localhost:8000"
        print_status "📚 Documentation: http://localhost:8000/docs"
    else
        print_error "❌ Service failed to start properly"
        docker-compose logs
        exit 1
    fi
}

# Function to deploy locally
deploy_local() {
    print_status "Deploying locally..."
    
    # Check if Python is installed
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3 first."
        exit 1
    fi
    
    # Install dependencies
    print_status "Installing dependencies..."
    pip3 install -r requirements.txt
    
    # Start the application
    print_status "Starting the application..."
    python3 app.py &
    
    # Wait for service to start
    sleep 5
    
    # Check if service is running
    if curl -f http://localhost:8000/ > /dev/null 2>&1; then
        print_status "✅ Service is running successfully!"
        print_status "🌐 API URL: http://localhost:8000"
        print_status "📚 Documentation: http://localhost:8000/docs"
        print_warning "Press Ctrl+C to stop the service"
        
        # Keep the script running
        wait
    else
        print_error "❌ Service failed to start properly"
        exit 1
    fi
}

# Function to run tests
run_tests() {
    print_status "Running API tests..."
    python3 test_api.py
}

# Function to show logs
show_logs() {
    print_status "Showing Docker logs..."
    docker-compose logs -f
}

# Function to stop service
stop_service() {
    print_status "Stopping service..."
    docker-compose down
    print_status "✅ Service stopped"
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  docker    Deploy using Docker (default)"
    echo "  local     Deploy locally with Python"
    echo "  test      Run API tests"
    echo "  logs      Show Docker logs"
    echo "  stop      Stop the service"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 docker    # Deploy with Docker"
    echo "  $0 local     # Deploy locally"
    echo "  $0 test      # Run tests"
}

# Main script logic
case "${1:-docker}" in
    "docker")
        check_docker
        deploy_docker
        ;;
    "local")
        deploy_local
        ;;
    "test")
        run_tests
        ;;
    "logs")
        show_logs
        ;;
    "stop")
        stop_service
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        print_error "Unknown option: $1"
        show_help
        exit 1
        ;;
esac 