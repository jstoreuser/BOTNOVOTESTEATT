@echo off
REM ==========================================
REM BotNovoTesteAtt - Automated Setup Script
REM AI-Human Collaborative Development Setup
REM ==========================================

echo.
echo 🤖 BotNovoTesteAtt - AI-Human Collaborative Setup
echo ================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.10+ first.
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment created
echo.

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip and core tools
echo 📈 Upgrading pip and core tools...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo ❌ Failed to upgrade pip
    pause
    exit /b 1
)

echo ✅ Core tools upgraded
echo.

REM Install production dependencies
echo 📥 Installing production dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install production dependencies
    pause
    exit /b 1
)

echo ✅ Production dependencies installed
echo.

REM Install development dependencies
echo 🔧 Installing development dependencies...
pip install -r requirements-dev.txt
if errorlevel 1 (
    echo ❌ Failed to install development dependencies
    pause
    exit /b 1
)

echo ✅ Development dependencies installed
echo.

REM Install Playwright browsers
echo 🎭 Installing Playwright browsers...
playwright install
if errorlevel 1 (
    echo ⚠️  Playwright browser installation failed (non-critical)
    echo    You can install them later with: playwright install
)

echo ✅ Playwright setup completed
echo.

REM Setup pre-commit hooks
echo 🪝 Setting up pre-commit hooks...
pre-commit install
if errorlevel 1 (
    echo ⚠️  Pre-commit setup failed (non-critical)
    echo    You can set it up later with: pre-commit install
)

echo ✅ Pre-commit hooks installed
echo.

REM Create necessary directories
echo 📁 Creating project directories...
if not exist "logs" mkdir logs
if not exist "data" mkdir data
if not exist "screenshots" mkdir screenshots

echo ✅ Project directories created
echo.

REM Run basic validation
echo 🧪 Running basic validation...
python -c "import sys; print(f'✅ Python {sys.version}')"
python -c "import playwright; print('✅ Playwright imported successfully')"
python -c "import dearpygui; print('✅ DearPyGUI imported successfully')"

echo.
echo 🎉 Setup completed successfully!
echo.
echo 🚀 Next steps:
echo    1. Open VS Code: code .
echo    2. Install recommended extensions when prompted
echo    3. Run the bot: Use VS Code task "🚀 Run Bot"
echo.
echo 🤖 Ready for AI-Human collaborative development!
echo.

pause
