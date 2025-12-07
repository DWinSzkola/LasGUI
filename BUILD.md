# Building Executable from GUI App

This guide explains how to build a standalone executable from the GUI application, avoiding Docker/X11 complexity.

## Prerequisites

- Python 3.10 or higher
- pip

## Quick Build

### macOS/Linux:
```bash
./build.sh
```

### Windows:
```batch
build.bat
```

## Manual Build Steps

### 1. Create Virtual Environment (Optional but Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Build Requirements

```bash
pip install -r requirements-build.txt
```

### 3. Build Executable

```bash
pyinstaller build-exe.spec
```

The executable will be created in the `dist/` directory:
- **macOS/Linux**: `dist/LasGUI`
- **Windows**: `dist/LasGUI.exe`

## Configuration

### API URL

The executable will connect to the API at `http://localhost:8000` by default. You can change this by:

1. **Environment Variable**: Set `API_URL` before running:
   ```bash
   export API_URL=http://your-api-host:8000
   ./dist/LasGUI
   ```

2. **Modify the code**: Edit `gui_app.py` to change the default API URL.

### Custom Icon

To add a custom icon to the executable:

1. Create or obtain an `.ico` file (Windows) or `.icns` file (macOS)
2. Update `build-exe.spec`:
   ```python
   icon='path/to/your/icon.ico',  # or .icns for macOS
   ```

## Troubleshooting

### Build Fails

- Ensure all dependencies are installed: `pip install -r requirements-build.txt`
- Check that Python version is 3.10+
- Try cleaning and rebuilding: `rm -rf build dist __pycache__`

### Executable Doesn't Run

- Check console output (if console=False, temporarily set to True in spec file)
- Ensure API server is running if the app needs to connect to it
- Check file permissions: `chmod +x dist/LasGUI` (Linux/macOS)

### Large Executable Size

The executable includes Python and all dependencies, so it will be large (50-100MB+). This is normal for PyInstaller builds.

### Missing Modules

If you get import errors, add missing modules to `hiddenimports` in `build-exe.spec`.

## Distribution

To distribute the executable:

1. **Single File**: The executable is self-contained - just copy `dist/LasGUI` (or `LasGUI.exe`) to the target machine
2. **Dependencies**: No additional installation needed - Python and all libraries are bundled
3. **API**: Make sure the API server is accessible from the target machine

## Cross-Platform Building

- **macOS**: Build on macOS to create macOS executable
- **Windows**: Build on Windows to create Windows executable  
- **Linux**: Build on Linux to create Linux executable

For cross-platform builds, use Docker or CI/CD services.

## Notes

- The executable is platform-specific (can't run macOS exe on Windows, etc.)
- First launch may be slower as PyInstaller extracts files to a temp directory
- Antivirus software may flag PyInstaller executables - this is a false positive

