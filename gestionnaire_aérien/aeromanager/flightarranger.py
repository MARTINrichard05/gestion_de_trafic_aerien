from .models import Aeroports, Avions, Compagnies, Pistes, TypesAvions, Vols
import datetime

def arrange():
    # Get all the flights
    vols = Vols.objects.all()
    # Get all the pistes
    pistes = Pistes.objects.all()

    total_pistes = {} # {piste_id: [[begin, end], [begin, end] ...]}

    # Get all the pistes
    for piste in pistes:
        total_pistes[piste.id] = []

    # assingn the flights to the pistes, by taking in count the min length of the piste

    for vol in vols:
        min_lenght = vol.avion.modele.longueur_piste_necessaire
        up_time = vol.date_heure_depart
        down_time = vol.date_heure_arrivee
        piste_up_id = None
        for piste in pistes:
            if piste_up_id is None:
                if piste.aeroport == vol.aeroport_depart and piste.longueur >= min_lenght:
                    if total_pistes[piste.id] == []:
                        piste_up_id = piste.id
                        total_pistes[piste.id].append([up_time, up_time + datetime.timedelta(minutes=10)])
                    else: # we check if the piste is free during the time we need it
                        for piste_time in total_pistes[piste.id]:
                            if not piste_time[0] <= up_time < piste_time[1]:
                                if not piste_time[0] <= up_time + datetime.timedelta(minutes=10) < piste_time[1]:
                                    piste_up_id = piste.id
                                    total_pistes[piste.id].append([up_time, up_time + datetime.timedelta(minutes=10)])
                                    break
            else:
                break
        piste_down_id = None
        for piste in pistes:
            if piste_down_id is None:
                if piste.aeroport == vol.aeroport_arrivee and piste.longueur >= min_lenght:
                    if total_pistes[piste.id] == []:
                        piste_down_id = piste.id
                        total_pistes[piste.id].append([down_time, down_time + datetime.timedelta(minutes=10)])
                    else:
                        for piste_time in total_pistes[piste.id]:
                            if not piste_time[0] <= down_time < piste_time[1]:
                                if not piste_time[0] <= down_time + datetime.timedelta(minutes=10) < piste_time[1]:
                                    piste_down_id = piste.id
                                    total_pistes[piste.id].append([down_time, down_time + datetime.timedelta(minutes=10)])
                                    break
            else:
                break
        vol.piste_depart = piste_up_id
        vol.piste_arrivee = piste_down_id
        vol.save()








