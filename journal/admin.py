# journals/admin.py
from django.contrib import admin

from .models import Habit, JournalLog


@admin.register(JournalLog)
class JournalLogAdmin(admin.ModelAdmin):
    list_display = ("text", "user", "type", "scheduled_for", "done_at", "is_deleted", "created_at")
    list_filter = ("type", "done_at", "deleted_at", "created_at")
    search_fields = ("text", "user__email")
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("user",)
    date_hierarchy = "created_at"

    def is_deleted(self, obj):
        return obj.is_deleted

    is_deleted.boolean = True


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("text", "user", "is_deleted", "created_at")
    list_filter = ("deleted_at", "created_at")
    search_fields = ("text", "user__email")
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("user", "source_log")
    date_hierarchy = "created_at"

    def is_deleted(self, obj):
        return obj.is_deleted

    is_deleted.boolean = True
