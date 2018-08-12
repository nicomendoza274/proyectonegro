from django.conf.urls import url
from . import views

app_name = 'cargarcamion'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'cargar', views.cargar, name='cargar'),
    url(r'report/', views.report, name='report'),
]