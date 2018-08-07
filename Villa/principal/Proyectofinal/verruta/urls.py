from django.conf.urls import url
from . import views

app_name = 'verruta'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'registrarventa/', views.registrarventa, name='registrarventa'),
]