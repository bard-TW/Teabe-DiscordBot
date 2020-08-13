from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer


consumer_object_list = []


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        """
        客户端連結後自動觸發
        """
        self.accept()
        consumer_object_list.append(self)

    def websocket_receive(self, message):
        """
        客戶端發消息
        """
        text = message.get('text')
        for obj in consumer_object_list:
            obj.send(text_data=text)

    def websocket_disconnect(self, message):
        """
        客户端斷開連線自動觸發
        """
        consumer_object_list.remove(self)
        raise StopConsumer()