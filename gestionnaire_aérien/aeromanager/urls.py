from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("aeroport_detail/<int:id>", views.aeroport_detail, name="aeroport_detail"),
    path("avion_detail/<int:id>", views.avion_detail, name="avion_detail"),
    path("compagnie_detail/<int:id>", views.compagnie_detail, name="compagnie_detail"),
    path("piste_detail/<int:id>", views.piste_detail, name="piste_detail"),
    path("type_avion_detail/<int:id>", views.type_avion_detail, name="type_avion_detail"),
]