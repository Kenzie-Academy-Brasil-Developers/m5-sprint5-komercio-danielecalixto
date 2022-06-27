from django.urls import path
from rest_framework.authtoken import views

from .views import UserView, LoginView, ListNumUsersView

urlpatterns = [
    path("accounts/", UserView.as_view()),
    path("login/", LoginView.as_view()),
    path("accounts/newest/<int:num>/", ListNumUsersView.as_view())
]