@echo off
chcp 65001 >nul
title Deep Search Pro
cd /d "%~dp0"

echo ========================================
echo   Deep Search Pro 正在启动
echo   访问地址: http://127.0.0.1:8002/
echo ========================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [错误] 没有找到 Python 虚拟环境：.venv\Scripts\python.exe
    echo 请先在项目目录安装依赖。
    echo.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" -m uvicorn api.server:app --host 127.0.0.1 --port 8002

echo.
echo [提示] 服务已经停止，退出代码：%errorlevel%
echo 如果上方显示端口被占用，请先关闭旧的 Deep Search Pro 窗口。
pause
