from rest_framework import generics, permissions
from users.models import User
from .serializers import UserRegistrationSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer
