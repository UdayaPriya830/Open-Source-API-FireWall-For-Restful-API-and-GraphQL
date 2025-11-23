#!/bin/bash

echo "========================================"
echo "  API Firewall - Quick Deploy Script"
echo "========================================"
echo

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found! Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

echo "✅ Docker found!"

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found! Please install Docker Compose."
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker Compose found!"

# Check if docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found!"
    echo "Make sure you're in the project root directory."
    exit 1
fi

echo "🚀 Starting API Firewall services..."
echo

# Start services
docker-compose up -d

if [ $? -eq 0 ]; then
    echo
    echo "✅ Services started successfully!"
    echo
    echo "🌐 Access Points:"
    echo "  • Firewall API: http://localhost:8000"
    echo "  • Dashboard:    http://localhost:8501"
    echo "  • Test API:     http://localhost:8080"
    echo
    echo "📊 Open the dashboard to see real-time monitoring!"
    echo
    echo "🔍 Run demo: python demo_script.py"
    echo
    
    # Try to open dashboard in browser (Linux/Mac)
    if command -v xdg-open &> /dev/null; then
        echo "Opening dashboard in browser..."
        xdg-open http://localhost:8501
    elif command -v open &> /dev/null; then
        echo "Opening dashboard in browser..."
        open http://localhost:8501
    else
        echo "Please open http://localhost:8501 in your browser"
    fi
else
    echo
    echo "❌ Failed to start services!"
    echo "Check the error messages above."
    echo
    echo "🔧 Troubleshooting:"
    echo "  • Make sure ports 8000, 8501, 8080 are free"
    echo "  • Try: docker-compose down"
    echo "  • Then run this script again"
fi

echo
echo "Press Enter to continue..."
read