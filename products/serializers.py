from rest_framework import serializers

from .models import Product
from users.models import User

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'description', 'price', 'quantity', 'is_active']
        read_only_fields = ['seller']
        extra_kwargs = {'is_active': {'required': False}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = User.objects.get(id=instance.user_id)
        seller = {}
        seller['id'] = user.id
        seller['email'] = user.email
        seller['first_name'] = user.first_name
        seller['last_name'] = user.last_name
        seller['is_seller'] = user.is_seller
        seller['date_joined'] = user.date_joined
        representation['seller'] = seller
        return representation

    def create(self, validated_data):
        user = validated_data.pop('user')
        product = Product.objects.create(user=user, **validated_data)
        return product

class GetProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['description', 'price', 'quantity', 'is_active']
        read_only_fields = ['seller_id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['seller_id'] = instance.user_id
        return representation