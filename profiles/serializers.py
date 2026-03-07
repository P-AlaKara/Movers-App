from rest_framework import serializers
from .models import Profile, MoverProfile

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'role', 'phone_number', 'location', 'created_at']
        read_only_fields = ['role', 'created_at']


class MoverProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoverProfile
        fields = ['truck_size', 'service_area', 'price_range', 'availability', 'verification_status']
        read_only_fields = ['verification_status']  # only admins should set this

class PublicMoverSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    location = serializers.CharField(source='user.profile.location', read_only=True)

    class Meta:
        model = MoverProfile
        fields = ['id', 'username', 'location', 'truck_size', 'service_area', 'price_range', 'availability', 'verification_status']