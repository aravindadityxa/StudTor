@echo off
REM StudTor Ollama Setup Script
REM This script checks, installs, and configures Ollama for offline AI

setlocal enabledelayedexpansion

echo.
echo ========================================
echo    StudTor - Ollama Setup
echo ========================================
echo.

REM Check if Ollama is installed
echo [1/5] Checking Ollama installation...
where ollama >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Ollama is not installed or not in PATH.
    echo.
    echo Please install Ollama from: https://ollama.ai
    echo.
    echo After installation:
    echo   1. Restart this script
    echo   2. Ensure Ollama is running (start Ollama app)
    echo   3. This script will automatically download qwen2.5:1.5b
    echo.
    pause
    exit /b 1
)

echo [✓] Ollama found
echo.

REM Check if Ollama service is running
echo [2/5] Checking if Ollama is running...
timeout /t 2 /nobreak >nul
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [NOTICE] Ollama service is not running.
    echo.
    echo Please start Ollama by:
    echo   1. Opening the Ollama application
    echo   2. Waiting for it to show "Ollama is running"
    echo   3. Then run this script again
    echo.
    pause
    exit /b 1
)

echo [✓] Ollama is running
echo.

REM Pull the model
echo [3/5] Downloading qwen2.5:1.5b model...
echo This may take a few minutes on first run...
echo.
ollama pull qwen2.5:1.5b

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to download model
    echo Please check your internet connection and try again
    echo.
    pause
    exit /b 1
)

echo.
echo [✓] Model downloaded successfully
echo.

REM Verify model
echo [4/5] Verifying model installation...
ollama list | findstr "qwen2.5" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Model verification failed
    pause
    exit /b 1
)

echo [✓] Model verified
echo.

REM Test model
echo [5/5] Testing model...
echo Testing model with a simple query...
timeout /t 2 /nobreak >nul
curl -X POST http://localhost:11434/api/generate -H "Content-Type: application/json" -d "{\"model\":\"qwen2.5:1.5b\",\"prompt\":\"Hello\",\"stream\":false}" >nul 2>&1

if %errorlevel% neq 0 (
    echo [WARNING] Model test failed, but setup may still work
) else (
    echo [✓] Model test successful
)

echo.
echo ========================================
echo    Setup Complete!
echo ========================================
echo.
echo StudTor is now ready to use with Ollama.
echo.
echo To start StudTor:
echo   1. Ensure Ollama is running
echo   2. Run: python run.py
echo   3. Open http://localhost:5500 in your browser
echo.
echo Model: qwen2.5:1.5b
echo API URL: http://localhost:11434
echo.
pause
