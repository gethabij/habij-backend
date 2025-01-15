# journals/views.py
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import JournalLog
from .serializers import JournalLogCreateSerializer, JournalLogListSerializer


class JournalLogFilter(filters.FilterSet):
    date = filters.DateFilter(field_name="created_at__date", help_text="Filter by date (YYYY-MM-DD)")
    type = filters.ChoiceFilter(choices=JournalLog.LogType.choices, help_text="Filter by log type (habit/log/todo)")

    class Meta:
        model = JournalLog
        fields = ["date", "type"]


class JournalLogViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = JournalLogFilter

    def get_serializer_class(self):
        if self.action == "create":
            return JournalLogCreateSerializer
        return JournalLogListSerializer

    def get_queryset(self):
        return JournalLog.objects.filter(user=self.request.user, deleted_at__isnull=True).order_by("-created_at")

    @extend_schema(
        summary="Create journal log",
        description="Create a new journal log entry. If type is 'todo', scheduled_for is required",
        responses={201: JournalLogListSerializer},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        journal_log = serializer.save(user=request.user)

        return Response(JournalLogListSerializer(journal_log).data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="List journal logs",
        description="Get list of journal logs with optional date and type filters",
        parameters=[
            OpenApiParameter(name="date", description="Filter by date (YYYY-MM-DD)", required=False, type=str),
            OpenApiParameter(
                name="type",
                description="Filter by log type (habit/log/todo)",
                required=False,
                type=str,
                enum=["habit", "log", "todo"],
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
