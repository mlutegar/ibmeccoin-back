from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from .views import logout_view, get_user_info, generate_token_ic
from rest_framework_simplejwt.views import TokenRefreshView
from .views import user_login_view, get_saldo_aluno

urlpatterns = [
    path("login/", user_login_view, name="aluno_login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", logout_view, name="logout"),
    path("me/", get_user_info, name="get_user_info"),
    path('saldo/<int:matricula>/<int:turma_id>/', get_saldo_aluno, name='get_saldo_aluno'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path("tokenic/", generate_token_ic, name="generate_token_ic"),
]
