import pandas as pd

def MergeDatasets(df_training, df_results):
    # Fusiona los datos de entrenamiento con los resultados.

    df_merged = pd.merge(df_training, df_results, left_on='RUT', right_on='RUT', how='inner')

    df_matematicas = df_merged[df_merged["Rinde Matemáticas"] == "SI"].copy()

    print(f"\nTotal después del merge: {len(df_merged)}")
    print(f"Estudiantes que rinden matemáticas: {len(df_matematicas)}")
    
    return df_matematicas

if __name__ == "__main__":
    # Para probar el archivo directamente
    df = MergeDatasets()