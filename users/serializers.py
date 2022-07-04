from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User

class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'is_seller', 'date_joined', 'is_active']
        extra_kwargs = {
            'is_seller': {'required': True},
            'is_active': {'required': False, 'write_only': True},
            'password': {'write_only': True},
            'date_joined': {'read_only': True},
            'email': {'validators': [UniqueValidator(queryset=User.objects.all(), message='This email already exists.')]}
            }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class DeactivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_seller', 'date_joined', 'is_active']
        read_only_fields = ['id', 'email', 'first_name', 'last_name', 'is_seller', 'date_joined']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)