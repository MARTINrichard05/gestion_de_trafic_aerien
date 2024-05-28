from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("aeroport_detail/<int:id>", views.aeroport_detail, name="aeroport_detail"),
    path("avion_detail/<int:id>", views.avion_detail, name="avion_detail"),
    path("compagnie_detail/<int:id>", views.compagnie_detail, name="compagnie_detail"),
    path("piste_detail/<int:id>", views.piste_detail, name="piste_detail"),
    path("type_avion/<int:id>", views.type_avion_detail, name="type_avion_detail"),
    path("vol_detail/<int:id>", views.vol_detail, name="vol_detail"),

    path('add_aeroport/', views.add_aeroport, name='add_aeroport'),
    path('add_avion/', views.add_avion, name='add_avion'),
    path('add_compagnie/', views.add_compagnie, name='add_compagnie'),
    path('add_piste/', views.add_piste, name='add_piste'),
    path('add_type_avion/', views.add_type_avion, name='add_type_avion'),
    path('add_vol/', views.add_vol, name='add_vol'),

    path('edit_aeroport/<int:id>', views.edit_aeroport, name='edit_aeroport'),
    path('edit_avion/<int:id>', views.edit_avion, name='edit_avion'),
    path('edit_compagnie/<int:id>', views.edit_compagnie, name='edit_compagnie'),
    path('edit_piste/<int:id>', views.edit_piste, name='edit_piste'),
    path('edit_type_avion/<int:id>', views.edit_type_avion, name='edit_type_avion'),
    path('edit_vol/<int:id>', views.edit_vol, name='edit_vol'),

    path('delete_aeroport/<int:id>', views.delete_aeroport, name='delete_aeroport'),
    path('delete_avion/<int:id>', views.delete_avion, name='delete_avion'),
    path('delete_compagnie/<int:id>', views.delete_compagnie, name='delete_compagnie'),
    path('delete_piste/<int:id>', views.delete_piste, name='delete_piste'),
    path('delete_type_avion/<int:id>', views.delete_type_avion, name='delete_type_avion'),
    path('delete_vol/<int:id>', views.delete_vol, name='delete_vol'),

    #static("type_avion_images", document_root=settings.MEDIA_ROOT)
]