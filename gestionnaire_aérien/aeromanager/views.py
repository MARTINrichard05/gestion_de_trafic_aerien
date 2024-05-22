from django.shortcuts import render
from .models import Aeroports, Avions, Compagnies, Pistes, TypesAvions, Vols

def index(request):
    aeroports = Aeroports.objects.all()
    avions = Avions.objects.all()
    compagnies = Compagnies.objects.all()
    pistes = Pistes.objects.all()
    types_avions = TypesAvions.objects.all()
    vols = Vols.objects.all()

    context = {
        'aeroports': aeroports,
        'avions': avions,
        'compagnies': compagnies,
        'pistes': pistes,
        'types_avions': types_avions,
        'vols': vols,
    }

    return render(request, 'index.html', context)

def aeroport_detail(request, id):
    aeroport = Aeroports.objects.get(id=id)
    context = {
        'aeroport': aeroport,
    }
    return render(request, 'aeroport_detail.html', context)

def avion_detail(request, id):
    avion = Avions.objects.get(id=id)
    context = {
        'avion': avion,
    }
    return render(request, 'avion_detail.html', context)

def compagnie_detail(request, id):
    compagnie = Compagnies.objects.get(id=id)
    context = {
        'compagnie': compagnie,
    }
    return render(request, 'compagnie_detail.html', context)

def piste_detail(request, id):
    piste = Pistes.objects.get(id=id)
    context = {
        'piste': piste,
    }
    return render(request, 'piste_detail.html', context)

def type_avion_detail(request, id):
    type_avion = TypesAvions.objects.get(id=id)
    context = {
        'type_avion': type_avion,
    }
    return render(request, 'type_avion_detail.html', context)
