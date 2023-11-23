from os import system
from abc import ABC, abstractmethod
from peewee import SqliteDatabase, Model, AutoField, CharField
from extraer_datos import *
from modelo_orm import funcion_mapear_orm
from gestionar_obra import GestionarObra
from importar_csv import *

#FUNCIONES INDICADORES
#a. Listado de todas las áreas responsables.

Etapa, TipoObra, AreaResponsable, Comuna, Barrio, ContratacionTipo, Financiamiento, ObraUrbana = funcion_mapear_orm(db)



def listar_areas_responsables():
    # Obtener todas las áreas responsables
    db = funcion_conectar_db()
    areas_responsables = AreaResponsable.select()

    # Mostrar la lista de áreas responsables
    print("Listado de todas las áreas responsables:")
    for area in areas_responsables:
        print(area.nombre_area)
      
def listar_tipos_obra():
    areas_responsables = AreaResponsable.select()

        # Mostrar la lista de áreas responsables
    print("Listado de todas las áreas responsables:")
    for area in areas_responsables:
        print(area.nombre_area)
def contar_obras_por_etapa():
    etapas = Etapa.select()
    print("Cantidad de obras que se encuentran en cada etapa:")
    for etapa in etapas:
        cantidad_obras = ObraUrbana.select().where(ObraUrbana.etapa == etapa).count()
        print(f"{etapa.nombre_etapa}: {cantidad_obras} obras")

def contar_obras_tipo_monto_total():
    print("HOLA SOY M")
def listar_barrios_comunas_1_2_3():
    comunas_1_2_3 = Comuna.select().where(Comuna.nombre_comuna.in_(['1', '2', '3']))
    print("Listado de todos los barrios pertenecientes a las comunas 1, 2 y 3:")
    for comuna in comunas_1_2_3:
        barrios = Barrio.select().where(Barrio.comuna == comuna)
        for barrio in barrios:
            print(f"{comuna.nombre_comuna} - {barrio.nombre_barrio}")
def contar_obras_finalizadas_comuna_1():
    comuna_1 = Comuna.get(Comuna.nombre_comuna == '1')
    obras_finalizadas = ObraUrbana.select().where((ObraUrbana.comuna == comuna_1) & (ObraUrbana.etapa.nombre_etapa == 'Finalizada'))
    monto_total = ObraUrbana.select(fn.SUM(ObraUrbana.monto_contrato)).where((ObraUrbana.comuna == comuna_1) & (ObraUrbana.etapa.nombre_etapa == 'Finalizada')).scalar()
    print(f"Cantidad de obras finalizadas en la comuna 1: {obras_finalizadas.count()} - Monto total: {monto_total}")
def cantidad_obras_menor():
    obras_menor_24_meses = ObraUrbana.select().where(ObraUrbana.plazo_meses <= 24)
    print(f"Cantidad de obras finalizadas en un plazo menor o igual a 24 meses: {obras_menor_24_meses.count()}")

def calcular_porcentaje_obras_finalizadas():
    obras_finalizadas = ObraUrbana.select().where(ObraUrbana.etapa.nombre_etapa == 'Finalizada')
    obras_total = ObraUrbana.select().count()
    porcentaje = (obras_finalizadas.count() / obras_total) * 100
    print(f"Porcentaje total de obras finalizadas: {porcentaje:.2f}%")
def contar_mano_obra_total():
    mano_obra_total = ObraUrbana.select(fn.SUM(ObraUrbana.mano_obra)).scalar()
    print(f"Cantidad total de mano de obra empleada: {mano_obra_total} personas")

def calcular_monto_total_inversion():
    monto_total_inversion = ObraUrbana.select(fn.SUM(ObraUrbana.monto_contrato)).scalar()
    print(f"Monto total de inversión: ${monto_total_inversion}")


#MENU INDICADORES:

opciones = {
    'a': listar_areas_responsables,
    'b': listar_tipos_obra,
    'c': contar_obras_por_etapa,
    'd': contar_obras_tipo_monto_total,
    'e': listar_barrios_comunas_1_2_3,
    'f': contar_obras_finalizadas_comuna_1,
    'g': cantidad_obras_menor,
    'h': calcular_porcentaje_obras_finalizadas,
    'i': contar_mano_obra_total,
    'j': calcular_monto_total_inversion,
    's': listar_barrios_comunas_1_2_3,
}
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
    
    if opcion in opciones:
        opciones[opcion]()  # Llama a la función correspondiente
    elif opcion == 'q':
        print("Saliendo del programa. ¡Hasta luego!")
        break
    else:
        print("Opción no válida. Inténtalo de nuevo.")
    

