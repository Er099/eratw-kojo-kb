@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ============================================
echo  Push AI knowledge base to GitHub
echo  Repo: github.com/Er099/eratw-kojo-kb
echo ============================================
echo.
echo Folder:
echo   %CD%
echo.

rem --- locate git.exe (WorkBuddy bundled PortableGit), no non-ASCII path typed ---
set "GITEXE="
for /d %%d in ("D:\*") do (
    if exist "%%~d\WorkBuddyAI\resources\vendor\PortableGit\cmd\git.exe" set "GITEXE=%%~d\WorkBuddyAI\resources\vendor\PortableGit\cmd\git.exe"
)
if not defined GITEXE (
    for /d %%d in ("C:\*") do (
        if exist "%%~d\WorkBuddyAI\resources\vendor\PortableGit\cmd\git.exe" set "GITEXE=%%~d\WorkBuddyAI\resources\vendor\PortableGit\cmd\git.exe"
    )
)
if not defined GITEXE set "GITEXE=git"

echo Git:
echo   %GITEXE%
echo.
"%GITEXE%" status -sb
echo.
echo --------------------------------------------
echo  A browser window may open for GitHub login.
echo  Sign in as Er099, then click "Authorize".
echo --------------------------------------------
echo.
"%GITEXE%" push -u origin main
set "RC=%errorlevel%"
echo.
if "%RC%"=="0" (
    echo [OK] Push finished. GitHub Pages updates in 1-2 minutes.
) else (
    echo [FAIL] Push failed, exit code %RC%. Read the messages above.
)
echo.
pause
