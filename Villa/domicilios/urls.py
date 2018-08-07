from django.conf.urls import url
from . import views

app_name = 'domicilios'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'guardar', views.guardar, name='guardar'),
]