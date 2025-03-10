from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import logout


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = self.user if hasattr(self, "user") else request.user
        response.data.update({"user_id": user.id, "email": user.email})
        return response


@api_view(["POST"])
def logout_view(request):

    logout(request)
    return Response({"message": "Logout realizado com sucesso."})
