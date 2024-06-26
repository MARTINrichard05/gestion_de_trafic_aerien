# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.exceptions import ValidationError


class Aeroports(models.Model):
    nom = models.CharField(max_length=255)
    pays = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'aeroports'

    def __str__(self):
        return self.nom + " (" + self.pays + ")"



    def delete(self, *args, **kwargs):
        if self.vols_aeroport_depart_set.exists() or self.vols_aeroport_arrivee_set.exists():
            raise ValidationError("Cet aéroport est utilisé dans un ou plusieurs vols, il ne peut pas être supprimé.")
        super().delete(*args, **kwargs)


class Avions(models.Model):
    nom = models.CharField(max_length=255)
    compagnie = models.ForeignKey('Compagnies', models.DO_NOTHING)
    modele = models.ForeignKey('TypesAvions', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'avions'

    def __str__(self):
        return str(self.modele)+" "+str(self.nom)


class Compagnies(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    pays_rattachement = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'compagnies'

    def __str__(self):
        return self.nom


class Pistes(models.Model):
    numero = models.IntegerField()
    aeroport = models.ForeignKey(Aeroports, models.DO_NOTHING,null=True)
    longueur = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'pistes'

    def __str__(self):
        return str(self.aeroport) + " - Piste " + str(self.numero)


class TypesAvions(models.Model):
    marque = models.CharField(max_length=255)
    modele = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='type_avion_images/')
    longueur_piste_necessaire = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'types_avions'

    def __str__(self):
        return str(self.marque) + " " + self.modele

    def delete(self, *args, **kwargs):
        if self.marque == "Default" and self.modele == "Default":
            raise ValidationError("Ce type d'avion ne peut pas être supprimé.")

        if self.avions_set.exists():
            raise ValidationError("Ce type d'avion est utilisé par un ou plusieurs avions, il ne peut pas être supprimé.")
        super().delete(*args, **kwargs)


class Vols(models.Model):
    avion = models.ForeignKey(Avions, models.DO_NOTHING,null=True)
    pilote = models.CharField(max_length=255)
    aeroport_depart = models.ForeignKey(Aeroports, models.DO_NOTHING, null=True, related_name='vols_aeroport_depart_set')
    date_heure_depart = models.DateTimeField()
    aeroport_arrivee = models.ForeignKey(Aeroports, models.DO_NOTHING, null=True, related_name='vols_aeroport_arrivee_set')
    date_heure_arrivee = models.DateTimeField()
    piste_depart = models.IntegerField(blank=True, null=True)
    piste_arrivee = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'vols'

    def __str__(self):
        return str(self.avion) + " - " + str(self.aeroport_depart) + " ("+str(self.piste_depart)+") -> " + str(self.aeroport_arrivee)+ " ("+str(self.piste_arrivee)+")"
