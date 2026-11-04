@echo off
echo ========================================================
echo   Video Deepfake Detection - Starting FastAPI Backend Server
echo ========================================================
set TORCHDYNAMO_DISABLE=1
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
