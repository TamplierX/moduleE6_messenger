from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    avatar = serializers.ImageField(allow_null=True, required=False)

    class Meta:
        model = Profile
        fields = ['user_id', 'username', 'first_name', 'last_name', 'bio', 'avatar']

    # def update(self, instance, validated_data):
    #     instance.first_name = validated_data.get("first_name", instance.first_name)
    #     instance.last_name = validated_data.get("last_name", instance.last_name)
    #     instance.bio = validated_data.get("bio", instance.bio)
    #     instance.avatar = validated_data.get("avatar", instance.avatar)
    #     instance.save()
    #     return instance


