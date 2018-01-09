import json
from rest_framework import status
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from capas.models import TipologiaConstructiva
from capas.serializadores.tipologia import TipologiaListSerializador, TipologiaSerializador


class GETSingleTipologiaTest(APITestCase):
    
    """ Test module for GET single Tipologia API """
    
    def setUp(self):
        TipologiaConstructiva.objects.create(id=1, descripcion='tipo 1', nombre_centro='principal', estandar='1.0', anyo='2000')
        TipologiaConstructiva.objects.create(id=2, descripcion='tipo 2', nombre_centro='secundario', estandar='2.0', anyo='2010')
        TipologiaConstructiva.objects.create(id=3, descripcion='tipo 3', nombre_centro='terciario', estandar='3.0', anyo='2015')
        
    
    def test_get_valid_single_Tipologia(self):
        response = self.client.get('/tipologias/1')
        objeto = TipologiaConstructiva.objects.get(pk=1)
        serializer = TipologiaListSerializador(objeto)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    
    

class CreateNewTipologiaTest(APITestCase):
    
    """ Test module for create new Tipologia """
    
    def setUp(self):
        self.valid_payload = {'descripcion':'tipo 3', 'nombre_centro':'terciario', 'estandar':'3.0', 'anyo':'2015'}
        self.invalid_payload ={'descripcion':'', 'nombre_centro': '', 'estandar':'', 'anyo':''}
            

    def test_create_valid_tipologia(self):
        response = self.client.post("/tipologias", self.valid_payload, format='json')
        objeto = TipologiaConstructiva.objects.get(pk=1)
        serializer = TipologiaSerializador(objeto)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  
        self.assertEqual(response.data, serializer.data)                    

    def test_create_invalid__tipologia(self):
        response = self.client.post("/tipologias", self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    
class UpdateSingleTipologiaTest(APITestCase):
    
    """ Test module for updating an existing  Tipologia record """
    
    
    def setUp(self):
        TipologiaConstructiva.objects.create(id=1, descripcion='tipo 1', nombre_centro='principal', estandar='1.0', anyo='2000')
        TipologiaConstructiva.objects.create(id=2, descripcion='tipo 2', nombre_centro='secundario', estandar='2.0', anyo='2010')
        TipologiaConstructiva.objects.create(id=3, descripcion='tipo 3', nombre_centro='terciario', estandar='3.0', anyo='2015')
        
        self.valid_payload = {'descripcion':'tipo 1.1', 'nombre_centro':'principal', 'estandar':'3.0', 'anyo':'2015'}
        self.invalid_payload ={'descripcion':'', 'nombre_centro': '', 'estandar':'', 'anyo':''}
    
    
    def test_valid_update_tipologia(self):
        response = self.client.put('/tipologias/1', self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)           
        
    def test_invalid_update_tipologia(self):
        response = self.client.put('/tipologias/3', self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
class DeleteSingleTipologiaTest(APITestCase):
    
    """ Test module for deleting an existing  Tipologia record """
    
    def setUp(self):
        TipologiaConstructiva.objects.create(id=1, descripcion='tipo 1', nombre_centro='principal', estandar='1.0', anyo='2000')
        TipologiaConstructiva.objects.create(id=2, descripcion='tipo 2', nombre_centro='secundario', estandar='2.0', anyo='2010')
        
    def test_valid_delete_tipologia(self):
        response = self.client.delete('/tipologias/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)           

    
    def test_invalid_delete_tipologia(self):
        response = self.client.delete('/tipologias/7')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)