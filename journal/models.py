# journals/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User


class JournalLog(models.Model):
    class LogType(models.TextChoices):
        HABIT = "habit", _("Habit")
        LOG = "log", _("Log")
        TODO = "todo", _("Todo")

    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="journal_logs")
    done_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=5, choices=LogType.choices, default=LogType.LOG)
    scheduled_for = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("journal log")
        verbose_name_plural = _("journal logs")
        db_table = "journal_logs"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_type_display()} by {self.user.email}: {self.text[:50]}"

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    @property
    def is_done(self):
        return self.done_at is not None


class Habit(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits")
    source_log = models.ForeignKey(JournalLog, on_delete=models.SET_NULL, null=True, related_name="derived_habits")
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("habit")
        verbose_name_plural = _("habits")
        db_table = "habits"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Habit by {self.user.email}: {self.text[:50]}"

    @property
    def is_deleted(self):
        return self.deleted_at is not None
