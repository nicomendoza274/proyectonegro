from django.conf.urls import url
from . import views

app_name = 'abmproveedores'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'crearproveedor/', views.crearproveedor, name='crearproveedor'),
    url(r'editarproveedor/', views.editarproveedor, name='editarproveedor'),
    url(r'editarlistaproveedor/', views.editarlistaproveedor, name='editarlistaproveedor'),
    url(r'eliminarproveedor/', views.eliminarproveedor, name='eliminarproveedor'),
    url(r'buscar/', views.buscar, name='buscar'),
    url(r'recargar/', views.recargar, name='recargar'),
]