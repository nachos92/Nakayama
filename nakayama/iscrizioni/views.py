from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Iscrizione
import datetime
import logging
from . import utils


log = logging.getLogger()


def index(request):

    lista_iscritti = Iscrizione.objects.filter(
        anno_iscrizione=utils.get_current_year()
    ).all()
    context = {'lista_iscritti': lista_iscritti}
    return render(request, 'iscrizioni/index.html', context)


def dettaglio_iscritto(request, iscritto_id):

    iscritto = get_object_or_404(Iscrizione, pk=iscritto_id)
    return render(request, 'iscrizioni/dettaglio-iscritto.html', {'iscritto': iscritto})

