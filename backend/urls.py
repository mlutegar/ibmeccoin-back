from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView

from .views import logout_view, get_user_info, generate_token_ic, generate_qr
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import get_saldo_aluno

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", logout_view, name="logout"),
    path("me/", get_user_info, name="get_user_info"),
    path('saldo/<int:matricula>/<int:turma_id>/', get_saldo_aluno, name='get_saldo_aluno'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path("tokenic/", generate_token_ic, name="generate_token_ic"),
    path("generate_qr", generate_qr, name="generate_qr"),
    path('auth/', include('django.contrib.auth.urls')),
]
