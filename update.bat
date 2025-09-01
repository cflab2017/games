@echo off
:: 작업할 폴더 경로로 이동
@REM cd /d D:\MyProject\GitRepo
cd c:\github\game

:: 현재 상태 출력
echo =========================
echo GitHub Update Start
echo =========================
git status

:: 원격 저장소 최신 내용 가져오기
git pull origin main

echo =========================
echo Update Complete
echo =========================
pause
