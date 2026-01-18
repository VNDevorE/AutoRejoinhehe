@echo off
setlocal

echo ╔═══════════════════════════════════════════════════════════╗
echo ║        🎮  ROBLOX AUTO-REJOIN GIT SETUP  🎮             ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

:: Check for Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed!
    pause
    exit /b 1
)

:: Configuration
set REPO_URL=https://github.com/VNDevorE/AutoRejoinhehe.git

:: 1. Setup Identity if missing
git config user.name >nul 2>&1
if %errorlevel% neq 0 (
    set /p GIT_NAME="Enter your GitHub name: "
    git config --global user.name "%GIT_NAME%"
)

git config user.email >nul 2>&1
if %errorlevel% neq 0 (
    set /p GIT_EMAIL="Enter your GitHub email: "
    git config --global user.email "%GIT_EMAIL%"
)

:: 2. Initialize or Update Connection
if not exist .git (
    echo [INFO] Initializing new repository...
    git init
    git remote add origin %REPO_URL%
) else (
    echo [INFO] Updating remote connection...
    git remote set-url origin %REPO_URL%
)

:: 3. Commit and Push
echo [INFO] Syncing changes to GitHub...
git add .
git commit -m "AutoRejoin: Minimal Setup Update"
git branch -M main
git push -u origin main

echo.
echo ✅ GIT SETUP AND SYNC COMPLETED!
echo.
pause
