@echo off
setlocal
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo Instale Python com Tkinter: winget install --id Python.Python.3.13 --exact
  echo Depois abra este arquivo novamente em um novo terminal.
  pause
  exit /b 1
)
python -c "import tkinter" >nul 2>nul
if errorlevel 1 (
  echo Python ou Tkinter indisponivel. Instale Python de python.org com Tcl/Tk.
  pause
  exit /b 1
)
python app.py
if errorlevel 1 pause
