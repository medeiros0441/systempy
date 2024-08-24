# api/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class SomeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Código para executar quando a conexão WebSocket for estabelecida
        await self.accept()

    async def disconnect(self, close_code):
        # Código para executar quando a conexão WebSocket for fechada
        pass

    async def receive(self, text_data):
        # Código para processar mensagens recebidas pelo WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')

        # Enviar uma resposta para o WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
