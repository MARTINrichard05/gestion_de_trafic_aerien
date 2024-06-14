from django.shortcuts import render ,get_object_or_404, redirect
from .models import Aeroports, Avions, Compagnies, Pistes, TypesAvions, Vols
from .forms import AeroportsForm, AvionsForm, CompagniesForm, PistesForm, TypesAvionsForm, VolsForm, GeneratePdfForm, UploadCSVForm
import time
import datetime
from .matcher import find_best_match, findairports, findavionsmodels
from .flightarranger import arrange
import csv
from django.http import HttpResponse

from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import FileResponse

from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.pagesizes import letter, landscape


def vols_par_aeroport_et_periode_pdf(request):
    if request.method == 'POST':
        form = GeneratePdfForm(request.POST)
        if form.is_valid():
            aeroport = form.cleaned_data.get('aeroport')
            date_debut = form.cleaned_data.get('date_debut')
            date_fin = form.cleaned_data.get('date_fin')
            all_aeroports = form.cleaned_data.get('all_aeroports')

            # Créer un fichier PDF en mémoire
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

            if all_aeroports:
                # Récupérer tous les vols
                vols = Vols.objects.filter(date_heure_depart__range=[date_debut, date_fin])
            else:
                # Récupérer les vols pour l'aéroport sélectionné
                vols = Vols.objects.filter(
                    Q(aeroport_depart=aeroport) | Q(aeroport_arrivee=aeroport),
                    date_heure_depart__range=[date_debut, date_fin]
                )

            # Créer le tableau
            data = [['Avion', 'Type d\'avion', 'Date heure départ', 'Date heure arrivée', 'Aéroport et piste départ', 'Aéroport et piste arrivée']]
            for vol in vols:
                if vol.piste_arrivee is not None: # we have to get the name of the piste with the id vol.piste_arrivee
                    print(vol.piste_arrivee)
                    pistearrivee = Pistes.objects.get(id=vol.piste_arrivee).numero

                else:
                    pistearrivee = None
                if vol.piste_depart is not None:
                    print(vol.piste_depart)
                    pistedepart = Pistes.objects.get(id=vol.piste_depart).numero
                else:
                    pistedepart = None
                data.append([vol.avion.nom, vol.avion.modele, vol.date_heure_depart, vol.date_heure_arrivee, f"{vol.aeroport_depart.nom} - {pistedepart}", f"{vol.aeroport_arrivee.nom} - {pistearrivee}"])

            table = Table(data)

            # Ajouter le tableau au PDF
            elements = []
            elements.append(table)
            doc.build(elements)

            # Créer une réponse avec le PDF
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename='vols.pdf')
    else:
        form = GeneratePdfForm()

    return render(request, 'aeromanager/index.html', {'form': form})



def index(request):
    aeroports = Aeroports.objects.all()
    avions = Avions.objects.all()
    compagnies = Compagnies.objects.exclude(nom="Default")
    pistes = Pistes.objects.all()
    types_avions = TypesAvions.objects.exclude(modele="Default")
    vols = Vols.objects.all() # on récupère tout les vols

    arrange() # on associe vols/pistes



    context = {
        'aeroports': aeroports,
        'avions': avions,
        'compagnies': compagnies,
        'pistes': pistes,
        'types_avions': types_avions,
        'vols': vols,
    } # on renvoie tout les objets à la page index

    return render(request, 'aeromanager/index.html', context)

def aeroport_detail(request, id):
    aeroport = Aeroports.objects.get(id=id)
    pistes = Pistes.objects.filter(aeroport=id)
    context = {
        'aeroport': aeroport,
        'pistes': pistes,
    }
    return render(request, 'aeroport/aeroport_detail.html', context)

def avion_detail(request, id):
    avion = get_object_or_404(Avions, id=id)
    type_avions = get_object_or_404(TypesAvions, id=avion.modele.id)
    context = {
        'avion': avion,
        'type_avion': type_avions,
    }
    return render(request, 'avion/avion_detail.html', context)

def compagnie_detail(request, id):
    compagnie = Compagnies.objects.get(id=id)
    context = {
        'compagnie': compagnie,
    }
    return render(request, 'companie/compagnie_detail.html', context)

def piste_detail(request, id):
    piste = Pistes.objects.get(id=id)
    context = {
        'piste': piste,
    }
    return render(request, 'piste/piste_detail.html', context)

def type_avion_detail(request, id):
    type_avion = TypesAvions.objects.get(id=id)
    context = {
        'type_avion': type_avion,
    }
    return render(request, 'type_avion/type_avion_detail.html', context)

def vol_detail(request, id):
    vol = get_object_or_404(Vols, id=id)
    return render(request, 'vol/detail_vol.html', {'vol': vol})

