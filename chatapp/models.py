from django.db import models
from django.conf import settings
import uuid
from storages.backends.s3boto3 import S3Boto3Storage

class CustomS3Boto3Storage(S3Boto3Storage):
    location = 'uploads'  
    file_overwrite = False  
    default_acl = 'private'  

    def get_available_name(self, name, max_length=None):
        
        extension = name.split('.')[-1]  
        new_name = f"{uuid.uuid4().hex}.{extension}"
        return super().get_available_name(new_name, max_length)


class ChatInteraction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    chat_content = models.JSONField(default = dict)
    created_at = models.DateTimeField(auto_now_add=True)
    is_bot = models.BooleanField(default = False)
    chat_interaction = models.ForeignKey(ChatInteraction, on_delete=models.CASCADE, related_name='chats')

class ChatFile(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='aizen-uploads/', storage=CustomS3Boto3Storage())
    uploaded_at = models.DateTimeField(auto_now_add=True)