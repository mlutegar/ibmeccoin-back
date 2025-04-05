from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from backend.views import ProcessarToken

schema_view = get_schema_view(
    openapi.Info(
        title="API de Conteúdos",
        default_version='v1',
        description="Documentação da API para o app de streaming de áudio e vídeo",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="suporte@exemplo.com"),
        license=openapi.License(name="Licença BSD"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url='https://gtddjango.fly.dev',
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("backend.urls")),
    path('', include("frontend.urls")),
    path('api/processar-token/<int:token_id>/', ProcessarToken.as_view(), name='processar-token'),

    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
