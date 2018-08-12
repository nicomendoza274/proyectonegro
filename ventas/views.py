from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from principal.models import Ventas
from django.contrib.auth.models import User
from django.db.models import Q
from django.db import IntegrityError
import datetime
from datetime import date
# Create your views here.


def index(request):
    ventas = Ventas.objects.all().order_by('-fecha')
    return render(request, "ventas/ventas.html", {'ventas': ventas})
