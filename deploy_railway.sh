#!/bin/bash

# Railway Deployment Script for Document Q&A API
# This script helps deploy the FastAPI application to Railway

set -e

echo "🚀 Starting Railway deployment for Document Q&A API..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if Railway CLI is installed
check_railway_cli() {
    if ! command -v railway &> /dev/null; then
        print_error "Railway CLI is not installed."
        print_status "Installing Railway CLI..."
        
        if command -v npm &> /dev/null; then
            npm install -g @railway/cli
        else
            print_error "npm is not installed. Please install Node.js first:"
            print_status "Visit: https://nodejs.org/"
            exit 1
        fi
    fi
}

# Check if git is initialized
check_git() {
    if [ ! -d ".git" ]; then
        print_status "Initializing git repository..."
        git init
        git add .
        git commit -m "Initial commit for Railway deployment"
    fi
}

# Deploy to Railway
deploy_to_railway() {
    print_step "1. Checking Railway CLI..."
    check_railway_cli
    
    print_step "2. Checking git repository..."
    check_git
    
    print_step "3. Logging into Railway..."
    railway login
    
    print_step "4. Creating new Railway project..."
    railway init
    
    print_step "5. Setting environment variables..."
    print_warning "Please set your GROQ_API_KEY in Railway dashboard or run:"
    print_status "railway variables set GROQ_API_KEY=your_api_key_here"
    
    print_step "6. Deploying to Railway..."
    railway up
    
    print_step "7. Getting deployment URL..."
    DEPLOY_URL=$(railway status --json | grep -o '"url":"[^"]*"' | cut -d'"' -f4)
    
    if [ -n "$DEPLOY_URL" ]; then
        print_status "✅ Deployment successful!"
        print_status "🌐 Your API is now live at: $DEPLOY_URL"
        print_status "🔗 Webhook URL: $DEPLOY_URL/hackrx/run"
        print_status "📚 API Documentation: $DEPLOY_URL/docs"
        print_status "🔑 Bearer Token: 3eda6f3ac8aeaebd1954058607902b3759d6cbbf848dec41d470a19263cd7180"
        
        echo ""
        print_status "📋 Test your webhook with:"
        echo "curl -X POST \"$DEPLOY_URL/hackrx/run\" \\"
        echo "  -H \"Content-Type: application/json\" \\"
        echo "  -H \"Accept: application/json\" \\"
        echo "  -H \"Authorization: Bearer 3eda6f3ac8aeaebd1954058607902b3759d6cbbf848dec41d470a19263cd7180\" \\"
        echo "  -d '{\"documents\": \"https://example.com/policy.pdf\", \"questions\": [\"What is the grace period for premium payment?\"]}'"
    else
        print_error "❌ Could not get deployment URL. Check Railway dashboard."
    fi
}

# Show help
show_help() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  deploy    Deploy to Railway (default)"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 deploy    # Deploy to Railway"
    echo "  $0 help      # Show help"
}

# Main script logic
case "${1:-deploy}" in
    "deploy")
        deploy_to_railway
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