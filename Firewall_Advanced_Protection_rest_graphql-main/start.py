#!/usr/bin/env python3
"""
API Firewall Startup Script
Starts both the FastAPI backend and Streamlit dashboard
"""

import subprocess
import sys
import os
import time
import threading

def start_backend():
    """Start FastAPI backend server."""
    print("🚀 Starting API Firewall Backend...")
    os.chdir("backend")
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000", 
        "--reload"
    ])

def start_dashboard():
    """Start Streamlit dashboard."""
    print("📊 Starting Security Dashboard...")
    time.sleep(3)  # Wait for backend to start
    dashboard_path = os.path.join(os.getcwd(), "dashboard.py")
    subprocess.run([
        sys.executable, "-m", "streamlit", 
        "run", dashboard_path, 
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ])

def main():
    print("🛡️  API Firewall - Advanced Protection System")
    print("=" * 50)
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Start dashboard in main thread
    try:
        start_dashboard()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down API Firewall...")
        sys.exit(0)

if __name__ == "__main__":
    main()