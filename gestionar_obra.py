from os import system
from abc import ABC, abstractmethod
from peewee import *
from extraer_datos import *
from modelo_orm import *
from obtener_indicadores import *

#import extraer_datos as etl
#import modelo_ as 
# definición de la clase abstracta “GestionarObra”
class GestionarObra(ABC):
  dataFrame = None
  db = None
  Etapa = None
  TipoObra = None
  AreaResponsable = None
  Comuna = None
  Barrio = None
  ContratacionTipo = None
  Financiamiento = None
  ObraUrbana = None
  cantidad_obras_finalizadas = 0

  def __init__(self):
    pass
  
  @classmethod
  def extraer_datos(cls):
    cls.dataFrame = funcion_extraer_datos()

  @classmethod
  def conectar_db(cls):
    cls.db = funcion_conectar_db()


  @classmethod
  def mapear_orm(cls):
    # Guardamos en las variables de clase las clases que estan dentro de una funcion
    cls.Etapa, cls.TipoObra, cls.AreaResponsable, cls.Comuna, cls.Barrio, cls.ContratacionTipo, cls.Financiamiento, cls.ObraUrbana = funcion_mapear_orm(cls.db)
    """ db = GestionarObra.db
    Etapa = GestionarObra.Etapa
    TipoObra = GestionarObra.TipoObra
    AreaResponsable = GestionarObra.AreaResponsable
    Comuna = GestionarObra.Comuna
    Barrio = GestionarObra.Barrio
    ContratacionTipo = GestionarObra.ContratacionTipo
    Financiamiento = GestionarObra.Financiamiento
    ObraUrbana = GestionarObra.ObraUrbana """

  @classmethod
  def limpiar_datos(cls):
    cls.dataFrame = funcion_limpiar(cls.dataFrame)
    print("DataFrame limpio.")


  @classmethod
  def cargar_datos(cls):
    # Obtenemos valores únicos de cada columna.
    try:
      lista_etapas = list(GestionarObra.dataFrame['etapa'].unique())
      lista_tipoObras = list(GestionarObra.dataFrame['tipo'].unique())
      lista_area_resps = list(GestionarObra.dataFrame['area_responsable'].unique())
      lista_comunas = list(GestionarObra.dataFrame['comuna'].unique())
      lista_barrios = list(GestionarObra.dataFrame['barrio'].unique())
      lista_contratacion = list(GestionarObra.dataFrame['contratacion_tipo'].unique())
      lista_financiamiento = list(GestionarObra.dataFrame['financiamiento'].unique())
      print("Valores únicos por columna obtenidos correctamente.")
    except Exception as e:
       print("No se obtuvieron los valores únicos",e)

    # ---------------------------  Cargamos tablas de consulta (lookups) -------------------
    for elem in lista_etapas:
        try:
            GestionarObra.Etapa.create(nombre_etapa = elem)
        except IntegrityError as e:
            print("Error al insertar un nuevo registro en la tabla Etapa", e)
    print("Se han persistido las etapas en la BD.")
       
    for elem in lista_tipoObras:
        try:
            GestionarObra.TipoObra.create(tipo_obra = elem)
        except IntegrityError as e:
            print("Error al insertar un nuevo registro en la tabla TipoObra", e)
    print("Se han persistido los tipos de obras en la BD.")

    for elem in lista_area_resps:
        try:
            GestionarObra.AreaResponsable.create(nombre_area = elem)
        except IntegrityError as e:
            print("Error al insertar un nuevo registro en la tabla AreaResponsable", e)
    print("Se han persistido las áreas responsables en la BD.")

    for elem in lista_comunas:
        try:
            GestionarObra.Comuna.create(nombre_comuna = elem)
        except IntegrityError as e:
            print("Error al insertar un nuevo registro en la tabla Comuna", e)
    print("Se han persistido las comunas en la BD.")

    for elem in lista_barrios:
        try:
            GestionarObra.Barrio.create(nombre_barrio = elem)
        except IntegrityError as e:
            print("Error al insertar un nuevo registro en la tabla Barrio", e)
    print("Se han persistido los barrios en la BD.")

    for elem in lista_contratacion:
        try:
            GestionarObra.ContratacionTipo.create(contratacion = elem)
        except IntegrityError as e:
            print("Error al insertar un nuevo registro en la tabla ContratacionTipo", e)
    print("Se han persistido los tipos de contrataciones en la BD.")

    for elem in lista_financiamiento:
        try:
            GestionarObra.Financiamiento.create(financiamiento = elem)
        except IntegrityError as e:
            print("Error al insertar un nuevo registro en la tabla Financiamiento", e)
    print("Se han persistido los financiamientos en la BD.")


    # Cargamos la tabla principal ObraUrbana
    print("cargando registros en tabla ObraUrbana...")
    cargando = ""
    for elem in GestionarObra.dataFrame.values:
        # En vista de que tarda mucho, imprimimos un punto por cada iteracion para emular carga
        cargando = cargando + "."
        print(cargando)
        # Se obtiene el id de la tabla lookup y lo guardamos en una variable.
        fk_etapa = GestionarObra.Etapa.get(GestionarObra.Etapa.nombre_etapa == elem[2])
        fk_obra = GestionarObra.TipoObra.get(GestionarObra.TipoObra.tipo_obra == elem[3])
        fk_area_resp = GestionarObra.AreaResponsable.get(GestionarObra.AreaResponsable.nombre_area == elem[4])
        fk_comuna = GestionarObra.Comuna.get(GestionarObra.Comuna.nombre_comuna == elem[7])
        fk_barrio = GestionarObra.Barrio.get(GestionarObra.Barrio.nombre_barrio == elem[8])
        fk_contratacion = GestionarObra.ContratacionTipo.get(GestionarObra.ContratacionTipo.contratacion == elem[17])
        fk_financiamiento = GestionarObra.Financiamiento.get(GestionarObra.Financiamiento.financiamiento == elem[23])
        try:
            GestionarObra.ObraUrbana.create(entorno=elem[0], #elem[indice] hace referencia a la columna del dataframe
                                  nombre=elem[1],
                                  etapa=fk_etapa,
                                  tipo_obra=fk_obra,
                                  area_responsable=fk_area_resp,
                                  descripcion=elem[5],
                                  monto_contrato=elem[6],
                                  comuna=fk_comuna,
                                  barrio=fk_barrio,
                                  direccion=elem[9],
                                  fecha_inicio=elem[10],
                                  fecha_fin_inicial=elem[11],
                                  plazo_meses=elem[12],
                                  porcentaje_avance=elem[13],
                                  imagen=elem[14],
                                  licitacion_oferta_empresa=elem[15],
                                  licitacion_anio=elem[16],
                                  contratacion_tipo=fk_contratacion,
                                  nro_contratacion=elem[18],
                                  cuit_contratista=elem[19],
                                  mano_obra=elem[20],
                                  destacada=elem[21],
                                  expediente_numero=elem[22],
                                  financiamiento=fk_financiamiento
                                  )
        except IntegrityError as e:
            print("Error al insertar un nuevo registro en la tabla ObraUrbana.", e)
    system('cls')
    print("Se han persistido correctamente los registros en la BD.")



  @classmethod
  def nueva_obra(cls):
    pass

  @classmethod

  def obtener_indicadores(cls):
    # Obtener todas las áreas responsables
    while True:
      print("\nMenú:")
      print("a. Listado de todas las áreas responsables.")
      print("b. Listado de todos los tipos de obra.")
      print("c. Cantidad de obras que se encuentran en cada etapa.")
      print("d. Cantidad de obras y monto total de inversión por tipo de obra.")
      print("e. Listado de todos los barrios pertenecientes a las comunas 1, 2 y 3.")
      print("f. Cantidad de obras finalizadas y su y monto total de inversión en la comuna 1.")
      print("g. Cantidad de obras finalizadas en un plazo menor o igual a 24 meses.")
      print("h. Porcentaje total de obras finalizadas.")
      print("i. Cantidad total de mano de obra empleada.")
      print("j. Monto total de inversión.")
      print("s. Salir")

      opcion = input("Selecciona una opción (a-j) o q para salir: ").lower()
    
      while True:
        if opcion == 'a':
          n=1
          areas_responsables = list(GestionarObra.dataFrame['area_responsable'].unique())
          print("\nListado de todas las áreas responsables\t")
          for area_responsable in areas_responsables:
            print(n,area_responsable)
            n+=1
        elif opcion == 'b':
          n=1
          # Obtener todos los tipos de obra
          tipos_obra =list(GestionarObra.dataFrame['tipo'].unique())

          # Imprimir la lista de tipos de obra
          print("\nListado de todos los tipos de obra:\t")
          for tipos_obra in tipos_obra:
            print(n,tipos_obra)
            n+=1
          break
          
          
        elif opcion == 'c':
          areas_responsables = list(GestionarObra.dataFrame['area_responsable'].unique())
          print(areas_responsables)
          break
        elif opcion == 'd':
          areas_responsables = list(GestionarObra.dataFrame['area_responsable'].unique())
          print(areas_responsables)
          break
        else:
          print("incorrecto")
    

    """     # Obtener todos los tipos de obra
    tipos_obra = Obra.select(Obra.tipo_obra).distinct()

        # Cantidad de obras en cada etapa
    obras_por_etapa = Obra.select(Obra.etapa, fn.COUNT(Obra.id).alias('cantidad')).group_by(Obra.etapa)

        # Cantidad de obras y monto total de inversión por tipo de obra
    obras_por_tipo = Obra.select(Obra.tipo_obra, fn.COUNT(Obra.id).alias('cantidad'), fn.SUM(Obra.monto_contrato).alias('monto_total')).group_by(Obra.tipo_obra)

        # Listado de barrios pertenecientes a las comunas 1, 2 y 3
    barrios_comunas_1_2_3 = Obra.select(Obra.barrio).where(Obra.comuna.in_([1, 2, 3])).distinct()

        # Cantidad de obras finalizadas y monto total de inversión en la comuna 1
    obras_finalizadas_comuna_1 = Obra.select().where((Obra.comuna == 1) & (Obra.etapa == 'Finalizada'))
    cantidad_obras_finalizadas_comuna_1 = obras_finalizadas_comuna_1.count()
    monto_total_inversion_comuna_1 = obras_finalizadas_comuna_1.select(fn.SUM(Obra.monto_contrato)).scalar()

        # Cantidad de obras finalizadas en un plazo menor o igual a 24 meses
    obras_finalizadas_24_meses = Obra.select().where((Obra.etapa == 'Finalizada') & (Obra.duracion <= 24)).count()

        # Porcentaje total de obras finalizadas
    total_obras = Obra.select().count()
    porcentaje_obras_finalizadas = (cantidad_obras_finalizadas / total_obras) * 100

        # Cantidad total de mano de obra empleada
    total_mano_obra = Obra.select(fn.SUM(Obra.mano_obra)).scalar()

        # Monto total de inversión
    monto_total_inversion = Obra.select(fn.SUM(Obra.monto_contrato)).scalar()

        # Mostrar los resultados por consola
    print("a. Listado de todas las áreas responsables:")
    for area_responsable in areas_responsables:
      print(area_responsable.area_responsable)

      print("\nb. Listado de todos los tipos de obra:")
    for tipo_obra in tipos_obra:
      print(tipo_obra.tipo_obra)

      print("\nc. Cantidad de obras que se encuentran en cada etapa:")
    for obra_por_etapa in obras_por_etapa:
      print(f"{obra_por_etapa.etapa}: {obra_por_etapa.cantidad} obras")

      print("\nd. Cantidad de obras y monto total de inversión por tipo de obra:")
    for obra_por_tipo in obras_por_tipo:
      print(f"{obra_por_tipo.tipo_obra}: {obra_por_tipo.cantidad} obras, Monto total: {obra_por_tipo.monto_total}")

      print("\ne. Listado de todos los barrios pertenecientes a las comunas 1, 2 y 3:")
    for barrio in barrios_comunas_1_2_3:
      print(barrio.barrio)

      print("\nf. Cantidad de obras finalizadas y su monto total de inversión en la comuna 1:")
      print(f"Cantidad de obras finalizadas en la comuna 1: {cantidad_obras_finalizadas_comuna_1}")
      print(f"Monto total de inversión en la comuna 1: {monto_total_inversion_comuna_1}")

      print("\ng. Cantidad de obras finalizadas en un plazo menor o igual a 24 meses:")
      print(f"Cantidad de obras finalizadas en 24 meses o menos: {obras_finalizadas_24_meses}")

      print("\nh. Porcentaje total de obras finalizadas:")
      print(f"Porcentaje de obras finalizadas: {porcentaje_obras_finalizadas}%")

      print("\ni. Cantidad total de mano de obra empleada:")
      print(f"Cantidad total de mano de obra: {total_mano_obra}")

      print("\nj. Monto total de inversión:")
      print(f"Monto total de inversión: {monto_total_inversion}")    """ 
    
    """ def opcion_indicadores():
      pass
     
    pass
    mostrar por consola la siguiente información:
    a. Listado de todas las áreas responsables.
    b. Listado de todos los tipos de obra.
    c. Cantidad de obras que se encuentran en cada etapa.
    d. Cantidad de obras y monto total de inversión por tipo de obra.
    e. Listado de todos los barrios pertenecientes a las comunas 1, 2 y 3.
    f. Cantidad de obras finalizadas y su y monto total de inversión en la comuna 1.
    g. Cantidad de obras finalizadas en un plazo menor o igual a 24 meses.
    h. Porcentaje total de obras finalizadas.
    i. Cantidad total de mano de obra empleada.
    j. Monto total de inversión. """
    
  
  
if __name__ == "__main__":
    try:
        GestionarObra.extraer_datos()
        GestionarObra.conectar_db()
        GestionarObra.mapear_orm()
        GestionarObra.limpiar_datos()
        GestionarObra.cargar_datos()
        # Llamar al método de clase para obtener e imprimir los indicadores
       
    except Exception as e:
        print(e)
    GestionarObra.obtener_indicadores()