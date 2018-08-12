from django.conf.urls import url
from . import views

app_name = 'principal'

urlpatterns = [
    url(r'^$', views.index, name='index'),
]