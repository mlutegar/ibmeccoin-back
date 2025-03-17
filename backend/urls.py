from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import TokenICViewSet, GrupoViewSet, AlunoViewSet, ConviteViewSet, MovimentacaoSaldoViewSet, CadastroView

router = DefaultRouter()
router.register(r'tokens', TokenICViewSet)
router.register(r'grupos', GrupoViewSet)
router.register(r'alunos', AlunoViewSet)
router.register(r'convites', ConviteViewSet)
router.register(r'movimentacoes', MovimentacaoSaldoViewSet)

urlpatterns = [
                  path('login/', obtain_auth_token, name='api_token_auth'),
                  path('cadastro/', CadastroView.as_view(), name='cadastro'),
              ] + router.urls
