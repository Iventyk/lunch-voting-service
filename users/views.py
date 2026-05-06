from rest_framework import mixins, permissions, viewsets

from users.models import Employee
from users.serializers import EmployeeCreateSerializer, EmployeeSerializer


class EmployeeViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Employee.objects.select_related("user")
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.action == "create":
            return EmployeeCreateSerializer
        return EmployeeSerializer
