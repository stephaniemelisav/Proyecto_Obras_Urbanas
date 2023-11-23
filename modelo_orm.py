from peewee import *


# función que conecta y retorna base de datos.
def funcion_conectar_db():
  sqlite_db = SqliteDatabase('obras_urbanas.db', pragmas={'journal_mode': 'wal'})
  try:
    sqlite_db.connect()
    print("Base de datos conectada.")
  except OperationalError as e:
    print("Error al conectar con la BD.", e)
    exit()
  return sqlite_db

  

# función que mapea y crea las tablas de la base de datos en donde se cargará el dataset limpio.
def funcion_mapear_orm(db):
  class BaseModel(Model):
    class Meta:
        database = db

    # -----------------------------Tablas de consulta (lookups) -------------------------
  class Etapa(BaseModel):
    ID_ETAPA = AutoField()
    nombre_etapa = CharField(unique=True)
    def __str__(self):
      return self.nombre_etapa
    class Meta:
      db_table = 'Etapa'
      
  class TipoObra(BaseModel):
    ID_TIPO_OBRA = AutoField()
    tipo_obra = CharField(unique=True)
    def __str__(self):
      return self.tipo_obra
    class Meta:
      db_table = 'TipoObra'
      
  class AreaResponsable(BaseModel):
    ID_AREA_RESPONSABLE = AutoField()
    nombre_area = CharField(unique=True)
    def __str__(self):
      return self.nombre_area
    class Meta:
      db_table = 'AreaResponsable'

  class Comuna(BaseModel):
    ID_COMUNA = AutoField()
    nombre_comuna = CharField(unique=True)
    def __str__(self):
      return self.nombre_comuna
    class Meta:
      db_table = 'Comuna'

  class Barrio(BaseModel):
    ID_BARRIO = AutoField()
    nombre_barrio = CharField(unique=True)
    #comuna = ForeignKeyField(Comuna, backref='barrio') # Muchos barrios pueden estar en una comuna
    def __str__(self):
      return self.nombre_barrio
    class Meta:
      db_table = 'Barrio'

  class ContratacionTipo(BaseModel):
    ID_TIPO_CONTRATACION = AutoField()
    contratacion = CharField(unique=True)
    def __str__(self):
      return self.contratacion
    class Meta:
      db_table = 'TipoContratacion'

  class Financiamiento(BaseModel):
    ID_FINANCIAMIENTO = AutoField()
    financiamiento = CharField(unique=True)
    def __str__(self):
      return self.financiamiento
    class Meta:
      db_table = 'Financiamiento'

  # -------------------------------Tabla principal--------------------------
  class ObraUrbana(BaseModel):
    ID_OBRA_URBANA = AutoField() # por forma N1 se agrega campo ID, a definir
    entorno = CharField(100) # Se limita a 100 carácteres.
    nombre = CharField(100)
    etapa = ForeignKeyField(Etapa, backref='obra_urbana')
    tipo_obra = ForeignKeyField(TipoObra, backref='obra_urbana')
    area_responsable = ForeignKeyField(AreaResponsable, backref = 'obra_urbana')
    descripcion = CharField(500)
    monto_contrato = IntegerField(20)
    comuna = ForeignKeyField(Comuna, backref = 'obra_urbana')
    barrio = ForeignKeyField(Barrio, backref='obra_urbana') # Analizar mejor : deberíamos poder responder ¿cuántos barrios por comuna?
    direccion = CharField(200)
    fecha_inicio = DateField()
    fecha_fin_inicial = DateField()
    plazo_meses = FloatField()
    porcentaje_avance = IntegerField()
    imagen = TextField()
    licitacion_oferta_empresa = TextField()
    licitacion_anio = IntegerField()
    contratacion_tipo = ForeignKeyField(ContratacionTipo, backref = 'obra_urbana')
    nro_contratacion = CharField(50)
    cuit_contratista = IntegerField()
    mano_obra = IntegerField()
    destacada = BooleanField()
    expediente_numero = CharField(100)
    financiamiento = ForeignKeyField(Financiamiento, backref = 'obra_urbana')
  
    def __str__(self):
        pass
    class Meta:
        database = funcion_conectar_db()  # Asegúrate de que la base de datos esté conectada
        db_table = 'ObraUrbana'
  
  # Creamos todas las tablas
  db.create_tables([Etapa, TipoObra, AreaResponsable, Comuna, Barrio, ContratacionTipo, Financiamiento, ObraUrbana])
  print("ORM mapeado.")
  # Retornamos las clases por estar dentro de una función.
  return Etapa, TipoObra, AreaResponsable, Comuna, Barrio, ContratacionTipo, Financiamiento, ObraUrbana

