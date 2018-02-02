from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, Polygon
from django.contrib.gis.geos.collections import MultiPolygon, MultiLineString
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre =  models.CharField(max_length=30, unique=True)
    descripcion =  models.CharField(max_length=80, null=True)

    @property
    def eliminable(self):
        return not self.capas.all().exists()

    def __str__(self):
        return self.nombre

class Capas(models.Model):
    PUNTO = 'Point'
    POLIGONO = 'Polygon'
    POLIGONO_MULTIPLE = 'MultiPolygon'
    PUNTO_MULTIPLE = 'MultiPoint'
    LINEA = 'LineString'
    LINEA_MULTIPLE = 'MultiLineString'
    GEOMETRICOS_CHOICES = (
        (PUNTO, PUNTO),
        (POLIGONO, POLIGONO),
        (LINEA, LINEA),
        (POLIGONO_MULTIPLE, POLIGONO_MULTIPLE),
        (LINEA_MULTIPLE, LINEA_MULTIPLE)
        )

    nombre = models.CharField(max_length=30)
    categoria = models.ForeignKey(Categoria, related_name="capas",
                                  on_delete=models.CASCADE)
    tipo = models.CharField(max_length=30, choices=GEOMETRICOS_CHOICES)

    def __str__(self):
        return self.nombre

class Atributos(models.Model):
    PUNTO = 'Point'
    POLIGONO = 'Polygon'
    POLIGONO_MULTIPLE = 'MultiPolygon'
    PUNTO_MULTIPLE = 'MultiPoint'
    LINEA = 'LineString'
    TEXTO = 'Text'
    ENTERO = 'Int'
    FLOTANTE = 'Float'
    LINEA_MULTIPLE = 'MultiLineString'
    IMAGEN = 'Image'
    EMAIL = 'Email'
    DATE = 'Date'
    DATETIME = 'DateTime'

    GEOMETRICOS = (PUNTO, POLIGONO, LINEA, POLIGONO_MULTIPLE, LINEA_MULTIPLE, LINEA_MULTIPLE,)

    TIPO_CHOICES = (
        (PUNTO, PUNTO),
        (POLIGONO, POLIGONO),
        (LINEA, LINEA),
        (TEXTO, TEXTO),
        (ENTERO, ENTERO),
        (FLOTANTE, FLOTANTE),
        (POLIGONO_MULTIPLE, POLIGONO_MULTIPLE),
        (LINEA_MULTIPLE, LINEA_MULTIPLE),
        (IMAGEN, IMAGEN),
        (EMAIL, EMAIL),
        (DATE, DATE),
        (DATETIME, DATETIME),
    )

    capa = models.ForeignKey(Capas, on_delete=models.CASCADE,
                             related_name='atributos')
    nombre = models.CharField(max_length=30)
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    descripcion = models.CharField(max_length=80, null=True)

    @property
    def eliminable(self):
        if self.nombre != "geom":
            return not self.capa.categoria.parametros.filter(nombre=self.nombre).exists()
        return False


    @property
    def modificable(self):
        if self.nombre != "geom":
            return not self.capa.categoria.parametros.filter(nombre=self.nombre).exists()
        return False

def crear_modelo(nombre):
    opciones = {
        "__module__": "capas"
    }
    campos = buscar_capa_y_atributos(nombre)
    opciones.update(campos)
    modelo = type(nombre, (models.Model,), opciones)
    return modelo

def buscar_capa_y_atributos(nombre):
    try:
        capa = Capas.objects.filter(nombre=nombre).first()
        campos = {}
        for attr in capa.atributos.all():
            if attr.tipo == Atributos.TEXTO:
                attr.tipo = models.CharField(max_length=255)
            elif attr.tipo == Atributos.ENTERO:
                attr.tipo = models.IntegerField()
            elif attr.tipo == Atributos.FLOTANTE:
                attr.tipo = models.FloatField()
            campo = {
                attr.nombre: attr.tipo,
            }
            campos.update(campo)
        campos.update({"geom": models.GeometryField()})
        return campos
    except Exception as e:
        print(e)
        error = {
            "capa": "no existe"
        }
        raise ValidationError(error)

class Parametro(models.Model):
    TEXTO = 'Text'
    ENTERO = 'Int'
    FLOTANTE = 'Float'
    IMAGEN = 'Image'
    EMAIL = 'Email'
    DATE = 'Date'
    DATETIME = 'DateTime'

    TIPO_CHOICES = (
        (TEXTO, TEXTO),
        (ENTERO, ENTERO),
        (FLOTANTE, FLOTANTE),
        (IMAGEN, IMAGEN),
        (EMAIL, EMAIL),
        (DATE, DATE),
        (DATETIME, DATETIME)
    )

    nombre = models.CharField(max_length=30, unique=True)
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE,
                             related_name='parametros')
    @property
    def eliminable(self):
        return not self.categoria.capas.all().exists()
    
    
    def __str__(self):
        return self.nombre


