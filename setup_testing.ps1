# Script para instalar dependencias y ejecutar tests en Windows (PowerShell)

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "        SETUP TESTING - Base de Datos INACAP" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si Python esta instalado
$pythonCheck = cmd /c python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "Exito: Python detectado" -ForegroundColor Green
} else {
    Write-Host "Error: Python no esta instalado o no esta en el PATH" -ForegroundColor Red
    Write-Host "Descargalo desde: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""

# Instalar dependencias
Write-Host "Instalando dependencias..." -ForegroundColor Yellow
Write-Host ""

pip install -r requirements-testing.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error al instalar dependencias" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
Write-Host "Exito: Dependencias instaladas correctamente" -ForegroundColor Green
Write-Host ""

# Menu interactivo
$continuar = $true

while ($continuar) {
    Write-Host "======================================================================" -ForegroundColor Cyan
    Write-Host "SELECCIONA UNA OPCION:" -ForegroundColor Cyan
    Write-Host "======================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Ejecutar TODOS los tests"
    Write-Host "2. Ejecutar solo tests de DATOS VALIDOS"
    Write-Host "3. Ejecutar solo tests de DATOS INVALIDOS"
    Write-Host "4. Ejecutar solo tests de CASCADE/RESTRICT"
    Write-Host "5. Ver EJEMPLOS PRACTICOS"
    Write-Host "6. Ejecutar tests con output DETALLADO"
    Write-Host "7. Generar reporte de COBERTURA"
    Write-Host "8. Salir"
    Write-Host ""
    
    $choice = Read-Host "Ingresa tu opcion (1-8)"
    
    Write-Host ""
    
    if ($choice -eq "1") {
        Write-Host "Ejecutando TODOS los tests..." -ForegroundColor Yellow
        pytest test_database.py -v
        Read-Host "Presiona Enter para continuar"
    }
    elseif ($choice -eq "2") {
        Write-Host "Ejecutando tests de DATOS VALIDOS..." -ForegroundColor Yellow
        pytest test_database.py::TestInsertarDatosValidos -v
        Read-Host "Presiona Enter para continuar"
    }
    elseif ($choice -eq "3") {
        Write-Host "Ejecutando tests de DATOS INVALIDOS..." -ForegroundColor Yellow
        pytest test_database.py::TestInsertarDatosInvalidos -v
        Read-Host "Presiona Enter para continuar"
    }
    elseif ($choice -eq "4") {
        Write-Host "Ejecutando tests de CASCADE/RESTRICT..." -ForegroundColor Yellow
        pytest test_database.py::TestConstraintsCascadeRestrict -v
        Read-Host "Presiona Enter para continuar"
    }
    elseif ($choice -eq "5") {
        Write-Host "Ejecutando EJEMPLOS PRACTICOS..." -ForegroundColor Yellow
        python ejemplos_testing.py
        Read-Host "Presiona Enter para continuar"
    }
    elseif ($choice -eq "6") {
        Write-Host "Ejecutando todos los tests con output DETALLADO..." -ForegroundColor Yellow
        pytest test_database.py -v -s
        Read-Host "Presiona Enter para continuar"
    }
    elseif ($choice -eq "7") {
        Write-Host "Generando reporte de cobertura..." -ForegroundColor Yellow
        Write-Host "(Instalando pytest-cov...)" -ForegroundColor Gray
        pip install pytest-cov
        pytest test_database.py --cov=. --cov-report=html
        Write-Host ""
        Write-Host "Exito: Reporte generado en htmlcov/index.html" -ForegroundColor Green
        Read-Host "Presiona Enter para continuar"
    }
    elseif ($choice -eq "8") {
        Write-Host "Hasta luego!" -ForegroundColor Green
        $continuar = $false
    }
    else {
        Write-Host "Opcion no valida" -ForegroundColor Red
    }
    
    Write-Host ""
}
