from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .forms import SignUpForm
from .models import Profile
from .serializers import ProfileSerializer
from .permissions import IsUserOrReadOnly


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return render(request, 'accounts/logout.html', {})


@login_required
def profiles_list(request):
    return render(request, 'accounts/profiles.html')


@login_required
def my_profile(request):
    return render(request, 'accounts/my_profile.html')


@login_required
def another_profile(request, pk):
    return render(request, 'accounts/another_profile.html', {'id': pk})


@login_required
def edit_profile(request):
    return render(request, 'accounts/edit_profile.html')


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserOrReadOnly]

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def profiles(self, request):
        profile = Profile.objects.exclude(user_id=request.user.id)
        serializer = self.get_serializer(profile, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated, IsUserOrReadOnly])
    def my_profile(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    @action(detail=False, methods=['get', 'patch'], permission_classes=[permissions.IsAuthenticated, IsUserOrReadOnly])
    def edit_my_profile(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
