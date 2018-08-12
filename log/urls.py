from django.conf.urls import url
from . import views

app_name = 'log'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'iniciarsesion', views.iniciarsesion, name='iniciarsesion'),
    url(r'recuperarpassword', views.recuperarpassword, name='recuperarpassword'),
    url(r'cambiarpassword', views.cambiarpassword, name='cambiarpassword'),
    url(r'enviarcodigo', views.enviarcodigo, name='enviarcodigo'),
    url(r'ingresarcodigo', views.ingresarcodigo, name='ingresarcodigo'),
    url(r'salir', views.salir, name='salir'),
]