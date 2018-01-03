from django.contrib.gis.db import models
from django.contrib.gis.geos.point import Point
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

    GEOMETRICOS = (PUNTO, POLIGONO, LINEA, POLIGONO_MULTIPLE, LINEA_MULTIPLE, LINEA_MULTIPLE,)

    TIPO_CHOICES = (
        (PUNTO, PUNTO),
        (POLIGONO, POLIGONO),
        (LINEA, LINEA),
        (TEXTO, TEXTO),
        (ENTERO, ENTERO),
        (FLOTANTE, FLOTANTE),
        (POLIGONO_MULTIPLE, POLIGONO_MULTIPLE),
        (LINEA_MULTIPLE, LINEA_MULTIPLE)
    )

    capa = models.ForeignKey(Capas, on_delete=models.CASCADE,
                             related_name='atributos')
    nombre = models.CharField(max_length=30)
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    descripcion = models.CharField(max_length=80, null=True)

    @property
    def eliminable(self):
        return self.nombre != "geom"

    @property
    def modificable(self):
        return self.nombre != "geom"

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
    visible = models.BooleanField()
    geom = models.PointField(null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Casos')
    capa = models.ForeignKey(Capas, null=True, on_delete=models.CASCADE, related_name='Casos')
    registro = models.IntegerField(null=True)

class TipologiaConstructiva(models.Model):
   
    descripcion = models.CharField(max_length=255)    
    nombre_centro = models.CharField(max_length=255, unique=True)
    estandar = models.CharField(max_length=255)    
    anyo = models.CharField(max_length=4)

    def __str__(self):
        return self.nombre