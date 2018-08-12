from django.conf.urls import url
from . import views

app_name = 'despacharcamion'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'despachar/', views.despachar, name='despachar'),
]