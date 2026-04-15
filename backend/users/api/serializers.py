from rest_framework import serializers
from users.models import User
from vendors.models import VendorProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    store_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'user_type', 'store_name']

    def create(self, validated_data):
        user_type = validated_data.get('user_type', User.UserType.CONSUMER)
        store_name = validated_data.pop('store_name', None)
        password = validated_data.pop('password')
        
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        if user_type == User.UserType.VENDOR:
            if not store_name:
                store_name = f"{user.username}'s Store"
            VendorProfile.objects.create(user=user, store_name=store_name, is_approved=False)

        return user
