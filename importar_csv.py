import pandas as pd

# función que retorna el dataset si la ruta hacia dicho dataset es correcto.
def importar_datos_csv():
  # se asigna ruta local a variable.
  fichero_csv = "observatorio-de-obras-urbanas.csv"

  # se hace un control de excepción por si dicho fichero no se encuentra.
  try:
    dataframe = pd.read_csv(fichero_csv)
    return dataframe
  except FileNotFoundError as e:
    print("Error. El dataset no fue encontrado.")
    return False