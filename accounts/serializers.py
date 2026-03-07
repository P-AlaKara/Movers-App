from rest_framework import serializers
from django.contrib.auth.models import User
from profiles.models import MoverProfile

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    ROLE_CHOICES = [('customer', 'Customer'), ('mover', 'Mover')]
    role = serializers.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        role = validated_data.pop('role')
        validated_data.pop('password2')
        password = validated_data.pop('password1')

        user = User.objects.create_user(password=password, **validated_data)

        user.profile.role = role
        user.profile.save()

        if role == 'mover':
            MoverProfile.objects.create(user=user)

        return user