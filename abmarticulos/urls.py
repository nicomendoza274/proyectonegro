from django.conf.urls import url
from . import views

app_name = 'abmarticulos'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'creararticulo/', views.creararticulo, name='creararticulo'),
    url(r'editararticulo/', views.editararticulo, name='editararticulo'),
    url(r'eliminararticulo/', views.eliminararticulo, name='eliminararticulo'),
    url(r'buscar/', views.buscar, name='buscar'),
    url(r'recargar/', views.recargar, name='recargar'),
]