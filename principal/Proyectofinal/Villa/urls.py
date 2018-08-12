"""Villa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', include('principal.urls')),
    url(r'^abmclientes/', include('abmclientes.urls')),
    url(r'^abmarticulos/', include('abmarticulos.urls')),
    url(r'^abminsumos/', include('abminsumos.urls')),
    url(r'^abmempleados/', include('abmempleados.urls')),
    url(r'^abmpedidos/', include('abmpedidos.urls')),
    url(r'^abmproveedores/', include('abmproveedores.urls')),
    url(r'^asignarpedidos/', include('asignarpedidos.urls')),
    url(r'^log/', include('log.urls')),
    url(r'^verruta/', include('verruta.urls')),
    url(r'^cargarcamion/', include('cargarcamion.urls')),
    url(r'^descargarcamion/', include('descargarcamion.urls')),
    url(r'^despacharcamion/', include('despacharcamion.urls')),
    url(r'^ventas/', include('ventas.urls')),
    url(r'^domicilios/', include('domicilios.urls')),
    url(r'^produccion/', include('produccion.urls')),
    url(r'^stockart/', include('stockart.urls')),
    url(r'^stock/', include('stock.urls')),
    url(r'^prueba/', include('prueba.urls')),
    url(r'^remito/', include('remito.urls'))
]
