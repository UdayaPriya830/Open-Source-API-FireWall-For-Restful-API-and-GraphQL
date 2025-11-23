@echo off
echo ========================================
echo   API Firewall - Quick Deploy Script
echo ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker not found! Please install Docker Desktop first.
    echo Download from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo ✅ Docker found!
echo.

REM Check if docker-compose.yml exists
if not exist "docker-compose.yml" (
    echo ❌ docker-compose.yml not found!
    echo Make sure you're in the project root directory.
    pause
    exit /b 1
)

echo 🚀 Starting API Firewall services...
echo.

REM Start services
docker-compose up -d

if %errorlevel% equ 0 (
    echo.
    echo ✅ Services started successfully!
    echo.
    echo 🌐 Access Points:
    echo   • Firewall API: http://localhost:8000
    echo   • Dashboard:    http://localhost:8501
    echo   • Test API:     http://localhost:8080
    echo.
    echo 📊 Open the dashboard to see real-time monitoring!
    echo.
    echo 🔍 Run demo: python demo_script.py
    echo.
    echo Press any key to open dashboard in browser...
    pause >nul
    start http://localhost:8501
) else (
    echo.
    echo ❌ Failed to start services!
    echo Check the error messages above.
    echo.
    echo 🔧 Troubleshooting:
    echo   • Make sure ports 8000, 8501, 8080 are free
    echo   • Try: docker-compose down
    echo   • Then run this script again
)

echo.
echo Press any key to exit...
pause >nul