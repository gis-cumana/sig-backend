import json
from rest_framework import status
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from capas.models import Categoria, Parametro
from capas.serializadores.categorias import CategoriaListSerializador, CategoriaSerializador
from capas.serializadores.parametros import ParametroListSerializador, ParametroSerializador


class GETAllParametrosTest(APITestCase):
    """ Test module for GET all Parametros API """
    def setUp(self):
        self.objcat = Categoria.objects.create(nombre='edificacion', descripcion='comprende escuelas')
        Parametro.objects.create(nombre='matricula', tipo='Int', categoria=self.objcat)
        Parametro.objects.create(nombre='extension', tipo='Float', categoria=self.objcat)
        Parametro.objects.create(nombre='rigesgo', tipo='Text', categoria=self.objcat)
        

    def test_list_parametros(self):
        response = self.client.get("/parametros")
        parametro = Parametro.objects.all()
        serializer = ParametroSerializador(parametro, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)   
       
class GETSingleParametrosTest(APITestCase):
    
    """ Test module for GET single Parametros API """
    
    def setUp(self):
        self.objcat = Categoria.objects.create(nombre='edificacion', descripcion='comprende escuelas')
        Parametro.objects.create(id=1, nombre='matricula', tipo='Int', categoria=self.objcat)
        Parametro.objects.create(id=2, nombre='extension', tipo='Float', categoria=self.objcat)
        Parametro.objects.create(id=3, nombre='rigesgo', tipo='Text', categoria=self.objcat)
        
    
    def test_get_valid_single_parametros(self):
        response = self.client.get('/parametros/1')
        parametro = Parametro.objects.get(pk=1)
        serializer = ParametroListSerializador(parametro)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_get_invalid_single_parametros(self):
        response = self.client.get('/parametros/4')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
    

class CreateNewParametrosTest(APITestCase):
    
    """ Test module for create new Parametros """
    
    def setUp(self):
        self.categoria = Categoria.objects.create(id=1, nombre='edificacion', descripcion='comprende escuelas')
        self.valid_payload ={'nombre': 'matricula', 'tipo':'Int', 'categoria': 1}
        self.invalid_payload ={'nombre': '', 'tipo':'Float', 'categoria': 1}
            

    def test_create_valid_parametro(self):
        response = self.client.post("/parametros", self.valid_payload, format='json')
        parametro = Parametro.objects.get(pk=1)
        serializer = ParametroSerializador(parametro)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  
        self.assertEqual(response.data, serializer.data)                    

    def test_create_invalid_parametro(self):
        response = self.client.post("/parametros", self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    

class UpdateSingleParametrosTest(APITestCase):
    
    """ Test module for updating an existing  Parametros record """
    
    def setUp(self):
        self.categoria = Categoria.objects.create(id=1, nombre='edificacion', descripcion='comprende escuelas')
        Parametro.objects.create(id=1, nombre='matriz', tipo='Int', categoria=self.categoria)
        Parametro.objects.create(id=2, nombre='extension', tipo='Float', categoria=self.categoria)
        Parametro.objects.create(id=3, nombre='rigesgo', tipo='Text', categoria=self.categoria)
        
        self.valid_payload ={'id':1, 'nombre':'matricula','tipo': 'Int', 'categoria': 1}        
        self.invalid_payload = {'nombre' : '','tipo': 'Int', 'categoria': 1}
    
    def test_valid_update_parametro(self):
        response = self.client.put('/parametros/1', self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)           
        
    def test_invalid_update_parametro(self):
        response = self.client.put('/parametros/3', self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
class DeleteSingleParametrosTest(APITestCase):
    
    """ Test module for deleting an existing  Parametros record """
       
    def setUp(self):
        self.categoria = Categoria.objects.create(id=1, nombre='edificacion', descripcion='comprende escuelas')
        self.matricula = Parametro.objects.create(id=1, nombre='matricula', tipo='Int', categoria=self.categoria)
        self.matricula = Parametro.objects.create(id=2, nombre='extension', tipo='Float', categoria=self.categoria)        
        
    def test_valid_delete_parametro(self):
        response = self.client.delete('/parametros/2')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)           
    
    def test_invalid_delete_parametro(self):
        response = self.client.delete('/parametros/4')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    