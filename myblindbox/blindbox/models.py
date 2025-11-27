from django.db import models
from django.contrib.auth import get_user_model

class BlindBox(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"盲盒内容: {self.content}"

class Message(models.Model):

    sender = models.ForeignKey(get_user_model(), related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(get_user_model(), related_name='received_messages', on_delete=models.CASCADE)
    blindbox = models.ForeignKey(BlindBox, related_name='messages', on_delete=models.CASCADE)  # Relate to BlindBox
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"消息内容: {self.content} - 发送者: {self.sender.username}"

