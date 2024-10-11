# chatapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('chat_interactions/', views.ChatInteractionListView.as_view(), name='chatinteraction-list'),
    path('chat_interactions/<int:pk>/', views.ChatInteractionDetailView.as_view(), name='chatinteraction-detail'),
    path('chats/', views.ChatCreateView.as_view(), name='chat-create'),
    path('ml_service/<int:chat_int>/', views.MLServiceView.as_view(), name='ml-service'),
    
]