@echo off
cd /d "c:\Users\thaiv\OneDrive\Desktop\AutoRejoin"
if exist .git rmdir /s /q .git
git init
git add .
git commit -m "AutoRejoin Release 1.0"
git branch -M main
git remote add origin https://github.com/VNDevorE/AutoRejoinhehe.git
echo SETUP COMPLETED SUCCESSFULLY!
