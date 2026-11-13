# راه‌اندازی کامل محیط توسعه با یک دستور.
# کلاستر پستگرس را بالا می‌آورد و بعد سرور جنگو را اجرا می‌کند.
# نمونه:  .\scripts\dev.ps1
#         .\scripts\dev.ps1 -Port 8001

param(
    [int]$Port = 8000
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path $PSScriptRoot -Parent
$python = Join-Path $projectRoot ".venv\Scripts\python.exe"
$manage = Join-Path $projectRoot "manage.py"

if (-not (Test-Path $python)) {
    throw "محیط مجازی پیدا نشد. اول python -m venv .venv و pip install -r requirements-dev.txt را اجرا کن."
}

if (-not (Test-Path $manage)) {
    throw "manage.py پیدا نشد. این اسکریپت را از ریشهٔ پروژه اجرا کن."
}

$env:PYTHONUTF8 = "1"

# ۱. دیتابیس
& (Join-Path $PSScriptRoot "dev-db.ps1") start

# ۲. بیلد استایل اگر فایل خروجی نیست
$css = Join-Path $projectRoot "static\css\app.css"
if (-not (Test-Path $css)) {
    Write-Host "ساخت استایل‌ها..."
    Push-Location $projectRoot
    try {
        & npx tailwindcss -i ./assets/css/main.css -o ./static/css/app.css --minify
    } finally {
        Pop-Location
    }
}

# ۳. سرور
Write-Host "سرور روی http://127.0.0.1:$Port بالا می‌آید. برای توقف Ctrl+C را بزن."
& $python $manage runserver "127.0.0.1:$Port" --noreload
