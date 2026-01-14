import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def load_past_student_data():
    #Añadir las columnas de interes
    columns_of_interest = [
        'rut',
        "nombre",
        "programa de estudio",
        "promedio notas matemáticas",
        "promedio notas lenguaje",
        "promedio notas inglés"
    ]
    
    df = pd.read_csv("data/Predictor Progresión O2025 03.03.csv", dtype=str, engine="python", on_bad_lines="warn")
    df.columns = df.columns.str.lower()
    df_copy = df.copy()[columns_of_interest]

    #Limpiar RUT (igual que en results)
    df_copy = df_copy[df_copy["rut"].notna() & df_copy["rut"].str.contains(r"^\d", na=False)]

    #Modificar nombres de columnas para consistencia TODAS LAS COLUMNAS TENDRAN SUS NOMBRES EN MINUSCULAS
    df_copy.columns = df_copy.columns.str.lower()

    #Convertir variables numéricas importantes
    numeric_cols = [
        'promedio notas matemáticas',
        'promedio notas lenguaje', 
        'promedio notas inglés'
    ]
    for col in numeric_cols:
        if col in df_copy.columns:
            df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce')
    
    return df_copy

if __name__ == "__main__":
    # Para probar el archivo directamente
    df = load_past_student_data()
