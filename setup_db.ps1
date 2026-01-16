# setup_db.ps1
# Script PowerShell para ejecutar setup de la base de datos
# REQUISITO: Haber ejecutado previamente:
#   mysql_config_editor.exe set --login-path=local --host=localhost --user=root --password

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Iniciando setup de base de datos" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Rutas
$mysqlPath = "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"
$setupFile = "C:\Users\gstaudt\Desktop\Predictor-de-notas-Inacap\database\set_up.sql"

# Verificar que los archivos existen
if (-not (Test-Path $mysqlPath)) {
    Write-Host "❌ ERROR: No se encontró MySQL en $mysqlPath" -ForegroundColor Red
    Read-Host "Presiona ENTER para cerrar"
    exit
}

if (-not (Test-Path $setupFile)) {
    Write-Host "❌ ERROR: No se encontró el archivo de setup en $setupFile" -ForegroundColor Red
    Read-Host "Presiona ENTER para cerrar"
    exit
}

# Ejecutar
try {
    Write-Host "Ejecutando setup..." -ForegroundColor Yellow
    Get-Content $setupFile | & $mysqlPath --login-path=local
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "===================================" -ForegroundColor Green
        Write-Host "[OK] Base de datos creada exitosamente!" -ForegroundColor Green
        Write-Host "===================================" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "===================================" -ForegroundColor Red
        Write-Host "[ERROR] Hubo un problema al crear la base de datos" -ForegroundColor Red
        Write-Host "===================================" -ForegroundColor Red
    }
} catch {
    Write-Host ""
    Write-Host "❌ Error: $_" -ForegroundColor Red
}

Write-Host ""
Read-Host "Presiona ENTER para cerrar"
