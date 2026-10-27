@echo off
rem proposito: versionar e enviar mudancas da biblioteca no repositorio dedicado
setlocal
cd /d "%~dp0.."
git add -A
if errorlevel 1 exit /b 1
git diff --cached --quiet
if errorlevel 1 (
  git commit -m "Atualizar biblioteca de skills"
  if errorlevel 1 exit /b 1
)
git push origin HEAD
exit /b %errorlevel%
