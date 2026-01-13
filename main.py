import panda as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
path = "data/PredictorProgresionEDvsPredictor.csv"
df = pd.read_csv(path, dtype=str)
print(df.columns.tolist())
print(df.head(10))
print(df.shape)

# Eliminar filas sin RUT válido (ej: vacio o texto no numérico)
df = df[df['RUT'].notna() & df["RUT"].str.contains(r"\d", na=False)]

# Normalizamos nombres de columnas
df.columns = [c.strip() for c in df.columns]

# Filtrar alumnos que rindieron Matematica
df_math = df[df['Rinde Matemáticas'].str.upper() == 'SI'].copy()

# Convertir columna 'Logro' a numérico