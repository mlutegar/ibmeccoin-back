from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tarefas/', views.tarefas, name='tarefas'),
    path('adicionar_tarefa_ao_dia/<int:tarefa_id>/', views.adicionar_tarefa_ao_dia, name='adicionar_tarefa_ao_dia'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('criar_tarafa/', views.criar_tarefa, name='criar_tarefa'),
    path('obter_info_tarefa/', views.obter_info_tarefa, name='obter_info_tarefa'),
    ]
