from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # First try to get the token from Authorization header
        header_auth = super().authenticate(request)
        if header_auth is not None:
            return header_auth

        # If no Authorization header, try to get from cookie
        access_token = request.COOKIES.get("access_token")
        if access_token:
            validated_token = self.get_validated_token(access_token)
            return self.get_user(validated_token), validated_token
        return None
