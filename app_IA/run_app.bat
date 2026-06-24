@echo off
setlocal

cd /d "%~dp0"
set "PY_EXE=%~dp0..\..\..\.venv-1\Scripts\python.exe"

if not exist "%PY_EXE%" (
  echo Python do ambiente nao encontrado em: %PY_EXE%
  echo Ajuste o caminho no arquivo run_app.bat e tente novamente.
  exit /b 1
)

"%PY_EXE%" -m streamlit run app.py
