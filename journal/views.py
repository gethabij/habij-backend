from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckResponse(dict):
    status: bool


@extend_schema(
    tags=["System"],
    operation_id="health_check",
    description="API health check endpoint",
    responses={
        200: OpenApiResponse(response=HealthCheckResponse, description="Health check successful"),
    },
)
class HealthCheckView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        """
        Returns the health status of the API.
        """
        return Response({"status": True})
