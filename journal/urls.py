from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import JournalLogViewSet

router = DefaultRouter()
router.register(r"journal-logs", JournalLogViewSet, basename="journal-logs")

urlpatterns = [
    path("", include(router.urls)),
]
