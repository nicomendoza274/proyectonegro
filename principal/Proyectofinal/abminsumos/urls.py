from django.conf.urls import url
from . import views

app_name = 'abminsumos'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'crearinsumo/', views.crearinsumo, name='crearinsumo'),
    url(r'editarinsumo/', views.editarinsumo, name='editarinsumo'),
    url(r'eliminarinsumo/', views.eliminarinsumo, name='eliminarinsumo'),
    url(r'buscar/', views.buscar, name='buscar'),
    url(r'recargar/', views.recargar, name='recargar'),
]