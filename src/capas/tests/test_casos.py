import json
from rest_framework import status
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from capas.models import Casos
from django.contrib.gis.geos.point import Point
from django.contrib.auth.models import User
from capas.serializadores.casos import CasosListSerializador, CasosSerializador
from capas.serializadores.usuarios import UsuarioListSerializador, UsuarioSerializador
from datetime import datetime, date, time

       
class GETSingleCasosTest(APITestCase):
    
    """ Test module for GET single Casos API """
    
    def setUp(self):
        self.usuario = User.objects.create(username='usuariomaster', first_name='Usuario', last_name='Master')
        self.usuario.set_password('mastermaster')
        self.usuario.save()
        Casos.objects.create(id=1, descripcion='derrumbre', fecha='2017-10-17', hora='00:00:00', fecha_creado='2017-12-28',hora_creado='00:00:00', visible=False, geom = Point(-0.1,-0.6) ,usuario=self.usuario)
        Casos.objects.create(id=2, descripcion='deslave', fecha='2017-10-17', hora='00:00:00', fecha_creado='2017-12-28',hora_creado='00:00:00', visible=False, geom = Point(-0.2,-0.7), usuario=self.usuario)
        
        
    def _require_login(self):
        self.client.login(username='usuariomaster', password = 'mastermaster') 
            

    def test_get_valid_single_Casos(self):
        self._require_login()
        response = self.client.get('/casos/1')
        objeto = Casos.objects.get(pk=1)
        serializer = CasosListSerializador(objeto)
        #import pdb
        #pdb.set_trace()
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    
class CreateNewCasosTest(APITestCase):
    """ Test module for create new Casos """
    
    
    def setUp(self):
        self.usuario = User.objects.create(id=1, username='usuariomaster', first_name='Usuario', last_name='Master')
        self.usuario.set_password('mastermaster')
        self.usuario.save()
        self.valid_payload = {'lat':'0.1','lng':'0.1','descripcion':'derrumbre',  'fecha':'2017-10-17', 'hora':'00:00', 'fecha_creado':'2017-12-28', 'hora_creado':'00:00', 'visible':False,'usuario':1}
        self.invalid_payload = {'id':2, 'descripcion':'',  'fecha':'', 'hora':'00:00', 'fecha_creado':'2017-12-28', 'hora_creado':'00:00', 'visible':False,'usuario':1}
            
    def _require_login(self):
        self.client.login(username='usuariomaster', password = 'mastermaster')     
        
    def test_create_valid_casos(self):
        self._require_login()
        response = self.client.post("/casos", self.valid_payload, format='json')
        objeto = Casos.objects.get(pk=1)
        serializer = CasosSerializador(objeto)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  
        self.assertEqual(response.data, serializer.data)                    

    def test_create_invalid_casos(self):
        response = self.client.post("/casos", self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    

class UpdateSingleCasosTest(APITestCase):
    
    """ Test module for updating an existing  Casos record """
    
    
    def setUp(self):
        self.usuario = User.objects.create(id=1, username='usuariomaster', first_name='Usuario', last_name='Master')
        self.usuario.set_password('mastermaster')
        self.usuario.save()
        Casos.objects.create(id=1, descripcion='derrumbre', fecha='2017-10-17', hora='00:00:00', fecha_creado='2017-12-28',hora_creado='00:00:00', visible=False, geom = Point(-0.1,-0.6) ,usuario=self.usuario)
        Casos.objects.create(id=2, descripcion='deslave', fecha='2017-10-17', hora='00:00:00', fecha_creado='2017-12-28',hora_creado='00:00:00', visible=False, geom = Point(-0.2,-0.7), usuario=self.usuario)
        
        self.valid_payload = {'lat':'0.1','lng':'0.1','descripcion':'derrumbre',  'fecha':'2017-10-17', 'hora':'00:00', 'fecha_creado':'2017-12-28', 'hora_creado':'00:00', 'visible':False,'usuario':1}
        self.invalid_payload = {'descripcion':'derrumbre',  'fecha':'2017-10-17', 'hora':'00:00', 'fecha_creado':'2017-12-28', 'hora_creado':'00:00', 'visible':False,'usuario':1}
    
    def _require_login(self):
        self.client.login(username='usuariomaster', password = 'mastermaster')     

    def test_valid_update_casos(self):
        self._require_login()
        response = self.client.put('/casos/1', self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)           
        
    def test_invalid_update_casos(self):
        self._require_login()
        response = self.client.put('/casos/2', self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
class DeleteSingleCasosTest(APITestCase):
    """ Test module for deleting an existing  Casos record """
    
    
    def setUp(self):
        self.usuario = User.objects.create(id=1, username='usuariomaster', first_name='Usuario', last_name='Master')
        self.usuario.set_password('mastermaster')
        self.usuario.save()
        Casos.objects.create(id=1, descripcion='derrumbre', fecha='2017-10-17', hora='00:00:00', fecha_creado='2017-12-28',hora_creado='00:00:00', visible=False, geom = Point(-0.1,-0.6) ,usuario=self.usuario)
        Casos.objects.create(id=2, descripcion='deslave', fecha='2017-10-17', hora='00:00:00', fecha_creado='2017-12-28',hora_creado='00:00:00', visible=False, geom = Point(-0.2,-0.7), usuario=self.usuario) 

    def _require_login(self):
        self.client.login(username='usuariomaster', password = 'mastermaster')     

    def test_valid_delete_casos(self):
        self._require_login()
        response = self.client.delete('/casos/2')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)           
    
    def test_invalid_delete_casos(self):
        self._require_login()
        response = self.client.delete('/casos/4')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
   