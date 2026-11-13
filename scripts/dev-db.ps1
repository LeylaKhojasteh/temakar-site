# مدیریت کلاستر پستگرس محلی پروژه (فقط توسعه).
# نمونه استفاده:
#   .\scripts\dev-db.ps1 init
#   .\scripts\dev-db.ps1 start
#   .\scripts\dev-db.ps1 status
#   .\scripts\dev-db.ps1 stop

param(
    [ValidateSet("init", "start", "stop", "status")]
    [string]$Action = "status"
)

$ErrorActionPreference = "Stop"

$postgresBin = "C:\Program Files\PostgreSQL\18\bin"
$pgCtl = Join-Path $postgresBin "pg_ctl.exe"
$initdb = Join-Path $postgresBin "initdb.exe"
$createdb = Join-Path $postgresBin "createdb.exe"
$psql = Join-Path $postgresBin "psql.exe"

$projectRoot = Split-Path $PSScriptRoot -Parent
$dataDirectory = Join-Path $projectRoot ".pgdata"
$databaseName = "temakar"
$databaseUser = "temakar"
$databasePort = "5439"

if (-not (Test-Path $pgCtl)) {
    throw "PostgreSQL tools not found: $postgresBin"
}

function Invoke-PsqlQuiet {
    param([string[]]$PgArguments)
    $previous = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        & $psql @PgArguments *> $null
        return $LASTEXITCODE -eq 0
    } finally {
        $ErrorActionPreference = $previous
    }
}

function Initialize-Cluster {
    if (Test-Path $dataDirectory) {
        Write-Host "Cluster already exists: $dataDirectory"
        return
    }
    & $initdb -D $dataDirectory -U $databaseUser --auth=trust --encoding=UTF8 --locale=C | Out-Null
    $configLines = @(
        "",
        "port = $databasePort",
        "listen_addresses = '127.0.0.1'",
        "logging_collector = on",
        "log_directory = 'log'",
        "log_filename = 'postgresql-%Y-%m-%d.log'",
        "log_rotation_age = 1d"
    )
    Add-Content -Path (Join-Path $dataDirectory "postgresql.conf") -Encoding ascii -Value $configLines
    Write-Host "Cluster created on port $databasePort"
}

function Test-Connection {
    return Invoke-PsqlQuiet @("-h", "127.0.0.1", "-p", $databasePort, "-U", $databaseUser, "-d", "postgres", "-tAc", "select 1;")
}

function Start-Cluster {
    if (Test-Connection) {
        Write-Host "Cluster is already running."
        return
    }
    # استارت از طریق WMI تا سرور به کنسول این اسکریپت وابسته نماند.
    $commandLine = 'cmd.exe /c ""' + $pgCtl + '" -D "' + $dataDirectory + '" start"'
    $result = ([wmiclass]"Win32_Process").Create($commandLine)
    if ($result.ReturnValue -ne 0) {
        throw "pg_ctl failed with code $($result.ReturnValue)"
    }
    for ($attempt = 0; $attempt -lt 30; $attempt++) {
        Start-Sleep -Seconds 1
        if (Test-Connection) {
            Write-Host "Cluster is ready on port $databasePort."
            return
        }
    }
    throw "Cluster did not start. Check .pgdata\server.log"
}

function Ensure-Database {
    $previous = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $found = & $psql -h 127.0.0.1 -p $databasePort -U $databaseUser -d postgres -tAc "select 1 from pg_database where datname = '$databaseName';" 2>$null
    } finally {
        $ErrorActionPreference = $previous
    }
    if (-not ($found | Out-String).Trim()) {
        & $createdb -h 127.0.0.1 -p $databasePort -U $databaseUser $databaseName
        Write-Host "Database $databaseName created."
    }
}

switch ($Action) {
    "init" {
        Initialize-Cluster
        Start-Cluster
        Ensure-Database
    }
    "start" {
        Start-Cluster
        Ensure-Database
    }
    "stop" {
        & $pgCtl -D $dataDirectory stop -m fast
    }
    "status" {
        & $pgCtl -D $dataDirectory status
    }
}
