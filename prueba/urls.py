from django.conf.urls import url
from . import views

app_name = 'prueba'

urlpatterns = [
    url(r'^$', views.index, name='index'),
]