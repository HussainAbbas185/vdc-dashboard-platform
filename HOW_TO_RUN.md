# VDC Dashboard - Quick Start Guide

## 🚀 How to Run the Dashboard

### Method 1: Double-Click (Easiest)
Simply **double-click** the `run_dashboard.bat` file in this folder.

### Method 2: Command Line
Open PowerShell in this directory and run:
```powershell
.\.venv\Scripts\python.exe -m streamlit run dashboard.py
```

### Method 3: Short Command (if you're already in the project folder)
```powershell
.\run_dashboard.bat
```

## 🌐 Accessing the Dashboard
Once running, open your browser to:
- **http://localhost:8501**

## 🛑 Stopping the Dashboard
Press `Ctrl + C` in the terminal window

## 📝 Notes
- Make sure you're in the project directory when running commands
- The virtual environment (.venv) must exist with all dependencies installed
- If you get errors, ensure all packages are installed: `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`
