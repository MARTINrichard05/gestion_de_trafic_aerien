from django.shortcuts import render ,get_object_or_404, redirect
from .models import Aeroports, Avions, Compagnies, Pistes, TypesAvions, Vols
from .forms import AeroportsForm, AvionsForm, CompagniesForm, PistesForm, TypesAvionsForm, VolsForm
from .forms import UploadCSVForm
import time
import datetime
from .matcher import find_best_match, findairports
from .flightarranger import arrange
import csv
from django.http import HttpResponse






def coordinerpiste_vols(pistes, vols):
    pass

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
    avion = get_object_or_404(Avions, id=id)
    type_avions = get_object_or_404(TypesAvions, id=avion.modele.id)
    context = {
        'avion': avion,
        'type_avion': type_avions,
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

def vol_detail(request, id):
    vol = get_object_or_404(Vols, id=id)
    return render(request, 'detail_vol.html', {'vol': vol})

def add_aeroport(request):
    if request.method == 'POST':
        form = AeroportsForm(request.POST)
        if form.is_valid():
            aeroport = form.save()
            return redirect('aeroport_detail', id=aeroport.id)
    else:
        form = AeroportsForm()
    return render(request, 'add_aeroport.html', {'form': form})

def add_avion(request):
    if request.method == 'POST':
        form = AvionsForm(request.POST)
        if form.is_valid():
            avion = form.save()
            return redirect('avion_detail', id=avion.id)
    else:
        form = AvionsForm()
    return render(request, 'add_avion.html', {'form': form})

def add_compagnie(request):
    if request.method == 'POST':
        form = CompagniesForm(request.POST)
        if form.is_valid():
            compagnie = form.save()
            return redirect('compagnie_detail', id=compagnie.id)
    else:
        form = CompagniesForm()
    return render(request, 'add_compagnie.html', {'form': form})

def add_piste(request):
    if request.method == 'POST':
        form = PistesForm(request.POST)
        if form.is_valid():
            piste = form.save()
            arrange()
            return redirect('piste_detail', id=piste.id)
    else:
        form = PistesForm()
    return render(request, 'add_piste.html', {'form': form})

def add_type_avion(request):
    if request.method == 'POST':
        form = TypesAvionsForm(request.POST)
        if form.is_valid():
            type_avion = form.save()
            arrange()
            return redirect('type_avion_detail', id=type_avion.id)
    else:
        form = TypesAvionsForm()
    return render(request, 'add_type_avion.html', {'form': form})

def add_vol(request):
    if request.method == 'POST':
        form = VolsForm(request.POST)
        if form.is_valid():
            vol = form.save()
            arrange()
            return redirect('vol_detail', id=vol.id)
    else:
        form = VolsForm()
    return render(request, 'add_vol.html', {'form': form})

def edit_aeroport(request, id):
    aeroport = Aeroports.objects.get(id=id)
    if request.method == 'POST':
        form = AeroportsForm(request.POST, instance=aeroport)
        if form.is_valid():
            aeroport = form.save()
            return redirect('aeroport_detail', id=aeroport.id)
    else:
        form = AeroportsForm(instance=aeroport)
    return render(request, 'edit_aeroport.html', {'form': form})

def edit_avion(request, id):
    avion = Avions.objects.get(id=id)
    if request.method == 'POST':
        form = AvionsForm(request.POST, instance=avion)
        if form.is_valid():
            avion = form.save()
            return redirect('avion_detail', id=avion.id)
    else:
        form = AvionsForm(instance=avion)
    return render(request, 'edit_avion.html', {'form': form})

def edit_compagnie(request, id):
    compagnie = Compagnies.objects.get(id=id)
    if request.method == 'POST':
        form = CompagniesForm(request.POST, instance=compagnie)
        if form.is_valid():
            compagnie = form.save()
            return redirect('compagnie_detail', id=compagnie.id)
    else:
        form = CompagniesForm(instance=compagnie)
    return render(request, 'edit_compagnie.html', {'form': form})

def edit_piste(request, id):
    piste = Pistes.objects.get(id=id)
    if request.method == 'POST':
        form = PistesForm(request.POST, instance=piste)
        if form.is_valid():
            piste = form.save()
            arrange()
            return redirect('piste_detail', id=piste.id)
    else:
        form = PistesForm(instance=piste)
    return render(request, 'edit_piste.html', {'form': form})

def edit_type_avion(request, id):
    type_avion = TypesAvions.objects.get(id=id)
    if request.method == 'POST':
        form = TypesAvionsForm(request.POST, request.FILES, instance=type_avion)
        if form.is_valid():
            type_avion = form.save()
            arrange()
            return redirect('type_avion_detail', id=type_avion.id)
    else:
        form = TypesAvionsForm(instance=type_avion)
    return render(request, 'edit_type_avion.html', {'form': form})

def edit_vol(request, id):
    vol = Vols.objects.get(id=id)
    if request.method == 'POST':
        form = VolsForm(request.POST, instance=vol)
        if form.is_valid():
            vol = form.save()
            arrange()
            return redirect('vol_detail', id=vol.id)
    else:
        form = VolsForm(instance=vol)
    return render(request, 'edit_vol.html', {'form': form})

def delete_aeroport(request, id):
    aeroport = Aeroports.objects.get(id=id)
    aeroport.delete()
    return redirect('index')

def delete_avion(request, id):
    avion = Avions.objects.get(id=id)
    avion.delete()
    return redirect('index')

def delete_compagnie(request, id):
    compagnie = Compagnies.objects.get(id=id)
    compagnie.delete()
    return redirect('index')

def delete_piste(request, id):
    piste = Pistes.objects.get(id=id)
    piste.delete()
    arrange()
    return redirect('index')

def delete_type_avion(request, id):
    type_avion = TypesAvions.objects.get(id=id)
    type_avion.delete()
    arrange()
    return redirect('index')

def delete_vol(request, id):
    vol = Vols.objects.get(id=id)
    vol.delete()
    arrange()
    return redirect('index')

def upload_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            next(reader)  # Skip the header row
            for row in reader:
                # Extraire les données du vol
                compagnie_default, _ = Compagnies.objects.get_or_create(nom="Default")
                modele_default, _ = TypesAvions.objects.get_or_create(marque="Default", modele="Default")
                avion, created = Avions.objects.get_or_create(
                    nom=row[0],
                    defaults={'compagnie': compagnie_default, 'modele': modele_default}
                )
                pilote = row[1]
                aeroport_depart = row[2]
                date_heure_depart = row[3]
                aeroport_arrivee = row[4]
                date_heure_arrivee = row[5]



                aeroportsdispo = Aeroports.objects.all()
                aeroportsdisponames= []
                for aeroport in aeroportsdispo:
                    aeroportsdisponames.append(aeroport.nom)

                aeroportsfind = findairports(aeroport_depart,aeroport_arrivee,aeroportsdisponames)

                if aeroportsfind[0][1] < 10: # on crée l'aeroport si le score est trop bas
                    Aeroports.objects.create(nom=aeroport_depart, pays="Default")
                if aeroportsfind[1][1] < 10:
                    Aeroports.objects.create(nom=aeroport_arrivee, pays="Default")

                aeroport_depart = Aeroports.objects.get(nom=aeroportsfind[0][0])
                aeroport_arrivee = Aeroports.objects.get(nom=aeroportsfind[1][0])



                # Ajouter le vol à la base de données
                Vols.objects.create(
                    avion=avion,
                    pilote=pilote,
                    aeroport_depart=aeroport_depart,
                    date_heure_depart=date_heure_depart,
                    aeroport_arrivee=aeroport_arrivee,
                    date_heure_arrivee=date_heure_arrivee,
                )
            arrange()
            return render(request, 'index.html')
    else:
        form = UploadCSVForm()
    return render(request, 'upload_csv.html', {'form': form})
