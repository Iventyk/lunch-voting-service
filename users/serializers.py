from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Employee

User = get_user_model()


class EmployeeCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(required=False, allow_blank=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "username",
            "password",
            "email",
            "full_name",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        username = validated_data.pop("username")
        password = validated_data.pop("password")
        email = validated_data.pop("email", "")
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        return Employee.objects.create(user=user, **validated_data)


class EmployeeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Employee
        fields = ["id", "username", "email", "full_name", "created_at"]
