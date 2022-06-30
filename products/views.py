from .serializers import ProductSerializer, GetProductSerializer
from .models import Product
from utils.mixins import SerializerByMethodMixin
from rest_framework import generics
from .permissions import ProductDetailPermission, ProductPermission
from rest_framework.authentication import TokenAuthentication

class ProductView(SerializerByMethodMixin, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ProductPermission]
    queryset = Product.objects.all()
    serializer_map = {
        'GET': GetProductSerializer,
        'POST': ProductSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class ProductDetailView(SerializerByMethodMixin, generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ProductDetailPermission]
    queryset = Product.objects.all()
    serializer_map = {
        'GET': GetProductSerializer,
        'PATCH': ProductSerializer,
    }

