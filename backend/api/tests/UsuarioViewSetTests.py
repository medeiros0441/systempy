# tests/test_views.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import UsuarioModel
from django.contrib.auth.hashers import make_password
from api.serializers import UsuarioSerializer
class UsuarioViewSetTests(APITestCase):
    
    def test_list_usuarios(self):
            """
            Testa a listagem de todos os usuários.
            """
            response = self.client.get('api/usuarios/')  # Faz uma requisição GET para a URL de listagem

            # Verifica se o status code é 200 (OK)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Serializa os dados esperados
            usuarios = UsuarioModel.objects.all()
            serializer = UsuarioSerializer(usuarios, many=True)

            # Verifica se os dados retornados são os mesmos que os serializados
            self.assertEqual(response.data, serializer.data)

            # Verifica se a quantidade de usuários retornados está correta
            self.assertEqual(len(response.data), 2)