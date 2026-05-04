from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User
from .serializers import UserLoginSerializer, UserRegistrationSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer


class LoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer
