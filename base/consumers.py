import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .chatbot.rag_handler import RAGHandler
import asyncio
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.rag_handler = None

    async def connect(self):
        await self.accept()
        self.rag_handler = RAGHandler()

        if self.rag_handler.vector_store is None:
            await self.init_rag_handler()

    @database_sync_to_async
    def init_rag_handler(self):
        from dashboard.models import Event
        events = Event.objects.all()
        self.rag_handler.create_vector_store(events)

    @database_sync_to_async
    def get_rag_response(self, query, chat_history):
        return self.rag_handler.get_response(query, chat_history)

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        query = text_data_json['message']
        chat_history = text_data_json.get('chat_history', [])

        # Indiquer que le bot est en train d'écrire
        await self.send(json.dumps({
            'type': 'typing_start'
        }))

        # Obtenir la réponse de manière asynchrone
        response = await self.get_rag_response(query, chat_history)

        # Envoyer la réponse
        await self.send(json.dumps({
            'type': 'chat_message',
            'message': response
        }))