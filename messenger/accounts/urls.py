from django.urls import path, include
from django.contrib.auth.views import LoginView
from rest_framework import routers

from .views import (register, user_logout, profiles_list, ProfileViewSet, my_profile,
                    another_profile, edit_profile)

router = routers.DefaultRouter()
router.register(r'profile', ProfileViewSet)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', user_logout, name='logout'),
    path('profiles/', profiles_list, name='profiles_list'),
    path('profile/<int:pk>/', another_profile, name='another_profile'),
    path('my_profile/', my_profile, name='my_profile'),
    path('edit_profile/', edit_profile, name="edit_profile"),
    path('api/', include(router.urls)),
]
