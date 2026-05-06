from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import (
    decorators,
    mixins,
    permissions,
    response,
    status,
    viewsets,
)

from votes.models import Vote
from votes.selectors import current_day_results
from votes.serializers import (
    ResultSerializer,
    VoteCreateSerializer,
    VoteSerializer,
)


API_VERSION_HEADER = OpenApiParameter(
    name="X-API-Version",
    type=int,
    location=OpenApiParameter.HEADER,
    required=False,
    description=(
        "Mobile API version. Version 1 allows one vote per day; "
        "version 2 allows changing a vote. Defaults to 2."
    ),
)


class VoteViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Vote.objects.select_related("menu", "menu__restaurant").filter(
            user=self.request.user
        )

    def get_serializer_class(self):
        if self.action == "create":
            return VoteCreateSerializer
        return VoteSerializer

    @extend_schema(
        parameters=[API_VERSION_HEADER],
        request=VoteCreateSerializer,
        responses={200: VoteSerializer, 201: VoteSerializer},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vote = serializer.save()
        status_code = (
            status.HTTP_201_CREATED
            if serializer.context.get("vote_created")
            else status.HTTP_200_OK
        )
        response_serializer = VoteSerializer(
            vote, context=self.get_serializer_context()
        )
        return response.Response(response_serializer.data, status=status_code)

    @extend_schema(
        description="Return current-day voting results grouped by menu.",
        responses=ResultSerializer(many=True),
    )
    @decorators.action(detail=False, methods=["get"], url_path="results")
    def results(self, request):
        serializer = ResultSerializer(current_day_results(), many=True)
        return response.Response(serializer.data)
