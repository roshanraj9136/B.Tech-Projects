@echo off
echo ========================================================
echo   Video Deepfake Detection - Launching Fullstack Platform
echo ========================================================
start cmd /k "run_backend.bat"
start cmd /k "run_frontend.bat"
echo Backend running on http://127.0.0.1:8000
echo Frontend running on http://localhost:5173
