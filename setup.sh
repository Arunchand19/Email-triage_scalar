#!/usr/bin/env bash
#
# setup.sh - Automated setup script for Email Triage OpenEnv
#
# Usage:
#   bash setup.sh [--test|--docker|--deploy]
#
# Options:
#   --test    Run test suite only
#   --docker  Build and test Docker image
#   --deploy  Full deployment check
#   (no args) Interactive setup

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log() { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
error() { echo -e "${RED}[✗]${NC} $1"; exit 1; }

echo "=========================================="
echo "  Email Triage OpenEnv Setup"
echo "=========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    error "Python 3 not found. Please install Python 3.9+"
fi
log "Python 3 found: $(python3 --version)"

# Check pip
if ! command -v pip3 &> /dev/null; then
    error "pip3 not found. Please install pip"
fi
log "pip3 found"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt > /dev/null 2>&1
log "Dependencies installed"

# Run tests if requested
if [ "$1" = "--test" ] || [ "$1" = "--deploy" ]; then
    echo ""
    echo "Running test suite..."
    python3 test_env.py
    log "All tests passed"
fi

# Docker build if requested
if [ "$1" = "--docker" ] || [ "$1" = "--deploy" ]; then
    echo ""
    if ! command -v docker &> /dev/null; then
        warn "Docker not found. Skipping Docker build."
    else
        echo "Building Docker image..."
        docker build -t email-triage-env . > /dev/null 2>&1
        log "Docker image built successfully"
        
        echo ""
        echo "Testing Docker container..."
        docker run -d -p 7860:7860 --name email-triage-test email-triage-env > /dev/null 2>&1
        sleep 5
        
        if curl -s http://localhost:7860/health > /dev/null; then
            log "Docker container running successfully"
        else
            error "Docker container health check failed"
        fi
        
        docker stop email-triage-test > /dev/null 2>&1
        docker rm email-triage-test > /dev/null 2>&1
    fi
fi

# Full deployment check
if [ "$1" = "--deploy" ]; then
    echo ""
    echo "Running deployment validation..."
    
    # Start server in background
    python3 app.py > /dev/null 2>&1 &
    SERVER_PID=$!
    sleep 3
    
    # Test endpoints
    if curl -s http://localhost:7860/health > /dev/null; then
        log "Server health check passed"
    else
        kill $SERVER_PID 2>/dev/null
        error "Server health check failed"
    fi
    
    if curl -s -X POST http://localhost:7860/reset -H "Content-Type: application/json" -d '{"task":"easy"}' > /dev/null; then
        log "Reset endpoint working"
    else
        kill $SERVER_PID 2>/dev/null
        error "Reset endpoint failed"
    fi
    
    # Stop server
    kill $SERVER_PID 2>/dev/null
    log "Server tests passed"
    
    # Run mock inference
    echo ""
    echo "Running mock inference..."
    python3 inference.py --mock > /dev/null 2>&1
    log "Mock inference completed"
fi

# Interactive setup
if [ -z "$1" ]; then
    echo ""
    echo "Setup complete! Next steps:"
    echo ""
    echo "1. Test environment:"
    echo "   python3 test_env.py"
    echo ""
    echo "2. Start server:"
    echo "   python3 app.py"
    echo ""
    echo "3. Run inference (mock mode):"
    echo "   python3 inference.py --mock"
    echo ""
    echo "4. Run inference (with API):"
    echo "   export HF_TOKEN='your_token'"
    echo "   python3 inference.py"
    echo ""
    echo "5. Build Docker image:"
    echo "   docker build -t email-triage-env ."
    echo ""
    echo "6. Run validation:"
    echo "   bash validate-submission.sh http://localhost:7860"
    echo ""
fi

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
