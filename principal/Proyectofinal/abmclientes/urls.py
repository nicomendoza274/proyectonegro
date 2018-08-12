from django.conf.urls import url
from . import views

app_name = 'abmclientes'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'crearcliente/', views.crearcliente, name='crearcliente'),
    url(r'editarcliente/', views.editarcliente, name='editarcliente'),
    url(r'eliminarcliente/', views.eliminarcliente, name='eliminarcliente'),
    url(r'buscar/', views.buscar, name='buscar'),
    url(r'recargar/', views.recargar, name='recargar'),
]