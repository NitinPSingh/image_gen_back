import random
import json
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ChatInteraction, Chat, ChatFile
from django.core.files.base import ContentFile
from .serializers import ChatInteractionSerializer, ChatSerializer, ChatFileSerializer
import requests
from botocore.exceptions import ClientError
from rest_framework.parsers import MultiPartParser, FormParser

class ChatInteractionListView(generics.ListCreateAPIView):
    serializer_class = ChatInteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatInteraction.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        
        existing_interaction = ChatInteraction.objects.filter(user=request.user).first()
        
        serializer = self.get_serializer(data={'user':request.user.id})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ChatInteractionDetailView(generics.RetrieveAPIView):
    queryset = ChatInteraction.objects.all()
    serializer_class = ChatInteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data  
        
        chats = Chat.objects.filter(chat_interaction=instance)
        chat_serializer = ChatSerializer(chats, many=True)
        data['chats'] = chat_serializer.data

        
        for chat in data['chats']:
            files = ChatFile.objects.filter(chat_id=chat['id'])
            file_serializer = ChatFileSerializer(files, many=True)
            chat['files'] = file_serializer.data

        return Response(data)

class ChatCreateView(generics.CreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        chat_data = {
            'chat_interaction': request.data.get('chat_interaction'),
            'chat_content': json.loads(request.data.get('chat_content', '{}')),
            'is_bot': request.data.get('is_bot', False)
        }

        file_data = request.FILES.get('file')

        chat_serializer = self.get_serializer(data=chat_data)
        chat_serializer.is_valid(raise_exception=True)
        chat = chat_serializer.save()

        if file_data:
            file_serializer = ChatFileSerializer(data={'file': file_data, 'chat': chat.id})
            file_serializer.is_valid(raise_exception=True)
            file_serializer.save()

            
            chat_serializer.data['file'] = file_serializer.data

        return Response(chat_serializer.data, status=status.HTTP_201_CREATED)
    

class MLServiceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        chat_interaction = kwargs.get('chat_int')

        chat_data = {
            'chat_interaction': chat_interaction,
            'chat_content': json.loads(request.data.get('chat_content', '{}')),
            'is_bot': request.data.get('is_bot', True)
        }

        try:
            
            chat_serializer = ChatSerializer(data=chat_data)
            chat_serializer.is_valid(raise_exception=True)
            chat = chat_serializer.save()
            width = random.randint(400, 600)
            height = random.randint(400, 600)

            
            image_url = f"https://picsum.photos/{width}/{height}"
            response = requests.get(image_url, timeout=10)
            
            if response.status_code != 200:
                return Response({'error': 'Failed to fetch image'}, status=status.HTTP_400_BAD_REQUEST)

            
            file_data = {
                'file': ContentFile(response.content, "randomfile"),  
                'chat': chat.id
            }
            file_serializer = ChatFileSerializer(data=file_data)
            if file_serializer.is_valid():
                file_serializer.save()

            
            return Response(chat_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)