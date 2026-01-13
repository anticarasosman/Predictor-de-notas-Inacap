import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
path = "data/PredictorProgresiónEDvsPredictor.csv"
df = pd.read_csv(
    "data/PredictorProgresiónEDvsPredictor.csv",
    dtype=str,
    usecols=range(5),   # solo las primeras 5 columnas
    engine="python",    # parser más flexible
    on_bad_lines="warn" # opcional: avisa si descarta alguna fila
)
print("Columnas disponibles:")
print(df.columns.tolist())
print("\nPrimeras filas del dataset:")
print(df.head(10))
print("\nForma del dataset:")
print(df.shape)

# Eliminar filas con RUT vacío o invalido.
df = df[df["RUT"].notna() & df["RUT"].str.contains(r"^\d", na=False)]

# Limpiar espacios en blanco en nombres de columnas
df.columns = [c.strip() for c in df.columns]

# Convertir todos a minusculas para consistencias
df["Rinde Matematicas"] = df["Rinde Matematicas"].str.strip().str.upper()
df["Logro"] = pd.to_numeric(df["Logro"], errors='coerce')

print("Después de la limpieza:")
print(f"Registros válidos: {len(df)}")
print(f"\nEstudiantes que rinden matemáticas: {(df['Rinde Matematicas'] == 'SI').sum()}")
print(f"\nDistribución de logro:")
print(df['Logro'].describe())