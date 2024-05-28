from django import forms
from .models import Aeroports , Avions , Compagnies , Pistes , TypesAvions, Vols

class AeroportsForm(forms.ModelForm):
    class Meta:
        model = Aeroports
        fields = ['nom', 'pays']

class VolsForm(forms.ModelForm):
    class Meta:
        model = Vols
        fields = ['avion', 'pilote', 'aeroport_depart', 'date_heure_depart', 'aeroport_arrivee', 'date_heure_arrivee']
        widgets = {
            'date_heure_depart': forms.DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM:SS'}),
            'date_heure_arrivee': forms.DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM:SS'}),
        }

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
