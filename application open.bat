@echo off
title InsightFlow AI

cd /d "%~dp0"

echo ====================================
echo        Starting InsightFlow AI
echo ====================================
echo.

start "" http://localhost:8501

"C:\Users\bhoja\anaconda3\python.exe" -m streamlit run app.py

pause