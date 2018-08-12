from django.conf.urls import url
from . import views

app_name = 'stock'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'buscar/', views.buscar, name='buscar'),
    url(r'recargar/', views.recargar, name='recargar'),
    url(r'report/', views.report, name='report'),
]