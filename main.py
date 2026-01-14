import sys
sys.path.append('load data')
sys.path.append('preprocessing')

from load_data import LoadPastStudentData

# Cargar los datos de entrenamiento
print("\n========================================= Cargando datos pasados =========================================")
df_past_data = LoadPastStudentData()
