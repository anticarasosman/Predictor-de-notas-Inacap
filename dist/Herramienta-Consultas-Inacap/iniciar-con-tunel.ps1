# Script para iniciar aplicación con túnel SSH (Red Corporativa)
# Uso: .\iniciar-con-tunel.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  HERRAMIENTA INACAP - RED CORPORATIVA  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que exista el archivo .pem
if (-Not (Test-Path "tunnel-inacap.pem")) {
    Write-Host "[ERROR] No se encuentra el archivo 'tunnel-inacap.pem'" -ForegroundColor Red
    Write-Host "Coloca el archivo .pem en la misma carpeta que este script." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Verificar que exista el .env.tunnel
if (-Not (Test-Path ".env.tunnel")) {
    Write-Host "[ERROR] No se encuentra el archivo '.env.tunnel'" -ForegroundColor Red
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Copiar .env.tunnel a .env
Write-Host "[1/4] Configurando archivo .env para red corporativa..." -ForegroundColor Yellow
Copy-Item ".env.tunnel" ".env" -Force
Write-Host "[OK] Configuracion lista" -ForegroundColor Green
Write-Host ""

# Verificar si ya hay un túnel activo
Write-Host "[2/4] Verificando tunel SSH..." -ForegroundColor Yellow
$tunnel = Get-Process -Name "ssh" -ErrorAction SilentlyContinue | Where-Object {$_.CommandLine -like "*3307*"}

if ($tunnel) {
    Write-Host "[OK] Tunel SSH ya esta activo" -ForegroundColor Green
} else {
    Write-Host "Iniciando tunel SSH en puerto 443..." -ForegroundColor Yellow
    
    # Iniciar túnel en segundo plano
    Start-Process -FilePath "ssh" -ArgumentList @(
        "-p", "443",
        "-o", "StrictHostKeyChecking=no",
        "-i", "tunnel-inacap.pem",
        "-L", "3307:base-de-datos-inacap.cxeouo22gw7q.sa-east-1.rds.amazonaws.com:3306",
        "ec2-user@18.228.10.215",
        "-N"
    ) -WindowStyle Hidden
    
    Write-Host "Esperando 3 segundos para establecer conexion..." -ForegroundColor Yellow
    Start-Sleep -Seconds 3
    Write-Host "[OK] Tunel SSH iniciado (localhost:3307 -> RDS:3306)" -ForegroundColor Green
}
Write-Host ""

# Ejecutar la aplicación
Write-Host "[3/4] Iniciando aplicacion..." -ForegroundColor Yellow
Write-Host ""

# Usar la ruta completa del script para saber dónde estamos
$scriptDir = Split-Path -Parent $PSCommandPath
$exePath = Join-Path $scriptDir "Herramienta-Consultas-Inacap.exe"

if (Test-Path $exePath) {
    try {
        # Cambiar al directorio del script
        Push-Location $scriptDir
        
        # Ejecutar el .exe desde la carpeta correcta
        & $exePath
        
        Pop-Location
        Write-Host "[OK] Aplicacion iniciada con tunel SSH" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] No se pudo iniciar la aplicacion: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Intenta ejecutar manualmente: $exePath" -ForegroundColor Yellow
    }
} else {
    Write-Host "[ERROR] No se encuentra 'Herramienta-Consultas-Inacap.exe'" -ForegroundColor Red
    Write-Host "Ruta esperada: $exePath" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[4/4] Proceso completado" -ForegroundColor Green
Write-Host ""
Write-Host "NOTA: El tunel SSH quedara activo en segundo plano." -ForegroundColor Cyan
Write-Host "      Para cerrarlo, abre el Administrador de Tareas y finaliza" -ForegroundColor Cyan
Write-Host "      el proceso 'ssh.exe' cuando termines de usar la aplicacion." -ForegroundColor Cyan
Write-Host ""
Write-Host "Presiona Enter para cerrar esta ventana..." -ForegroundColor Gray
Read-Host
