from rest_framework import viewsets, permissions
from django.views import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import action
from django.contrib.auth.models import User

from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from .permissions import IsChatAdminOrReadOnly, IsAuthorOrReadOnly


@login_required
def chats_list(request):
    return render(request, 'chat/chats.html')


@login_required
def chat_create(request):
    return render(request, 'chat/create_chat.html')


@login_required
def get_chat(request, pk):
    return render(request, 'chat/chat.html', {'id': pk})


@login_required
def edit_chat(request, pk):
    return render(request, 'chat/edit_chat.html', {'id': pk})


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated, IsChatAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(is_admin=self.request.user)
        chat_is_group = self.request.data["is_group"]
        if chat_is_group == 'false':
            members = self.request.data["members"]
            another_user = User.objects.get(pk=members)
            serializer.save(name=f"Чат между {self.request.user} и {another_user.username}")

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_chats(self, request):
        chat1 = Chat.objects.filter(is_admin=request.user.id)
        chat2 = Chat.objects.filter(members=request.user.id)
        chat = chat1.union(chat2)
        serializer = self.get_serializer(chat, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def check_existing_chat(self, request):
        another_user = User.objects.get(pk=request.query_params['another_user_id'])
        check_is_group = Chat.objects.filter(is_group=False)
        check_user1 = Chat.objects.filter(is_admin=request.user.id)
        check_user2 = Chat.objects.filter(members=request.user.id)
        check_another_user1 = Chat.objects.filter(is_admin=another_user.id)
        check_another_user2 = Chat.objects.filter(members=another_user.id)
        check_user = check_user1.union(check_user2)
        check_another_user = check_another_user1.union(check_another_user2)
        check_chat = check_is_group.intersection(check_user)
        final_check_chat = check_chat.intersection(check_another_user)
        if not final_check_chat:
            return Response([])
        else:
            serializer = self.get_serializer(final_check_chat, many=True)
            return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def get_chat_messages(self, request):
        messages = Message.objects.filter(chat=request.query_params['chat_id'])
        if not messages:
            return Response([])
        else:
            serializer = self.get_serializer(messages, many=True)
            return Response(serializer.data)


# class ChatMessagesView(View):
#     def get(self, request, chat_id):
#         chat = get_object_or_404(Chat, id=chat_id)
#         messages = Message.objects.filter(chat=chat)
#         serializer = MessageSerializer(messages, many=True)
#         return JsonResponse(serializer.data, safe=False)
