# journals/views.py
from django.utils import timezone
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Habit, JournalLog
from .serializers import (
    HabitCreateSerializer,
    HabitListSerializer,
    JournalLogCreateSerializer,
    JournalLogListSerializer,
)


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

    @extend_schema(
        summary="Mark journal log as done",
        description="Update the done_at field of a journal log to the current date and time.",
        responses={200: JournalLogListSerializer},
    )
    @action(detail=True, methods=["post"], url_path="done")
    def mark_as_done(self, _, pk=None):
        try:
            journal_log = self.get_queryset().get(pk=pk)
            if journal_log.done_at is None:
                journal_log.done_at = timezone.now()
                journal_log.save()
                return Response(JournalLogListSerializer(journal_log).data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Log is already marked as done."}, status=status.HTTP_400_BAD_REQUEST)
        except JournalLog.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        summary="Change to habit",
        description="Update a log or todo to a habit",
        responses={200: JournalLogListSerializer},
    )
    @action(detail=True, methods=["post"], url_path="habitize")
    def create_habit_from_journal(self, request, pk=None):
        try:
            journal = self.get_queryset().get(pk=pk)
            if journal.type == JournalLog.LogType.HABIT:
                return Response({"detail": "This log is already a habit"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                journal.type = JournalLog.LogType.HABIT

                temp_habit_data = {"text": journal.text, "source_log": journal.id, "user": request.user.id}

                serializer = HabitCreateSerializer(data=temp_habit_data, context={"request": request})

                serializer.is_valid(raise_exception=True)

                journal.save()
                serializer.save()

                habits = Habit.objects.filter(user=request.user, deleted_at__isnull=True)
                habits_serializer = HabitListSerializer(habits, many=True)

                return Response(habits_serializer.data, status=status.HTTP_201_CREATED)
        except JournalLog.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