class Casos(models.Model):
   
    descripcion = models.CharField(max_length=255)    
    fecha = models.DateField(blank=True)
    hora = models.TimeField(blank=True)
    fecha_creado = models.DateField(blank=True)
    hora_creado =  models.TimeField(blank=True)
    visible = models.BooleanField(default=False)
    geom = models.PointField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Casos')
    capa = models.ForeignKey(Capas, null=True, on_delete=models.CASCADE, related_name='Casos')
    registro = models.IntegerField(null=True)

class Imagen(models.Model):
    caso = models.ForeignKey(Casos, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='fotos')

class TipologiaConstructiva(models.Model):
   
    descripcion = models.CharField(max_length=255)    
    nombre = models.CharField(max_length=255, unique=True)
    estandar = models.CharField(max_length=255)    
    anyo = models.IntegerField()

    def __str__(self):
        return self.nombre



""" Probablemente sea eliminada aunque es lo correcto para gis """
class Territorio(models.Model):
    geom = models.PolygonField(null=True, blank=True)          
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=60)
    poblacionCenso = models.IntegerField(default=0)
    poblacionDeterminada = models.IntegerField(default=0)
    estado =models.CharField(max_length=255, blank=True)
    municipio =models.CharField(max_length=255, blank=True)
    parroquia =models.CharField(max_length=255, blank=True)
    parentid = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='dependencias',)    
    
class GeoUnidad(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    area = models.FloatField(default=0)
    indiceAmenaza = models.FloatField(default=0)
    indiceVulnerabilidad = models.FloatField(default=0)
    indiceRiesgo = models.FloatField(default=0)
    fuente = models.CharField(max_length=255, null=True)
    anyo = models.IntegerField(default=1900)
    geom = models.PolygonField()          
    status = models.CharField(max_length=20, null=True, blank=True)
    territorio = models.ForeignKey(Territorio, on_delete=models.CASCADE, related_name='geounidades')    

    @property
    def eliminable(self):
        return not (self.comunidades.all().exists() or self.riesgos.all().exists())



class Riesgos(models.Model):
    indiceVulnerabilidad = models.FloatField(default=0)
    indiceAmenaza = models.FloatField(default=0)
    indiceRiesgo = models.FloatField(default=0)
    anyo = models.IntegerField(default=1900)
    fuente = models.CharField(null=True, blank=True, max_length=255)
    indiceModificado =  models.CharField(null=True, blank=True, max_length=255)
    activo = models.BooleanField(default=False)
    geounidad = models.ForeignKey(GeoUnidad, on_delete=models.CASCADE, related_name='riesgos')


class Comunidad(models.Model):
    
    geom = models.PolygonField()
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255, null=True,blank=True)
    poblacion = models.IntegerField(default=0)
    area = models.FloatField(default=0)
    indiceVulnerabilidad = models.FloatField(default=0)
    indiceAmenaza = models.FloatField(default=0)
    indiceRiesgo = models.FloatField(default=0)
    statusSocial = models.CharField(max_length=255, null=True,blank=True)
    geounidad = models.ForeignKey(GeoUnidad, on_delete=models.CASCADE, related_name='comunidades', null=True)
    tipologiaConstructiva = models.ForeignKey(TipologiaConstructiva, on_delete=models.CASCADE, related_name='comunidades', null=True)
    territorio = models.ForeignKey(Territorio, on_delete=models.CASCADE, related_name='comunidades', null=True)

    @property
    def eliminable(self):
        return not self.viviendas.all().exists()

class ConsejoComunal(models.Model):
    geom = models.PolygonField()
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255,null=True,blank=True)
    poblacionDeterminada = models.IntegerField(default=0)
    poblacionCenso = models.IntegerField(default=0)
    area = models.FloatField(default=0)
    servicios = models.CharField(max_length=255, null=True,blank=True)
    representante = models.CharField(max_length=255, null=True,blank=True)
    telefono = models.CharField(max_length=255, null=True,blank=True)
    indiceVulnerabilidad = models.IntegerField(default=0)
    indiceAmenaza = models.IntegerField(default=0)
    indiceRiesgo = models.IntegerField(default=0)
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE, related_name='consejoscomunales', null=True)

