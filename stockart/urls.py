from django.conf.urls import url
from . import views

app_name = 'stockart'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'recargar/', views.recargar, name='recargar'),
    url(r'busart/', views.busart, name='busart'),
    url(r'report/', views.report, name='report'),
]