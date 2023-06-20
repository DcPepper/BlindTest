import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.channel_layer.group_send(
                    self.room_group_name, {"type": "notify", "notify": ""}
                )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        if "message" in text_data_json:
            message = text_data_json["message"]
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat_message", "message": message}
            )
        elif "notify" in text_data_json:
            message = text_data_json["notify"]
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "notify", "notify": message}
            )
        elif "close" in text_data_json:
            message = text_data_json["close"]
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "notify", "close": message}
            )
        elif "answer" in text_data_json:
            message = text_data_json["answer"]
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "answer", "answer": message}
            )
        elif "next" in text_data_json:
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "next", "next": ""}
            )
        elif "endGame" in text_data_json:
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "endGame", "endGame": ""}
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
    

    async def notify(self, event):
        await self.send(text_data=json.dumps({"notify": event["notify"]}))
    
    async def answer(self, event):
        await self.send(text_data=json.dumps({"answer": event["answer"]}))
    
    async def next(self, event):
        await self.send(text_data=json.dumps({"next": event["next"]}))

    async def endGame(self, event):
        await self.send(text_data=json.dumps({"endGame": event["endGame"]}))

    