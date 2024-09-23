from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
import json

class ClienteTest(TestCase):
    def setUp(self):
        # Configura os dados iniciais, como criar um usuário de teste
        self.client = APIClient()
        
        # Aqui você pode criar um usuário de teste, se necessário
        # Exemplo:
        # self.user = User.objects.create_user(
        #     username='testuser',
        #     email='medeiros0441@gmail.com',
        #     password='S@m044119'
        # )
    def test_get_clientes_by_empresa(self):
        # Passo 1: Fazer o login
        data = {
            "email": "medeiros0441@gmail.com",
            "senha": "S@m044119"
        }
        login_url = reverse('public-login')
        print("Login URL:", login_url)
        login_response = self.client.post('/api/public/login/', json.dumps(data), content_type='application/json')


        # Verifica se o login foi bem-sucedido
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        # Obtém o token do cookie da resposta
        token_cookie = login_response.cookies.get("user_token")

        # Verifica se o cookie do token foi retornado
        self.assertIsNotNone(token_cookie, "Token de autenticação não foi gerado.")

        # Passo 2: Requisição protegida para o método get_clientes_by_empresa
        self.client.cookies["user_token"] = token_cookie.value  # Adiciona o token de autenticação

        # Faz a requisição para o endpoint de clientes da empresa
        response = self.client.get("/api/clientes/clientes-empresa/")

        # Verifica se a resposta está OK (200) e exibe os dados retornados
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)  # Exibe os dados de clientes

        # Caso deseje verificar mais detalhes, pode testar os dados retornados
        self.assertIn("data", response.data)
