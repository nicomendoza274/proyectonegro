from django.conf.urls import url
from . import views

app_name = 'descargarcamion'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'descargar', views.descargar, name='descargar'),
    url(r'report/', views.report, name='report'),
]