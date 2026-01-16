# Script para detectar si MySQL esta en el PATH
# No modifica nada, solo informa

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "        VERIFICADOR DE MYSQL EN PATH" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si mysql esta disponible en el PATH
$mysqlAvailable = $false
try {
    $result = cmd /c "mysql --version 2>&1"
    if ($LASTEXITCODE -eq 0) {
        $mysqlAvailable = $true
        Write-Host "Status: EXITO" -ForegroundColor Green
        Write-Host "MySQL ESTA en el PATH del sistema" -ForegroundColor Green
        Write-Host ""
        Write-Host "Version: $result"
        Write-Host ""
    }
}
catch {
    # MySQL no esta en el PATH
}

if (-not $mysqlAvailable) {
    Write-Host "Status: AVISO" -ForegroundColor Yellow
    Write-Host "MySQL NO esta en el PATH del sistema" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Para agregarlo, sigue estos pasos:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "OPCION 1: Agregarlo a traves de la interfaz grafica (Recomendado)" -ForegroundColor White
    Write-Host "  1. Presiona: Win + X" -ForegroundColor Gray
    Write-Host "  2. Selecciona: Sistema" -ForegroundColor Gray
    Write-Host "  3. Click en: Configuracion avanzada del sistema" -ForegroundColor Gray
    Write-Host "  4. Click en: Variables de entorno (parte inferior)" -ForegroundColor Gray
    Write-Host "  5. En Variables del sistema, busca: Path" -ForegroundColor Gray
    Write-Host "  6. Click en Editar" -ForegroundColor Gray
    Write-Host "  7. Click en: Nuevo" -ForegroundColor Gray
    Write-Host "  8. Copia y pega esta ruta:" -ForegroundColor Gray
    Write-Host ""
    Write-Host "     C:\Program Files\MySQL\MySQL Server 8.0\bin" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  9. Click en OK, OK, OK" -ForegroundColor Gray
    Write-Host " 10. Reinicia PowerShell completamente" -ForegroundColor Gray
    Write-Host " 11. Ejecuta este script de nuevo para verificar" -ForegroundColor Gray
    Write-Host ""
    Write-Host "OPCION 2: Usar en esta sesion de PowerShell (Temporal)" -ForegroundColor White
    Write-Host "  Ejecuta este comando:" -ForegroundColor Gray
    Write-Host ""
    Write-Host '  $env:Path += ";C:\Program Files\MySQL\MySQL Server 8.0\bin"' -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  (Solo funciona en esta sesion, se pierde al cerrar PowerShell)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "OPCION 3: Usar MySQL con ruta completa (Sin PATH)" -ForegroundColor White
    Write-Host "  Ejecuta:" -ForegroundColor Gray
    Write-Host ""
    Write-Host '  & "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql" -u root -e "SHOW DATABASES;"' -ForegroundColor Cyan
    Write-Host ""
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Información adicional
Write-Host "NOTA: Si MySQL esta en otra ruta distinta a C:\Program Files\MySQL\MySQL Server 8.0" -ForegroundColor Gray
Write-Host ""
