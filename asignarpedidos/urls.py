from django.conf.urls import url
from . import views

app_name = 'asignarpedidos'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'asignar/', views.asignar, name='asignar'),
]