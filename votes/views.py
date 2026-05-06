from rest_framework import decorators, mixins, permissions, response, status, viewsets

from votes.models import Vote
from votes.selectors import current_day_results
from votes.serializers import ResultSerializer, VoteCreateSerializer, VoteSerializer


class VoteViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Vote.objects.select_related("menu", "menu__restaurant").filter(
            user=self.request.user
        )

    def get_serializer_class(self):
        if self.action == "create":
            return VoteCreateSerializer
        return VoteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vote = serializer.save()
        status_code = (
            status.HTTP_201_CREATED
            if serializer.context.get("vote_created")
            else status.HTTP_200_OK
        )
        response_serializer = VoteSerializer(vote, context=self.get_serializer_context())
        return response.Response(response_serializer.data, status=status_code)

    @decorators.action(detail=False, methods=["get"], url_path="results")
    def results(self, request):
        serializer = ResultSerializer(current_day_results(), many=True)
        return response.Response(serializer.data)
