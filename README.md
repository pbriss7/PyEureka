# PyReka

## Description
Le programme permet d'interroger l'API de Cision-Eurêka et d'acquérir les métadonnées et textes complets de 22 journaux québécois. L'accès à cet API fait partie d'une entente signée entre l'Université McGill et Cision. Un identifiant unique et un mot de passe sont requis pour soumettre des requêtes. Ces informations personnelles permettent l'émission d'un "token" à durée limitée (renouvelable).

Le programme est interactif. Une fois lancé avec un interpréteur Python, il pose à l'utilisateur les questions qui conduiront au lancement d'une requête GET. Les résultats sont transposés dans un tableau de données (DataFrame), puis écrits dans un fichier `document.csv` qui est déposé dans le même répertoire du programme.

## Installation des modules et lancement du programme
Pour installer les modules qui ne le sont pas, exécutez la ligne suivante dans le Terminal (ajustez la commande pip selon la version Python utilisée. Le programme a été créé avec Python 3.11):

`pip3.11 install -r requirements.txt`

Pour lancer le programme, on exécute le fichier documentFetcher.py. Par exemple, dans le Terminal:

`python3.11 documentFetcher.py`

## Documentation Eurêka
Le répertoire contient deux fichiers .pdf fournissant des informations sur les clés à utiliser dans la requête de recherche.

Pour toute question: Pascal Brissette (pascal.brissette@mcgill.ca)
