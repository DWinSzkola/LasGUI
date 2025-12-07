#!/bin/bash
# Build script for creating executable from GUI app

set -e

echo "🔨 Building LasGUI executable..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install build requirements
echo "📥 Installing build requirements..."
pip install --upgrade pip
pip install -r requirements-build.txt

# Clean previous builds (but keep the spec file)
echo "🧹 Cleaning previous builds..."
rm -rf build dist __pycache__
# Only remove auto-generated spec files, not build-exe.spec
find . -maxdepth 1 -name "*.spec" ! -name "build-exe.spec" -delete 2>/dev/null || true

# Build executable
echo "🏗️  Building executable with PyInstaller..."
pyinstaller build-exe.spec

# Check if build was successful
if [ -f "dist/LasGUI" ] || [ -f "dist/LasGUI.exe" ]; then
    echo "✅ Build successful!"
    echo "📦 Executable location:"
    if [ -f "dist/LasGUI" ]; then
        echo "   dist/LasGUI (macOS/Linux)"
        ls -lh dist/LasGUI
    fi
    if [ -f "dist/LasGUI.exe" ]; then
        echo "   dist/LasGUI.exe (Windows)"
        ls -lh dist/LasGUI.exe
    fi
    echo ""
    echo "🚀 You can now run the executable from the dist/ directory"
else
    echo "❌ Build failed. Check the output above for errors."
    exit 1
fi

