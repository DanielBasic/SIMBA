from django.urls import path
from . import views

urlpatterns = [
    path("daniel", views.index, name='index_dashboard'),
    path("", views.index, name='dashboard'),
    path('retorna_total_vendido', views.retorna_total_vendido, name="retorna_total_vendido"),
    path('relatorio_faturamento', views.relatorio_faturamento, name="relatorio_faturamento"),
    path('relatorio_produtos', views.relatorio_produtos, name="relatorio_produtos"),
    path('relatorio_funcionario', views.relatorio_funcionario, name="relatorio_funcionario")
]
