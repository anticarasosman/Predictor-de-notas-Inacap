import pandas as pd

src = "data/PredictorProgresiónEDvsPredictor.csv"
df = pd.read_csv(src, header=0, dtype=str, engine="python")

# Quédate solo con las 5 columnas esperadas (descarta cualquier extra vacía)
df = df.iloc[:, :5]
df.columns = ["RUT", "PREDICTOR", "Rinde Matemáticas", "Logro", "R/N"]

# Rellena vacíos en R/N con "NO"
df["R/N"] = df["R/N"].fillna("").replace("", "NO")

# Opcional: si Logro puede venir vacío, conviértelo a numérico conservando NaN
# df["Logro"] = pd.to_numeric(df["Logro"], errors="coerce")

df.to_csv(src, index=False)
print("CSV normalizado y guardado.")