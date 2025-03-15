from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views import logout_view, get_user_info, TokenICViewSet
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import get_saldo_aluno

router = DefaultRouter()
router.register(r'tokens', TokenICViewSet)

urlpatterns = [
    path('login/', obtain_auth_token, name='api_token_auth'),
] + router.urls

# urlpatterns = [
#     path("me/", get_user_info, name="get_user_info"),
#     path('saldo/<int:matricula>/<int:turma_id>/', get_saldo_aluno, name='get_saldo_aluno'),
#     path('schema/', SpectacularAPIView.as_view(), name='schema'),
#     path("generate_qr", generate_qr, name="generate_qr"),
#     path('auth/', include('django.contrib.auth.urls')),
# ]
