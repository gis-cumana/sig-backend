from django.contrib.gis.geos import Point, MultiPoint, Polygon, MultiPolygon, \
                                    LineString

class Punto(Point):
    def get(value):
        return Point(value)

class MultiPunto(MultiPoint):
    def get(value):
        return MultiPoint(value)

class Linea(MultiPoint):
    def get(value):
        return LineString(value)

class MultiLinea(MultiPoint):
    def get(value):
        return LineString(value)

class Raster(MultiPoint):
    def get(value):
        return LineString(value)

class Poligono(Polygon):
    def get(value):
        return Polygon(value[0])

class MultiPoligono(Polygon):
    def get(value):
        lista = []
        if len(value[0]) == 1:
            lista.append(Polygon(value[0][0]))
        else:
            for i in range(len(value[0])):
                lista.append(Polygon(value[0][i][0]))
        return MultiPolygon(lista)