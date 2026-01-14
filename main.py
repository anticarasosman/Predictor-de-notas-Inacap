import sys
sys.path.append('load data')
sys.path.append('preprocessing')

from load_data import LoadResultsData
from load_data import LoadPastStudentData
from preprocessing import MergeDatasets

# Cargar los datos de resultados
print("\n========================================= Cargando datos de resultados =========================================")
df_results = LoadResultsData()
# Cargar los datos de entrenamiento
print("\n========================================= Cargando datos pasados =========================================")
df_past_data = LoadPastStudentData()

print("\n========================================= Combinando datos =========================================")
df_merged = MergeDatasets(df_past_data, df_results)
