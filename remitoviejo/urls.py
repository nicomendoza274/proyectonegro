from django.conf.urls import url
from . import views

app_name = 'remito'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'index2/', views.index2, name='index2'),
    url(r'index3/', views.index3, name='index3'),
    url(r'recargar/', views.recargar, name='recargar'),
    url(r'recargar2/', views.recargar2, name='recargar2'),
    url(r'validarremito/', views.validarremito, name='validarremito'),
    url(r'crearcopiaremito/', views.crearcopiaremito, name='crearcopiaremito'),
    url(r'guardar/', views.guardar, name='guardar'),
    url(r'eliminartodo/', views.eliminartodo, name='eliminartodo'),
    url(r'editardetalle/', views.editardetalle, name='editardetalle'),
    url(r'eliminardetalle/', views.eliminardetalle, name='eliminardetalle'),
    url(r'guardarcabecera/', views.guardarcabecera, name='guardarcabecera'),
    url(r'editarcabecera/', views.editarcabecera, name='editarcabecera'),
    url(r'buscar/', views.buscar, name='buscar')
]