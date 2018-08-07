from django.conf.urls import url
from . import views

app_name = 'produccion'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'crearcopiaprod/', views.crearcopiaprod, name='crearcopiaprod'),
    url(r'editarproduccion/', views.editarproduccion, name='editarproduccion'),
    url(r'eliminarproduccion/', views.eliminarproduccion, name='eliminarproduccion'),
    url(r'recargar/', views.recargar, name='recargar'),
    url(r'index2/', views.index2, name='index2'),
    url(r'recargar2/', views.recargar2, name='recargar2'),
    url(r'buscar/', views.buscar, name='buscar'),
    url(r'eliminartodo/', views.eliminartodo, name='eliminartodo'),
    url(r'guardar/', views.guardar, name='guardar'),
    
]
'''fer
app_name = 'consultarproduccion'

urlpatterns = [
    url(r'^$', views.index, name='index2'),
    url(r'recargar2/', views.recargar, name='recargar2')
    url(r'buscarempleado/', views.buscarempleado, name='buscarempleado'),
    url(r'buscartipo/', views.buscartipo, name='buscartipo'),
    url(r'buscararticulo/', views.buscararticulo, name='buscararticulo')
]
'''