# Comment Cela Fonctionne
## Globalement
### Résumé
Le gestionnaire aérien est un site web dynamique qui utilise des "CRUD" (Create, Read, Update, Delete) pour gérer les vols, les avions, les aéroports et les compagnies aériennes.   
Il est possible de créer, lire, mettre à jour et supprimer des éléments de ces catégories.   
Les vols sont les éléments principaux, car ils sont composés d'un avion, d'un aéroport de départ, d'un aéroport d'arrivée, d'une compagnie aérienne et d'une date de départ, de même pour l'arrivée.   
Les autres éléments sont des dépendances des vols.

## Structure
Le projet django s'apelle `gestionnaire_aérien`, dans le dossier de ce nom, se trouve deux fichiers principaux: `urls.py` et `settings.py`.