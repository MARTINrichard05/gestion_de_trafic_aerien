from django import forms
from .models import Aeroports , Avions , Compagnies , Pistes , TypesAvions, Vols

class GeneratePdfForm(forms.Form):
    aeroport = forms.ModelChoiceField(queryset=Aeroports.objects.all(), required=False)
    date_debut = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_fin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    all_aeroports = forms.BooleanField(required=False)
class AeroportsForm(forms.ModelForm):
    class Meta:
        model = Aeroports
        fields = ['nom', 'pays']

class UploadCSVForm(forms.Form):
    csv_file = forms.FileField()

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
        fields = ['nom','description', 'pays_rattachement']

class PistesForm(forms.ModelForm):
    class Meta:
        model = Pistes
        fields = ['numero', 'aeroport', 'longueur']

class TypesAvionsForm(forms.ModelForm):
    class Meta:
        model = TypesAvions
        fields = ['marque', 'modele', 'description', 'longueur_piste_necessaire', 'image']
