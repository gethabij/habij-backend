# users/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomTokenRefreshView, LoginView, TokenVerifyView, UserViewSet, logout_view

router = DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/login/", LoginView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("auth/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("auth/logout/", logout_view, name="auth_logout"),
]
