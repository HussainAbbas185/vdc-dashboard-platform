@echo off
echo ========================================
echo   Starting VDC Dashboard...
echo ========================================
echo.
.\.venv\Scripts\python.exe -m streamlit run dashboard.py
pause