class Vivienda(models.Model):
    geom = models.PointField()
    numero = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    anyo_construccion = models.IntegerField(default=1900)
    numpisos = models.IntegerField(default=1)
    tipoEstructura = models.CharField(max_length=255, null=True, blank=True)
    uso = models.CharField(max_length=255, null=True, blank=True)
    area = models.FloatField(default=0)
    indiceOcupacional = models.FloatField(default=0)
    numHabitacion = models.IntegerField(default=0)
    numAmbientes = models.IntegerField(default=1)
    tipo = models.CharField(max_length=255,null=True,blank=True)
    tipoParedes = models.CharField(max_length=255,null=True,blank=True)
    tipoPiso = models.CharField(max_length=255,null=True,blank=True)
    tipoTecho = models.CharField(max_length=255,null=True,blank=True)
    numBanos = models.IntegerField(default=0)
    aguasBlancas = models.CharField(max_length=2, null=True,blank=True)
    aguasServidas  = models.CharField(max_length=2, null=True,blank=True)
    gas = models.CharField(max_length=255, null=True,blank=True)
    sistemaElectrico = models.CharField(max_length=255, null=True,blank=True)
    aseo = models.CharField(max_length=255, null=True,blank=True)
    telefonia = models.CharField(max_length=255, null=True,blank=True)
    transporte = models.CharField(max_length=255, null=True,blank=True)
    numFamilias = models.IntegerField(default=0)
    numHabitantes = models.IntegerField(default=0)
    numNinos = models.IntegerField(default=0)
    numAdultos = models.IntegerField(default=0)
    numTercera = models.IntegerField(default=0)
    numMasculino = models.IntegerField(default=0)
    numFemenino = models.IntegerField(default=0)
    nacionalidad = models.CharField(max_length=255, null=True,blank=True)
    indiceVulnerabilidad = models.FloatField(default=0)
    indiceAmenaza = models.FloatField(default=0)
    indiceRiesgo = models.FloatField(default=0)
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE, related_name='viviendas', null=True)
    consejoComunal = models.ForeignKey(ConsejoComunal, on_delete=models.CASCADE, related_name='viviendas', null=True)
    tipologiaConstructiva = models.ForeignKey(TipologiaConstructiva, on_delete=models.CASCADE, related_name='viviendas', null=True)

class CentroSaludEmergencia(models.Model):
    geom = models.PointField()
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255,null=True,blank=True)
    anyo_construccion = models.IntegerField(default=1900)
    poblacionDiaria = models.IntegerField(default=0)
    numCamas = models.IntegerField(default=0)
    capacidad = models.IntegerField(default=0)
    horarioAtencion = models.CharField(max_length=255, null=True, blank=True)
    serviciosMedicos = models.CharField(max_length=255, null=True, blank=True)
    numpisos = models.IntegerField(default=1)
    numedificios = models.IntegerField(default=1)
    area = models.FloatField(default=0)
    indiceVulnerabilidad = models.FloatField(default=0)
    indiceAmenaza = models.FloatField(default=0)
    indiceRiesgo = models.FloatField(default=0)
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE, related_name='centrosaludemergencia')
    tipologiaConstructiva = models.ForeignKey(TipologiaConstructiva, on_delete=models.CASCADE, related_name='centrosaludemergencia', null=True)

class CentroEducativo(models.Model):
    geom = models.PointField()
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255,null=True,blank=True)
    anyo_construccion = models.IntegerField(default=1900)
    area = models.FloatField(default=0)
    uso = models.CharField(max_length=255,null=True,blank=True)
    tipoPisos = models.CharField(max_length=255,null=True,blank=True)
    indiceOcupacional = models.FloatField(default=0)
    codigoDEA = models.CharField(max_length=255,null=True,blank=True)
    matricula = models.IntegerField(default=1)
    tipoEscuela = models.CharField(max_length=255,null=True,blank=True)
    turno = models.CharField(max_length=255,null=True,blank=True)
    numedificios = models.IntegerField(default=1)
    numpisos = models.IntegerField(default=1)
    tipoEdificacion = models.CharField(max_length=255,null=True,blank=True)
    tipoDependencia = models.CharField(max_length=255,null=True,blank=True)
    danyo = models.CharField(max_length=255,null=True,blank=True)
    indiceVulnerabilidad = models.FloatField(default=0)
    indiceAmenaza = models.FloatField(default=0)
    indiceRiesgo = models.FloatField(default=0)
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE, related_name='centroseducativos')
    tipologiaConstructiva = models.ForeignKey(TipologiaConstructiva, on_delete=models.CASCADE, related_name='centroseducativos', null=True)    

class Censo(models.Model):
    fecha = models.DateField()
    descripcion = models.CharField(max_length=255)
    totalFamilias = models.IntegerField(default=0)
    totalHabitantes = models.IntegerField(default=0)
    totalViviendas = models.IntegerField(default=0)
    consejocomunal = models.ForeignKey(ConsejoComunal, on_delete=models.CASCADE, related_name='censo') 

class Role(models.Model):
    nombre = models.CharField(max_length=50,unique=True)
    descripcion =   models.CharField(max_length=50,unique=True)    

class Usuario(models.Model):
    institucion =  models.CharField(max_length=255,blank=True,null=True)
    user = models.OneToOneField(User)  