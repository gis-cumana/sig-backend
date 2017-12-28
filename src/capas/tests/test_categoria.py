import json
from rest_framework import status
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from capas.models import Categoria
from capas.serializadores.categorias import CategoriaListSerializador, CategoriaSerializador


class GETAllCategoriasTest(APITestCase):
    """ Test module for GET all Categorias API """
    def setUp(self):
        self.territorios = Categoria.objects.create(nombre='territorios', descripcion='comprende sectores, parroquias')
        self.eventos = Categoria.objects.create(nombre='eventos', descripcion='comprende eventos sismos,licuaciones')
        self.edificacion = Categoria.objects.create(nombre='edificiacion', descripcion='comprende escuelas, universidades')

    def test_list_categorias(self):
        response = self.client.get("/categorias")
        categoria = Categoria.objects.all()
        serializer = CategoriaSerializador(categoria, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)   
       
class GETSingleCategoriasTest(APITestCase):
    """ Test module for GET single Categorias API """

    def setUp(self):
        self.territorios = Categoria.objects.create(id=1, nombre='territorios', descripcion='comprende sectores, parroquias')
        self.eventos = Categoria.objects.create(id=2, nombre='eventos', descripcion='comprende eventos sismos,licuaciones')
        self.edificacion = Categoria.objects.create(id=3, nombre='edificiacion', descripcion='comprende escuelas, universidades')
        
    
    def test_get_valid_single_categorias(self):
        response = self.client.get('/categorias/1')
        categoria = Categoria.objects.get(pk=1)
        serializer = CategoriaListSerializador(categoria)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_get_invalid_single_categorias(self):
        response = self.client.get('/categorias/4')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)


class CreateNewCategoriasTest(APITestCase):
    """ Test module for create new Categorias """

    def setUp(self):
        self.valid_payload ={
            'nombre' : 'territorios',
            'descripcion' : 'todos los terrenos'
        }        

        self.invalid_payload = {
            'nombre' : '',
            'descripcion' : 'todas las edificaciones'
        }

    def test_create_valid_categoria(self):
        response = self.client.post("/categorias", self.valid_payload, format='json')
        categoria = Categoria.objects.get(pk=1)
        serializer = CategoriaSerializador(categoria)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  
        self.assertEqual(response.data, serializer.data)                    

    def test_create_invalid_categoria(self):
        response = self.client.post("/categorias", self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleCategoriasTest(APITestCase):
    """ Test module for updating an existing  Categorias record """
    def setUp(self):
        self.territorios = Categoria.objects.create(id=1, nombre='territorios', descripcion='comprende sectores, parroquias')
        self.eventos = Categoria.objects.create(id=2, nombre='eventos', descripcion='comprende eventos sismos,licuaciones')
        self.edificacion = Categoria.objects.create(id=3, nombre='edificiacion', descripcion='comprende escuelas, universidades')
        
        self.valid_payload ={'id':2, 'nombre' : 'eventos','descripcion' : 'todos los eventos'}        
        self.invalid_payload = {'nombre' : '', 'descripcion' : 'todas las edificaciones'}
    
    def test_valid_update_categoria(self):
        response = self.client.put('/categorias/2', self.valid_payload, format='json')
        self.assertEqual(response.status_code, 200)           
        
    def test_invalid_update_categoria(self):
        response = self.client.put('/categorias/2', self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleCategoriasTest(APITestCase):
    """ Test module for deleting an existing  Categorias record """
    def setUp(self):
        self.territorios = Categoria.objects.create(id=1, nombre='territorios', descripcion='comprende sectores, parroquias')
        self.eventos = Categoria.objects.create(id=2, nombre='eventos', descripcion='comprende eventos sismos,licuaciones')
        self.edificacion = Categoria.objects.create(id=3, nombre='edificiacion', descripcion='comprende escuelas, universidades')
        
    def test_valid_delete_categoria(self):
        response = self.client.delete('/categorias/2')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)           
    
    def test_invalid_delete_categoria(self):
        response = self.client.delete('/categorias/4')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)