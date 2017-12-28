import json
from rest_framework import status
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from capas.models import Suceso
from django.contrib.auth.models import User
from capas.serializadores.sucesos import SucesoListSerializador, SucesoSerializador
from capas.serializadores.usuarios import UsuarioListSerializador, UsuarioSerializador
from datetime import datetime, date, time



class GETAllSucesoTest(APITestCase):
    """ Test module for GET all Suceso API """
    
    def setUp(self):
        self.usuario = User.objects.create(username='usuariomaster', first_name='Usuario', last_name='Master')
        Suceso.objects.create(descripcion='derrumbre',tipo='deslave', fecha='2017-10-17', hora='00:00:00', fecha_creado='2017-12-28',hora_creado='00:00:00', visible=False,usuario=self.usuario)
        Suceso.objects.create(descripcion='deslave',tipo='deslave', fecha='2017-10-17', hora='00:00:00', fecha_creado='2017-12-28',hora_creado='00:00:00', visible=False,usuario=self.usuario)
        Suceso.objects.create(descripcion='licuacion edificio',tipo='licuacion', fecha='2017-10-17', hora='00:00:00', fecha_creado='2017-12-28',hora_creado='00:00:00', visible=False,usuario=self.usuario)
        

    def test_list_Suceso(self):
        response = self.client.get("/sucesos")
        objeto = Suceso.objects.all()
        serializer = SucesoSerializador(objeto, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)   
       
class GETSingleSucesoTest(APITestCase):
    
    """ Test module for GET single Suceso API """
    
    def setUp(self):
        self.usuario = User.objects.create(username='usuariomaster', first_name='Usuario', last_name='Master')
        Suceso.objects.create(id=1, descripcion='derrumbre',tipo='Deslave', fecha='2017-10-17', hora='00:00:00', fecha_creado='2017-12-28',hora_creado='00:00:00', visible=False,usuario=self.usuario)
        Suceso.objects.create(id=2, descripcion='deslave',tipo='Deslave', fecha='2017-10-17', hora='00:00:00', fecha_creado='2017-12-28',hora_creado='00:00:00', visible=False,usuario=self.usuario)
        Suceso.objects.create(id=3, descripcion='licuacion edificio',tipo='licuacion', fecha='2017-10-17', hora='00:00:00', fecha_creado='2017-12-28',hora_creado='00:00:00', visible=False,usuario=self.usuario)
        
    
    def test_get_valid_single_Suceso(self):
        response = self.client.get('/sucesos/1')
        objeto = Suceso.objects.get(pk=1)
        serializer = SucesoListSerializador(objeto)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_get_invalid_single_Suceso(self):
        response = self.client.get('/sucesos/4')
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
    

class CreateNewSucesoTest(APITestCase):
    """ Test module for create new Suceso """
    
    def setUp(self):
        self.usuario = User.objects.create(id=1, username='usuariomaster', first_name='Usuario', last_name='Master')
        self.valid_payload = {'descripcion':'derrumbre', 'tipo':'Deslave', 'fecha':'2017-10-17', 'hora':'00:00',\
         'fecha_creado':'2017-12-28', 'hora_creado':'00:00', 'visible':False,'usuario':1}
        self.invalid_payload ={'descripcion':'derrumbre','tipo':'deslave', 'fecha':'2017-10-17', 'hora':'00:00:00', 'fecha_creado':'2017-12-28', 'hora_creado':'00:00:00', 'visible':False,'usuario':2}
            

    def test_create_valid_parametro(self):
        response = self.client.post("/sucesos", self.valid_payload, format='json')
        objeto = Suceso.objects.get(pk=1)
        serializer = SucesoSerializador(objeto)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  
        self.assertEqual(response.data, serializer.data)                    

    def test_create_invalid_parametro(self):
        response = self.client.post("/sucesos", self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    


class UpdateSingleSucesoTest(APITestCase):
    
    """ Test module for updating an existing  Suceso record """
    
    def setUp(self):
        self.usuario = User.objects.create(id=1, username='usuariomaster', first_name='Usuario', last_name='Master')
        Suceso.objects.create(id=1, descripcion='derrumbre',tipo='Deslave', fecha='2017-10-17', hora='00:00:00', fecha_creado='2017-12-28',hora_creado='00:00:00', visible=False,usuario=self.usuario)
        Suceso.objects.create(id=2, descripcion='deslave',tipo='Deslave', fecha='2017-10-17', hora='00:00:00', fecha_creado='2017-12-28',hora_creado='00:00:00', visible=False,usuario=self.usuario)
        Suceso.objects.create(id=3, descripcion='licuacion edificio',tipo='Licuacion', fecha='2017-10-17', hora='00:00:00', fecha_creado='2017-12-28',hora_creado='00:00:00', visible=False,usuario=self.usuario)
        
        self.valid_payload = {'descripcion':'derrumbre', 'tipo':'Deslave', 'fecha':'2017-10-17', 'hora':'00:00', 'fecha_creado':'2017-12-28', 'hora_creado':'00:00', 'visible':False,'usuario':1}
        self.invalid_payload ={'descripcion':'derrumbre','tipo':'deslave', 'fecha':'2017-10-17', 'hora':'00:00:00', 'fecha_creado':'2017-12-28', 'hora_creado':'00:00:00', 'visible':False,'usuario':2}
    
    def test_valid_update_parametro(self):
        response = self.client.put('/sucesos/1', self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)           
        
    def test_invalid_update_parametro(self):
        response = self.client.put('/sucesos/3', self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
class DeleteSingleSucesoTest(APITestCase):
    """ Test module for deleting an existing  Suceso record """
    
    def setUp(self):
        self.usuario = User.objects.create(id=1, username='usuariomaster', first_name='Usuario', last_name='Master')
        Suceso.objects.create(id=1, descripcion='derrumbre',tipo='Deslave', fecha='2017-10-17', hora='00:00:00', fecha_creado='2017-12-28',hora_creado='00:00:00', visible=False,usuario=self.usuario)
        Suceso.objects.create(id=2, descripcion='deslave',tipo='Deslave', fecha='2017-10-17', hora='00:00:00', fecha_creado='2017-12-28',hora_creado='00:00:00', visible=False,usuario=self.usuario)
        Suceso.objects.create(id=3, descripcion='licuacion edificio',tipo='Licuacion', fecha='2017-10-17', hora='00:00:00', fecha_creado='2017-12-28',hora_creado='00:00:00', visible=False,usuario=self.usuario)
        
    def test_valid_delete_parametro(self):
        response = self.client.delete('/sucesos/2')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)           
    
    def test_invalid_delete_parametro(self):
        response = self.client.delete('/sucesos/4')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    