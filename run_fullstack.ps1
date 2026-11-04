Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Video Deepfake Detection - Launching Fullstack Platform" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

Start-Process powershell -ArgumentList "-NoExit", "-File", ".\run_backend.ps1"
Start-Process powershell -ArgumentList "-NoExit", "-File", ".\run_frontend.ps1"

Write-Host "Backend API: http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "Frontend UI: http://localhost:5173" -ForegroundColor Green
