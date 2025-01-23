# journals/serializers.py
from rest_framework import serializers
from .models import Habit, JournalLog

class JournalLogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalLog
        fields = ("text", "type", "scheduled_for")
        extra_kwargs = {
            "scheduled_for": {"required": False},
        }

    def validate(self, data):
        if data.get("type") == JournalLog.LogType.TODO and not data.get("scheduled_for"):
            raise serializers.ValidationError({"scheduled_for": "Scheduled time is required for todo type"})
        return data

    def create(self, validated_data):
        journal_log = JournalLog.objects.create(**validated_data)

        if validated_data.get("type") == JournalLog.LogType.HABIT:
            Habit.objects.create(text=validated_data["text"], user=validated_data["user"], source_log=journal_log)

        return journal_log


class JournalLogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalLog
        fields = ("id", "text", "type", "scheduled_for", "done_at", "created_at")

class HabitCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ("text", "source_log", "user", "id")
        extra_kwargs = {
            "user": {"write_only": True},
        }

class HabitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ("id", "text")