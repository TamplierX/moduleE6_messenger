from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatViewSet, MessageViewSet, chats_list, chat_create, get_chat, edit_chat

router = DefaultRouter()
router.register(r'chat', ChatViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', chats_list, name='chats_list'),
    path('chat/<int:pk>/', get_chat, name='chat'),
    path('chat/<int:pk>/edit', edit_chat, name='edit_chat'),
    path('chat/create', chat_create, name='chat_create'),
    path('api/', include(router.urls)),
    # path('api/chat/<int:chat_id>/messages/', ChatMessagesView.as_view(), name='chat_messages'),
]
