@echo off
echo Starting Music Recommendation System...

:: 检查 Python 是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8 or later from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 检查 Django 是否安装
python -c "import django" >nul 2>&1
if %errorlevel% neq 0 (
    echo Django is not installed
    echo Installing Django...
    pip install django
)

:: 检查其他依赖
echo Checking dependencies...
pip install -r requirements.txt

:: 执行数据库迁移
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate

:: 创建超级用户（如果不存在）
echo Checking superuser...
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123');
    print('Superuser created: admin/admin123');
"

:: 检查端口是否被占用
netstat -ano | findstr :8000 >nul
if %errorlevel% equ 0 (
    echo Port 8000 is already in use. Trying to kill the process...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
        taskkill /F /PID %%a
    )
    timeout /t 2
)

:: 启动 Django 服务器
echo Starting Django server...
echo Please wait while the server starts...
echo If you see any errors, please check:
echo 1. Python and Django are installed correctly
echo 2. All dependencies are installed
echo 3. Database is properly set up
echo.
echo Press Ctrl+C in the server window to stop the server
echo.

:: 使用 start 命令在新窗口中启动服务器
start cmd /k "python manage.py runserver"

:: 等待服务器启动
timeout /t 5

:: 打开浏览器
echo Opening browser...
start http://localhost:8000

echo System started successfully!
echo You can now access the website at http://localhost:8000
echo Login with admin/admin123
echo.
echo Press any key to exit this window...
pause >nul