from django.urls import path
from rest_framework.authtoken import views

from .views import ProductView, ProductDetailView

urlpatterns = [
    path("products/", ProductView.as_view()),
    path("products/<pk>", ProductDetailView.as_view()),
]