@echo off
echo Setting up StudTor Backend...

:: Check if virtual environment exists
if not exist "studtor_env" (
    echo Creating virtual environment...
    python -m venv studtor_env
)

echo Activating virtual environment...
call studtor_env\Scripts\activate

echo Installing dependencies...
pip install fastapi uvicorn google-generativeai langdetect python-dotenv sqlalchemy httpx passlib[bcrypt] python-jose[cryptography] aiofiles python-multipart

echo Setup complete!
echo Starting server...
uvicorn main:app --reload --port 8000

pause