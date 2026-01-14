import pandas as pd

def load_major_categories():
    df = pd.read_csv("data/CategoriasProgramasDeEstudio.csv", dtype=str, engine="python", on_bad_lines="warn")
    df_copy = df.copy()
    df_copy.columns = df_copy.columns.str.lower()

    #Convertir variables numéricas importantes
    numeric_cols = [
        'ramos matematicos',
        'ramos de ingles', 
        'ramos de lenguaje'
    ]
    for col in numeric_cols:
        if col in df_copy.columns:
            df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce') 

    return df_copy