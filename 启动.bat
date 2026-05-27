@echo off
chcp 65001 >nul
echo ========================================
echo   农产品质量安全追溯与分析系统 - 启动
echo ========================================
echo.

echo [1/4] 检查Docker是否运行...
docker info >nul 2>&1
if errorlevel 1 (
    echo [错误] Docker未运行，请先启动Docker Desktop！
    pause
    exit /b 1
)
echo Docker运行正常！

echo.
echo [2/4] 正在构建并启动Docker容器...
docker-compose up -d --build

echo.
echo [3/4] 等待服务启动（约90秒）...
echo 请耐心等待，Hive初始化需要一些时间...
timeout /t 90 /nobreak

echo.
echo [4/4] 检查服务状态...
docker ps --format "table {{.Names}}\t{{.Status}}"

echo.
echo ========================================
echo   Docker服务启动完成！
echo.
echo   服务访问地址：
echo   - Hadoop NameNode: http://localhost:9870
echo   - Spark Master:    http://localhost:8080
echo   - HiveServer2:     localhost:10000
echo ========================================
echo.
echo 正在安装Python依赖...
pip install flask pandas -q

echo.
echo 正在启动Flask Web应用...
echo 启动后请访问: http://localhost:5000
echo.

cd flask_app
python app.py

pause
