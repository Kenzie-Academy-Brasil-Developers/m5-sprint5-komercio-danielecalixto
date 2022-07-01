from django.urls import path
from rest_framework.authtoken import views

from .views import UserView, LoginView, ListNumUsersView, UpdateUserView, DeactivateView

urlpatterns = [
    path("accounts/", UserView.as_view()),
    path("accounts/<pk>/", UpdateUserView.as_view()),
    path("accounts/<pk>/management/", DeactivateView.as_view()),
    path("accounts/newest/<int:num>/", ListNumUsersView.as_view()),
    path("login/", LoginView.as_view())
]