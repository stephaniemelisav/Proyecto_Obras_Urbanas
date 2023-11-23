# -*- coding: utf-8 -*-
#@author: Barnes Lopez - Muñoz - Ozuna - Roel - Velarde
import pandas as pd
import unicodedata
import re

def funcion_extraer_datos():
    try:
        df = pd.read_csv('observatorio-de-obras-urbanas.csv', encoding = 'UTF-8')
        print("Datos extraidos correctamente.")
    except Exception as e:
        print("Error al extraer datos ,", e)
    return df

def funcion_limpiar(df):
    # Eliminamos las columnas que no vamos a utilizar
    df = df.drop(columns=["ID", "lat", "lng", "imagen_2", "imagen_3", "imagen_4", "beneficiarios", "compromiso", "ba_elige", "link_interno", "pliego_descarga", "estudio_ambiental_descarga"])

    #ENTORNO
    df['entorno'] = df['entorno'].astype(str)

    #NOMBRE
    df['nombre'] = df['nombre'].astype(str)

    #ETAPA
    df["etapa"] = df["etapa"].str.title()
    df["etapa"] = df["etapa"].str.strip()
    df["etapa"] = df["etapa"].replace(["Finalizado", 'Finalizada/Desestimada', 'Proyecto Finalizado'
        ], "Finalizada")
    df["etapa"] = df["etapa"].replace(['Etapa 3 - Frente 1', 'Iniciada','Piloto 1'], "Proyecto")
    df["etapa"] = df["etapa"].replace(['En Curso', 'En Obra', 'En Proyecto', 'Piloto 2',
        ], "En Ejecución")
    df["etapa"] = df["etapa"].replace(['Desestimada','Neutralizada', 'En Licitación'], "Rescindida")
    df['etapa'] = df['etapa'].astype(str)


    #TIPO
    df["tipo"] = df["tipo"].str.title()
    df["tipo"] = df["tipo"].str.strip()
    df["tipo"] = df["tipo"].fillna("No Especifica")
    df["tipo"] = df["tipo"].replace(['Escuelas', 'Espacio Publico',
        ],"Espacio Público")
    df["tipo"] = df["tipo"].replace('Hidráulica E Infraestructura/ Espacio Público',"Hidráulica E Infraestructura")
    df['tipo'] = df['tipo'].astype(str)


    #AREA RESPONSABLE
    df["area_responsable"] = df["area_responsable"].str.strip()
    df['area_responsable'] = df['area_responsable'].astype(str)


    #DESCRIPCION
    df["tipo"] = df["tipo"].str.strip()
    df["descripcion"] = df["descripcion"].fillna("No especifica")

    #MONTO_CONTRATO

    df["monto_contrato"] = df["monto_contrato"].fillna(0)
    df['monto_contrato'] = df['monto_contrato'].astype(str)
    df["monto_contrato"] = df["monto_contrato"].replace(['- Monto de contrato $ 108.808.255,86\n Adicionales: BED 1-2-3-4 y 5: $ 11.330.095,03'],"120.138.350,89")
    df.iloc[885, df.columns.get_loc("monto_contrato")] = "53160000"
    df.iloc[1146, df.columns.get_loc("monto_contrato")] = "28470000"
    df.iloc[1151, df.columns.get_loc("monto_contrato")] = "31200000"
    df.iloc[1238, df.columns.get_loc("monto_contrato")] = "88626475"
    df.iloc[1381, df.columns.get_loc("monto_contrato")] = "76960855,67"
    df.iloc[1492, df.columns.get_loc("monto_contrato")] = "132600000"
    df['monto_contrato'] = df['monto_contrato'].str.replace(r'[^0-9,]', '', regex=True)
    df['monto_contrato'] = df['monto_contrato'].str.replace(',',".").astype(float)


    #COMUNA
    df["comuna"] = df["comuna"].str.strip()
    df['comuna'] = "Comuna " + df['comuna']
    df["comuna"] = df["comuna"].fillna("No especifica")
    df["comuna"] = df["comuna"].replace(['Comuna 7 y 14','Comuna 7, 15 y 14','Comuna 7 y 9'],"Comuna 7")
    df["comuna"] = df["comuna"].replace('Comuna 1 y 4',"Comuna 1")
    df["comuna"] = df["comuna"].replace(['Comuna 1 a 15'],"Todas")
    df["comuna"] = df["comuna"].replace(['Comuna 14, 2 , 1'],"Comuna 14")
    df["comuna"] = df["comuna"].replace(['Comuna 4 y 1','Comuna 4, 8 y 9'],"Comuna 4")
    df.iloc[1385, df.columns.get_loc("comuna")] = 'Comuna 2'
    df.iloc[1289, df.columns.get_loc("comuna")] = 'Comuna 3'
    df.iloc[[406, 407, 1224], df.columns.get_loc("comuna")] = 'Comuna 4'
    df.iloc[[1019, 1139], df.columns.get_loc("comuna")] = 'Comuna 6'
    df.iloc[[960, 973, 1210], df.columns.get_loc("comuna")] = 'Comuna 8'
    df.iloc[[1110, 1151, 1209, 1474, 1491], df.columns.get_loc("comuna")] = 'Comuna 9'
    df.iloc[1404, df.columns.get_loc("comuna")] = 'Comuna 14'
    df.iloc[939, df.columns.get_loc("comuna")] = 'Comuna 15'
    df['comuna'] = df['comuna'].astype(str)


    #BARRIO
    df["barrio"] = df["barrio"].str.title()
    df["barrio"] = df["barrio"].str.strip()

    # Diccionario de mapeo
    mapeo_barrio = {
        'Agronomí­A': 'Agronomía',
        'Barracas Y Nueva Pompeya': 'Barracas',
        'Boca': 'La Boca',
        'Constitucion': 'Constitución',
        'Cuenca Matanza- Riachuelo':'Villa Riachuelo',
        'Devoto': 'Villa Devoto',
        'Flores, Floresta': 'Flores',
        'La Boca Y San Telmo': 'La Boca',
        'Lugano': 'Villa Lugano',
        'Mataderos, Villa Riachuelo, Barracas, Nueva Pompeya, Villa Lugano Y La Boca': 'Mataderos',
        'Monserrat': 'Montserrat',
        'Nuã±Ez':'Nuñez',
        'P. Chacabuco/Agronomía/ Palermo':'Parque Chacabuco',
        'P. Chacabuco/Palermo':'Parque Chacabuco',
        'Recoleta, Palermo Y Retiro':'Recoleta',
        'San Cristobal':'San Cristóbal',
        'San Nicolas': 'San Nicolás',
        'San Nicolas, Monserrat, San Telmo Y La Boca': 'San Nicolás',
        'Territorio Caba': 'CABA',
        'Villa 6 - Barrio Cildañez': 'Villa Cildañez',
        'Villa Ortúzar': 'Villa Ortuzar',
        'Villa Ortúzar':'Villa Ortuzar',
    }
    df["barrio"] = df["barrio"].replace(mapeo_barrio)
    df['barrio'] = df['barrio'].astype(str)

    #Verificamos valores únicos en BARRIO
    valores_unicos_barrio = df['barrio'].unique()
    valores_unicos_barrio.sort()


    #DIRECCION
    df["direccion"] = df["direccion"].fillna("No especifica")
    df['direccion'] = df['direccion'].astype(str)


    #FECHA_INICIO
    df["fecha_inicio"] = df["fecha_inicio"].fillna("01/01/0001")
    df["fecha_inicio"] = df["fecha_inicio"].replace("A/D", "01/01/0001")
    df['fecha_inicio'] = df['fecha_inicio'].astype(str)

    #FECHA_FIN_INICIAL
    df["fecha_fin_inicial"] = df["fecha_fin_inicial"].fillna("01/01/0001")
    df["fecha_fin_inicial"] = df["fecha_fin_inicial"].replace("A/D", "01/01/0001")
    df['fecha_fin_inicial'] = df['fecha_fin_inicial'].astype(str)

    #PLAZO_MESES

    df["plazo_meses"] = df["plazo_meses"].replace("A/D", 0)
    df["plazo_meses"] = df["plazo_meses"].replace("15 dias", 0.5)
    df.iloc[1125, df.columns.get_loc("plazo_meses")] = 49
    df.iloc[1124, df.columns.get_loc("plazo_meses")] = 24
    df['plazo_meses'] = df['plazo_meses'].str.replace(',', '.').astype(float)
    df["plazo_meses"] = df["plazo_meses"].fillna(0)

    #PORCENTAJE_AVANCE
    
    df["porcentaje_avance"] = df["porcentaje_avance"].str.replace("%","", regex=True)
    df["porcentaje_avance"] = df["porcentaje_avance"].str.replace(",", ".").astype(float)
    df["porcentaje_avance"] = df["porcentaje_avance"].fillna(0)

    #IMAGEN_1

    df["imagen_1"] = df["imagen_1"].fillna("No especifica")
    df['imagen_1'] = df['imagen_1'].str.replace(r'\b-\b', ' ', regex=True)
    df.iloc[1492, df.columns.get_loc("imagen_1")] = "No especifica"
    df['imagen_1'] = df['imagen_1'].astype(str)

    #LICITACION_OFERTA_EMPRESA

    df["licitacion_oferta_empresa"] = df["licitacion_oferta_empresa"].fillna("No especifica")
    df.iloc[1283, df.columns.get_loc("licitacion_oferta_empresa")] = "No especifica"
    df['licitacion_oferta_empresa'] = df['licitacion_oferta_empresa'].astype(str)

    #LICITACION_ANIO

    df["licitacion_anio"] = df["licitacion_anio"].fillna("0")
    df["licitacion_anio"] = df["licitacion_anio"].str.replace("512-0730-OC17","0")
    df["licitacion_anio"] = df["licitacion_anio"].str.replace("-","0")
    df['licitacion_anio'] = df['licitacion_anio'].astype(int)

    #CONTRATACION_TIPO

    df["contratacion_tipo"] = df["contratacion_tipo"].str.title()
    df["contratacion_tipo"] = df["contratacion_tipo"].str.strip()
    df["contratacion_tipo"] = df["contratacion_tipo"].fillna("No especifica")
    df["contratacion_tipo"] = df["contratacion_tipo"].replace(['-', 'Compulsa Privada De Precios', 'Donacion', 'Licitación'
        ], 'No especifica')
    df["contratacion_tipo"] = df["contratacion_tipo"].replace([
        '2095', '433', '433/16 (Decr Necesidad Y Urgencia)', '556/10 Y 433/16', 
        '556/2010', 'Decreto 433', 'Decreto 433/16', 'Decreto 433/2016', 'Decreto N° 433/16'
        ], "Decreto")
    df["contratacion_tipo"] = df["contratacion_tipo"].replace(['Ad Mantenimiento', 'Ad. Mantenimiento'
        ], 'Adicional De Mantenimiento')
    df["contratacion_tipo"] = df["contratacion_tipo"].replace('Contratacion', 'Contratación')
    df["contratacion_tipo"] = df["contratacion_tipo"].replace(['Bac', 'Contratacií“N Directa', 'Contratacion De Varias Empresas',
        'Contratación De Varias Empresas', 'Contratacion Directa', 'Contratación Directa', 'Contratación Directa - Contratación Menor',
        'Contratacion Menor', 'Contratación Menor'
        ], 'Contratación')
    df["contratacion_tipo"] = df["contratacion_tipo"].replace(['Licitacion', 'Publica'], ['Licitación', 'Pública'])
    df["contratacion_tipo"] = df["contratacion_tipo"].replace(['Licicitación Pública', 'Licitaciã³N Pãºblica', 
        'Licitacion Pí¹Blica', 'Licitacion Publica', 'Licitación Publica', 'Licitacíón Pública', 'Licitacion Pública',
        'Licitación Pública Abreviada.', 'Licitación Pública De Obra Mayor Nâ° 682/Sigaf/2020,', 'Licitación Pública Internacional',
        'Licitación Pública Nacional', 'Lpu', 'Obra Publica'
        ], 'Licitación Pública')
    df["contratacion_tipo"] = df["contratacion_tipo"].replace(['Licitacion Privada', 'Licitación Privada De Obra Menor', 'Licitación Privada Obra Menor'
        ], 'Licitación Privada')
    df["contratacion_tipo"] = df["contratacion_tipo"].replace("Desestimada", 'Sin Efecto')
    df.iloc[1488, df.columns.get_loc("contratacion_tipo")] = 'Licitación Pública'
    df['contratacion_tipo'] = df['contratacion_tipo'].astype(str)

    #Verificamos valores únicos en CONTRATACION_TIPO
    valores_unicos_contratacion_tipo = df['contratacion_tipo'].unique()

    #NRO_CONTRATACION

    df["nro_contratacion"] = df["nro_contratacion"].fillna("No especifica")
    df.iloc[[1283,145,209], df.columns.get_loc("nro_contratacion")] = "No especifica"
    df['nro_contratacion'] = df['nro_contratacion'].astype(str)

    #CUIT_CONTRATISTA

    df["cuit_contratista"] = df["cuit_contratista"].str.replace("-", "")
    df["cuit_contratista"] = df["cuit_contratista"].str[:11]
    df["cuit_contratista"] = df["cuit_contratista"].fillna(0)
    df.iloc[1283, df.columns.get_loc("cuit_contratista")] = 0
    df['cuit_contratista'] = df['cuit_contratista'].astype('int64')

    #MANO_OBRA

    df["mano_obra"] = pd.to_numeric(df["mano_obra"], errors="coerce")
    df["mano_obra"] = df["mano_obra"].fillna(0)
    df['mano_obra'] = df['mano_obra'].astype(int)

    #DESTACADA

    df["destacada"] = df["destacada"].replace("SI",1)
    df["destacada"] = df["destacada"].fillna(0)
    df["destacada"] = df["destacada"].astype(bool)

    #EXPEDIENTE_NUMERO

    df["expediente-numero"] = df["expediente-numero"].fillna("No especifica")
    df['expediente-numero'] = df['expediente-numero'].astype(str)

    #FINANCIAMIENTO

    df["financiamiento"] = df["financiamiento"].fillna("No especifica")
    df['financiamiento'] = df['financiamiento'].astype(str)

    return df
