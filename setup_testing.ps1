# Script para instalar dependencias y ejecutar tests en Windows (PowerShell)

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║           SETUP TESTING - Base de Datos INACAP                ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Verificar si Python está instalado
try {
    python --version | Out-Null
    Write-Host "✓ Python detectado" -ForegroundColor Green
} catch {
    Write-Host "✗ Python no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "  Descárgalo desde: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""

# Instalar dependencias
Write-Host "Instalando dependencias..." -ForegroundColor Yellow
Write-Host ""

pip install -r requirements-testing.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Error al instalar dependencias" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
Write-Host "✓ Dependencias instaladas correctamente" -ForegroundColor Green
Write-Host ""

# Menu de opciones
function Show-Menu {
    Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "SELECCIONA UNA OPCION:" -ForegroundColor Cyan
    Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Ejecutar TODOS los tests"
    Write-Host "2. Ejecutar solo tests de DATOS VALIDOS"
    Write-Host "3. Ejecutar solo tests de DATOS INVALIDOS"
    Write-Host "4. Ejecutar solo tests de CASCADE/RESTRICT"
    Write-Host "5. Ver EJEMPLOS PRACTICOS"
    Write-Host "6. Ejecutar tests con output DETALLADO (con -s flag)"
    Write-Host "7. Generar reporte de COBERTURA"
    Write-Host "8. Salir"
    Write-Host ""
}

$choice = 0
while ($true) {
    Show-Menu
    $choice = Read-Host "Ingresa tu opción (1-8)"
    
    switch ($choice) {
        "1" {
            Write-Host ""
            Write-Host "Ejecutando TODOS los tests..." -ForegroundColor Yellow
            pytest test_database.py -v
            Read-Host "Presiona Enter para continuar"
        }
        "2" {
            Write-Host ""
            Write-Host "Ejecutando tests de DATOS VALIDOS..." -ForegroundColor Yellow
            pytest test_database.py::TestInsertarDatosValidos -v
            Read-Host "Presiona Enter para continuar"
        }
        "3" {
            Write-Host ""
            Write-Host "Ejecutando tests de DATOS INVALIDOS..." -ForegroundColor Yellow
            pytest test_database.py::TestInsertarDatosInvalidos -v
            Read-Host "Presiona Enter para continuar"
        }
        "4" {
            Write-Host ""
            Write-Host "Ejecutando tests de CASCADE/RESTRICT..." -ForegroundColor Yellow
            pytest test_database.py::TestConstraintsCascadeRestrict -v
            Read-Host "Presiona Enter para continuar"
        }
        "5" {
            Write-Host ""
            Write-Host "Ejecutando EJEMPLOS PRACTICOS..." -ForegroundColor Yellow
            python ejemplos_testing.py
            Read-Host "Presiona Enter para continuar"
        }
        "6" {
            Write-Host ""
            Write-Host "Ejecutando todos los tests con output DETALLADO..." -ForegroundColor Yellow
            pytest test_database.py -v -s
            Read-Host "Presiona Enter para continuar"
        }
        "7" {
            Write-Host ""
            Write-Host "Generando reporte de cobertura..." -ForegroundColor Yellow
            Write-Host "(Primero instalando pytest-cov...)" -ForegroundColor Gray
            pip install pytest-cov
            pytest test_database.py --cov=. --cov-report=html
            Write-Host ""
            Write-Host "✓ Reporte generado en: htmlcov/index.html" -ForegroundColor Green
            Read-Host "Presiona Enter para continuar"
        }
        "8" {
            Write-Host ""
            Write-Host "¡Hasta luego!" -ForegroundColor Green
            exit 0
        }
        default {
            Write-Host ""
            Write-Host "✗ Opción no válida" -ForegroundColor Red
            Write-Host ""
        }
    }
}
