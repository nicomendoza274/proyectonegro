from django.conf.urls import url
from . import views

app_name = 'abmpedidos'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'crearpedido/', views.crearpedido, name='crearpedido'),
    url(r'validardni/', views.validardni, name='validardni'),
    url(r'modificartotal/', views.modificartotal, name='modificartotal'),
    url(r'buscartipos/', views.buscartipos, name='buscartipos'),
    url(r'editarpedido/', views.editarpedido, name='editarpedido'),
    url(r'eliminarpedido/', views.eliminarpedido, name='eliminarpedido'),
    url(r'buscar/', views.buscar, name='buscar'),
    url(r'recargar/', views.recargar, name='recargar'),

]
