# 🚀 Modern File Processor (CustomTkinter GUI)

A modern, dark-themed **file processing application** built with **Python + CustomTkinter**.  
It allows users to choose input/output files, adjust processing settings, view progress, and process files through a clean, modular GUI.

---

## ✨ Features

### 🎨 Modern UI
- Stylish **dark mode**
- Responsive layout
- Custom headers, sliders, buttons, and scrollable frames

### 📂 File Operations
- Select **input file**
- Choose **output file location**
- Clear selected files
- Live status updates
- Progress bar animation

### ⚙️ Settings Window
Includes customizable parameters:
- **Points to Render (%)** — controlled by a slider  
- **Output Format** — `.las`, `.txt`, `.csv`
- Buttons:
  - **Save Settings**
  - **Reset to Default**
  - **Cancel (Close Window)**

Settings persist during the current session.

### 🧩 Modular Structure
Easy to maintain and extend:
- `guiapp.py`  
- `views.py`  
- `settings_view.py`  
- `handlers.py`

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone <repo-url>
cd modern-file-processor
```
### 2. (Optional) Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate    # Linux/MacOS
venv\Scripts\activate       # Windows
```
### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```
### ▶️ Run the Application
```bash
python guiapp.py
```
### 🧭 Project Structure
```bash
📦 modern-file-processor
│
├── guiapp.py              # Main GUI
├── settings_view.py       # Settings window
├── views.py               # Factory-style UI components
├── handlers.py            # Logic for buttons & events
├── README.md
└── assets/                # (Optional) images/screenshots

```