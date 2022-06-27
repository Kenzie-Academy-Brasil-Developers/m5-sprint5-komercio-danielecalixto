from rest_framework import generics
from rest_framework.views import APIView, Response, status

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .models import User
from .serializers import UserSerializer, LoginSerializer

class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ListNumUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        max_users = self.kwargs["num"]
        return self.queryset.order_by("-date_joined")[0:max_users]

class LoginView(APIView):
        def post(self, request):
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = authenticate(
                username = serializer.validated_data['email'],
                password = serializer.validated_data['password']
            )
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": token.key})
            return Response(
                {"detail": "Invalid email or password"}, status.HTTP_401_UNAUTHORIZED
            )
