# Comment Cela Fonctionne
## Globalement
### Résumé
Le gestionnaire aérien est un site web dynamique qui utilise des "CRUD" (Create, Read, Update, Delete) pour gérer les vols, les avions, les aéroports et les compagnies aériennes.   

Il est possible de créer, lire, mettre à jour et supprimer des éléments de ces catégories.   

Les vols sont les éléments principaux, car ils sont composés d'un avion, d'un aéroport de départ, d'un aéroport d'arrivée, d'une compagnie aérienne et d'une date de départ, de même pour l'arrivée.   
Les autres éléments sont des dépendances des vols.

## Structure
Le projet django s'apelle `gestionnaire_aérien`, dans le dossier de ce nom, se trouve deux fichiers principaux: `urls.py` et `settings.py`.   

L'app s'apelle `aeromanager`, dans le dossier de ce nom se trouvent les fichiers `urls.py`, `models.py`, `views.py`, `forms.py` et bien d'autres, ce sont cependant les fichiers les plus intéressants.   

### `models.py`
Ce fichier contient les classes qui définissent les objets de la base de données.

La plupart on une methode `__str__` qui permet de les afficher plus facilement dans l'interface d'administration.   

Certaines on aussi une methode `delete` qui permet de supprimer les objets de la base de données en faisant les verification nécessaires avant pour éviter des soucis.   

Pour les vols, piste_depart et piste_arrive sont des integerfields qui contiennent l'id de la piste, je n'ai pas utilisé de foreignkey pour gagner en "souplesse" de gestion.
