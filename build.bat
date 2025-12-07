@echo off
REM Build script for Windows to create executable from GUI app

echo 🔨 Building LasGUI executable...

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install build requirements
echo 📥 Installing build requirements...
python -m pip install --upgrade pip
pip install -r requirements-build.txt

REM Clean previous builds (but keep build-exe.spec)
echo 🧹 Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__
REM Only remove auto-generated spec files, not build-exe.spec
for %%f in (*.spec) do if not "%%f"=="build-exe.spec" del /q "%%f"

REM Build executable
echo 🏗️  Building executable with PyInstaller...
pyinstaller build-exe.spec

REM Check if build was successful
if exist "dist\LasGUI.exe" (
    echo ✅ Build successful!
    echo 📦 Executable location: dist\LasGUI.exe
    dir dist\LasGUI.exe
    echo.
    echo 🚀 You can now run the executable from the dist\ directory
) else (
    echo ❌ Build failed. Check the output above for errors.
    exit /b 1
)

pause

