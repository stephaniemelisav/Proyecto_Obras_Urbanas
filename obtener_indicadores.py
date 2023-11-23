import pandas as pd
from peewee import Model, SqliteDatabase, CharField, IntegerField, FloatField

# Definir modelo Peewee para la tabla de obras
db = SqliteDatabase('obras_urbanas.db')

class Obra(Model):
    nombre = CharField()
    area_responsable = CharField()
    tipo_obra = CharField()
    etapa = CharField()
    comuna = IntegerField()
    barrio = CharField()
    fecha_inicio = CharField()
    fecha_fin = CharField()
    monto_contrato = FloatField()
    mano_obra = IntegerField()

    class Meta:
        database = db

# Definir la clase GestionarObra
class GestionarObra:

    def obtener_indicadores(cls):
        # Obtener todas las áreas responsables
        areas_responsables = Obra.select(Obra.area_responsable).distinct()

        # Obtener todos los tipos de obra
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
        print(f"Monto total de inversión: {monto_total_inversion}")

if __name__ == "__main__":
    GestionarObra.obtener_indicadores()
    