def add_aeroport(request):
    if request.method == 'POST':
        form = AeroportsForm(request.POST)
        if form.is_valid(): # si tout est bon, on sauvegarde
            aeroport = form.save()
            return redirect('aeroport_detail', id=aeroport.id)
    else: # sinon on renvoie le formulaire
        form = AeroportsForm()
    return render(request, 'aeroport/add_aeroport.html', {'form': form})

def add_avion(request):
    if request.method == 'POST':
        form = AvionsForm(request.POST)
        if form.is_valid():
            avion = form.save()
            return redirect('avion_detail', id=avion.id)
    else:
        form = AvionsForm()
    return render(request, 'avion/add_avion.html', {'form': form})

def add_compagnie(request):
    if request.method == 'POST':
        form = CompagniesForm(request.POST)
        if form.is_valid():
            compagnie = form.save()
            return redirect('compagnie_detail', id=compagnie.id)
    else:
        form = CompagniesForm()
    return render(request, 'companie/add_compagnie.html', {'form': form})

def add_piste(request):
    if request.method == 'POST':
        form = PistesForm(request.POST)
        if form.is_valid():
            piste = form.save()
            arrange()
            return redirect('piste_detail', id=piste.id)
    else:
        form = PistesForm()
    return render(request, 'piste/add_piste.html', {'form': form})

def add_type_avion(request):
    if request.method == 'POST':
        form = TypesAvionsForm(request.POST)
        if form.is_valid():
            type_avion = form.save()
            arrange()
            return redirect('type_avion_detail', id=type_avion.id)
    else:
        form = TypesAvionsForm()
    return render(request, 'type_avion/add_type_avion.html', {'form': form})

def add_vol(request):
    if request.method == 'POST':
        form = VolsForm(request.POST)
        if form.is_valid():
            vol = form.save()
            arrange()
            return redirect('vol_detail', id=vol.id)
    else:
        form = VolsForm()
    return render(request, 'vol/add_vol.html', {'form': form})

def edit_aeroport(request, id):
    aeroport = Aeroports.objects.get(id=id)
    if request.method == 'POST':
        form = AeroportsForm(request.POST, instance=aeroport)
        if form.is_valid():
            aeroport = form.save()
            return redirect('aeroport_detail', id=aeroport.id)
    else:
        form = AeroportsForm(instance=aeroport)
    return render(request, 'aeroport/edit_aeroport.html', {'form': form})

def edit_avion(request, id):
    avion = Avions.objects.get(id=id)
    if request.method == 'POST':
        form = AvionsForm(request.POST, instance=avion)
        if form.is_valid():
            avion = form.save()
            return redirect('avion_detail', id=avion.id)
    else:
        form = AvionsForm(instance=avion)
    return render(request, 'avion/edit_avion.html', {'form': form})

def edit_compagnie(request, id):
    compagnie = Compagnies.objects.get(id=id)
    if request.method == 'POST':
        form = CompagniesForm(request.POST, instance=compagnie)
        if form.is_valid():
            compagnie = form.save()
            return redirect('compagnie_detail', id=compagnie.id)
    else:
        form = CompagniesForm(instance=compagnie)
    return render(request, 'companie/edit_compagnie.html', {'form': form})

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
    return render(request, 'piste/edit_piste.html', {'form': form})

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
    return render(request, 'type_avion/edit_type_avion.html', {'form': form})

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
    return render(request, 'vol/edit_vol.html', {'form': form})

def delete_aeroport(request, id):
    # on doit dabord supprimer les pistes
    pistes = Pistes.objects.filter(aeroport=id)
    for piste in pistes:
        piste.delete()

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
            csv_file = request.FILES['csv_file'] # on récupère le fichier csv
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file) # on le lit
            # next(reader)  # Skip the header row
            for row in reader:
                # Extraire les données du vol
                compagnie_default, _ = Compagnies.objects.get_or_create(nom="Default")
                modele_default, _ = TypesAvions.objects.get_or_create(marque="Default", modele="Default")
                avion= row[0]
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



                type_avionsdispo = TypesAvions.objects.all()
                type_avionsdisponames = []

                for type_avion in type_avionsdispo:
                    type_avionsdisponames.append(type_avion.modele)

                avionsfind = findavionsmodels(avion,type_avionsdisponames)

                if avionsfind[1] < 10: # on utilise le modèle Default si le score est trop bas
                    type_avion = "Default"
                else:
                    type_avion = avionsfind[0]


                # Dans tout les cas on crée un avion, sauf si il existe déjà
                avionsdispo = Avions.objects.all()
                avionsdisponames = []
                for avion in avionsdispo:
                    avionsdisponames.append(avion.nom)
                found = False
                for avione in avionsdisponames:
                    if avione == avion:
                        avion = Avions.objects.get(nom=avione)
                        found = True
                        break
                if not found:
                    avion = Avions.objects.create(nom=avion, modele=TypesAvions.objects.get(modele=type_avion), compagnie=compagnie_default)









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
            return redirect('index')
    else:
        form = UploadCSVForm()
    return render(request, 'aeromanager/upload_csv.html', {'form': form})
