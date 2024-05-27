from django import forms
from .models import Aeroports , Avions , Compagnies , Pistes , TypesAvions, Vols

class AeroportsForm(forms.ModelForm):
    class Meta:
        model = Aeroports
        fields = ['nom', 'pays']

class VolsForm(forms.ModelForm):
    class Meta:
        model = Vols
        fields = ['avion', 'pilote', 'aeroport_depart', 'date_heure_depart', 'aeroport_arrivee']

class AvionsForm(forms.ModelForm):
    class Meta:
        model = Avions
        fields = ['nom', 'modele', 'compagnie']

class CompagniesForm(forms.ModelForm):
    class Meta:
        model = Compagnies
        fields = ['nom', 'pays_rattachement']

class PistesForm(forms.ModelForm):
    class Meta:
        model = Pistes
        fields = ['numero', 'aeroport', 'longueur']

class TypesAvionsForm(forms.ModelForm):
    class Meta:
        model = TypesAvions
        fields = ['marque', 'modele', 'description', 'longueur_piste_necessaire', 'image']
