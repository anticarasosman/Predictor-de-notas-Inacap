import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def LoadPastStudentData():
    #Añadir las columnas de interes
    columns_of_interest = [
        'rut',
        'promedio notas matemáticas',
        'promedio notas lenguaje', 
        'promedio notas inglés',
        'año de ingreso',
        'carrera'
    ]
    
    df = pd.read_csv("data/Predictor Progresión O2025 03.03.csv", dtype=str, engine="python", on_bad_lines="warn")
    df_copia = df.copy()[columns_of_interest]

    #Limpiar RUT (igual que en results)
    df_copia = df_copia[df_copia["rut"].notna() & df_copia["rut"].str.contains(r"^\d", na=False)]

    #Modificar nombres de columnas para consistencia TODAS LAS COLUMNAS TENDRAN SUS NOMBRES EN MINUSCULAS
    df_copia.columns = df_copia.columns.str.lower()

    #Convertir variables numéricas importantes
    numeric_cols = [
        'promedio notas matemáticas',
        'promedio notas lenguaje', 
        'promedio notas inglés'
    ]
    for col in numeric_cols:
        if col in df_copia.columns:
            df_copia[col] = pd.to_numeric(df_copia[col], errors='coerce')
    
    return df_copia

if __name__ == "__main__":
    # Para probar el archivo directamente
    df = LoadPastStudentData()
