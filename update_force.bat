@echo off
@REM cd /d D:\MyProject\GitRepo
c:
cd c:\github\game

echo =========================
echo Force Update from GitHub
echo =========================
git fetch --all
git reset --hard origin/main

echo =========================
echo Update Complete
echo =========================
pause
