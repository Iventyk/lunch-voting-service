from rest_framework import decorators, permissions, response, viewsets

from menus.models import Menu
from menus.selectors import menus_for_date
from menus.serializers import MenuSerializer


class MenuViewSet(viewsets.ModelViewSet):
    serializer_class = MenuSerializer
    queryset = Menu.objects.select_related("restaurant")

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy"}:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    @decorators.action(detail=False, methods=["get"], url_path="today")
    def today(self, request):
        serializer = self.get_serializer(menus_for_date(), many=True)
        return response.Response(serializer.data)
