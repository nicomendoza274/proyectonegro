from django.conf.urls import url
from . import views

app_name = 'abmempleados'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'crearempleado/', views.crearempleado, name='crearempleado'),
    url(r'editarempleado/', views.editarempleado, name='editarempleado'),
    url(r'eliminarempleado/', views.eliminarempleado, name='eliminarempleado'),
    url(r'buscar/', views.buscar, name='buscar'),
    url(r'recargar/', views.recargar, name='recargar'),
]