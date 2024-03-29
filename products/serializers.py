from rest_framework import serializers

from .models import Product
from users.models import User
from rest_framework.views import status, Response
from django.forms import ValidationError

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_seller', 'date_joined']

class ProductSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'description', 'price', 'quantity', 'is_active', 'seller']
        extra_kwargs = {'is_active': {'required': False}}

    def validate_quantity(self, value):
        if value<0:
            raise ValidationError("Ensure this value is greater than 0")
        return value

    def create(self, validated_data):
        seller = validated_data.pop('seller')
        product = Product.objects.create(seller=seller, **validated_data)
        return product

class GetProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['description', 'price', 'quantity', 'is_active', 'seller_id']
        read_only_fields = ['seller_id']
