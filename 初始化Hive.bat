@echo off
chcp 65001 >nul
echo ========================================
echo   初始化Hive数据仓库
echo ========================================
echo.

echo [1/3] 复制数据文件到容器...
docker cp data hive-server:/

echo.
echo [2/3] 创建Hive表结构...
docker exec -it hive-server hive -f /hive_scripts/create_tables.sql

echo.
echo [3/3] 导入示例数据...
docker exec -it hive-server hive -f /hive_scripts/load_data.sql

echo.
echo ========================================
echo   Hive数据仓库初始化完成！
echo ========================================
echo.

pause
