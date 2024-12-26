from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=32, null=True, blank=True)
    last_name = models.CharField(max_length=32, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/',
                               default='avatars/default.jpg',
                               blank=True,
                               validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))])
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.user)
