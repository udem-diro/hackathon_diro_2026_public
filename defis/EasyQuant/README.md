# Docker & Jupyter Notebook – Guide d’installation

---

## Installation

Ce README explique comment installer Docker sur macOS et Windows, puis comment configurer un environnement Python pour travailler avec des notebooks Jupyter (.ipynb) et les dépendances nécessaires au projet.

La partie ci-dessous devrait avoir ete fait d'avance, 

### macOS

Prérequis :
- macOS 10.15 ou plus récent
- Processeur Intel ou Apple Silicon

### Docker

Étapes :

1. Télécharger Docker Desktop : [Docker link](https://www.docker.com/products/docker-desktop/)
2. Ouvrir le fichier .dmg
3. Glisser Docker.app dans le dossier Applications
4. Lancer Docker et accepter les permissions

Vérification :

- `docker --version`

> Si cela ne fonctionne pas des instructions plus bas sont fournies apres la section Windows

---

### Windows

Prérequis :
- Windows 10 ou 11 (64 bits)
- WSL 2 recommandé

Étapes :

1. Télécharger Docker Desktop : [Docker link](https://www.docker.com/products/docker-desktop/)
2. Lancer l’installateur
3. Activer l’option "Use WSL 2 instead of Hyper-V" si proposée
4. Redémarrer si nécessaire
5. Lancer Docker Desktop

Vérification :

- `docker --version`

> La partie Docker est pour le défi 4 donc vous pourriez si vous voulez ne pas faire cela
> maintenant et le faire plus tard

Pour macOS , si vous voyez que l'application Docker Desktop n'arrive pas à ouvrir , installez:

`brew install colima docker`

Puis:

`colima start`

---

## Installation de Python et Jupyter Notebook

Python 3.8 ou supérieur est requis.

Vérifier l’installation :

- `python --version`
- `pip --version`


---

### Création d’un environnement virtuel (recommandé)

> L'environnement n'est pas necessaire , si cela marche du premier coup tant mieux
> Sinon installer les packages de maniere global comme dans la section "Installation des dependances"

Créer l’environnement virtuel avec uv:

- `pip install uv`


Créer l’environnement dans le répertoire où vous allez travailler:

- macOS / Linux / Windows:
    - `uv init`

Activier l'environnement pour Windows:

- Windows :
    - `.venv\Scripts\activate`

- macOS / Linux
    - La commande sera afficher.

---

### Installation des dépendances Python

Installer les packages nécessaires :

`pip install numpy pandas ipykernel`

ou utilisez le fichier requirements.txt qui avec la prochaine commande vont installer les packages nécessaires:

`pip install -r requirements.txt`
 
Si vous utilisez uv:

`uv pip install -r requirements.txt`

Certains modules suivants sont inclus par défaut avec Python :

1. random
2. string
3. datetime

Des modules où des librairies dans Python sont des bases de codes que les programmeurs peuvent réutiliser
de la même manière que Personne A pourrait créer `func_A()` et ensuite envoyer sa fonction a Personne B et celui-ci pourrait l'appeler dans son code.

---

### Vérification finale

Dans un notebook Jupyter (.ipynb), exécuter :

```python
import numpy as np
import pandas as pd
import datetime
```

> Si cela ne fonctionne pas pour vous , essayer de résoudre le problème mais si après 2 tentative et chatgpt, contactez la personne du défi pour de l'assistance !! 

---

### Conclusion

L’environnement est maintenant prêt pour :
- Utiliser Docker
- Travailler avec des notebooks Jupyter
- Manipuler des données avec NumPy et Pandas


## Digo Company - Défis d'Analyse Financière 🧱

### Mise en contexte
Bienvenue chez Digo Company, une entreprise innovante spécialisée dans la fabrication de jouets de construction pour enfants, similaire aux célèbres blocs LEGO. Dans un marché compétitif et en constante évolution, Digo doit gérer efficacement ses investissements financiers et son inventaire pour assurer sa croissance et sa stabilité.

Vous êtes nouvellement engagés en tant que Quants Developers au sein de l'équipe d'analyse financière de Digo Company. Votre mission consiste à développer des outils et des analyses sophistiqués pour évaluer la performance des investissements de l'entreprise, identifier les risques potentiels et optimiser la gestion du portefeuille financier.
Les défis ci-dessous représentent des problématiques réelles auxquelles l'équipe finance fait face quotidiennement. Votre expertise technique et votre capacité à traduire des besoins d'affaires en solutions concrètes seront essentielles pour aider Digo Company à prendre des décisions éclairées.

### Terminologie

Certains termes introduit dans les problemes sont peut-être inconnues pour certaines personnes donc Digo Company vous donne une liste de mot-clès qui pourrait aider a la compréhension
pour pouvoir vous aider dans certains concepts de la finance.


- Position:
    - Une position est le montant investi dans une compagnie ou un actif financier. Ex: (100 dollars investi dans LEGO Inc => une position de 100 dollars dans LEGO Inc)

- Portefeuille:
    - Ensemble des positions détenu par un agent ou une compagnie.
    - Exemple:
        - 67 et Compagnie détient un portefeuille des actions suivantes:
            1. AirFlow -> 100M dollars
            2. DonutTime -> 20M dollars
            3. BobetteLegend -> 500K dollars
            4. ...

- Gain:
    - Montant obtenu en vendant une partie ou la totalité d'une position pour un actif dans le portefeuille
    - Exemple: 67 et Compagnie vendent 30% de leur position dans AirFlow => 30M dollars de gain

- Identifier:
    - Identifiant unique pour répresenter les compagnies et instruments financiers dans le monde de la finance , ces identifiants peuvent avoir plusieurs formes.


> Tips and tricks: La compagnie vous conseille fortement de visualiser les données pour voir a quoi ressemble vos données , quel format chaque colonnes de
> votre dataset aurait , cela peut être utile pour établier des liens et comprendre quoi faire dans les défis !!

#### Liens utiles pour les défis

- [Pandas](https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html)
- [Numpy](https://numpy.org/doc/stable/user/absolute_beginners.html)
- [Defi 2](https://medium.com/@devendra631995/rolling-window-27036cdc7b91)

## Défi 1 : Optimisation des Positions sur la Fin de Semaine
Objectif ==> 
- Digo Company souhaite maximiser ses gains durant la fin de semaine en identifiant les meilleures positions possibles avec des prédictions 100% précises.

#### Tâches à accomplir

Calculer la somme de toutes les meilleures positions pour les périodes suivantes :

1. Fin de semaine complète (samedi + dimanche)
2. Samedi uniquement
3. Dimanche uniquement
4. Samedi avant 12h
5. Samedi après 12h

- Livrable attendu
    - Un rapport détaillé présentant les positions optimales pour chaque période et leur valeur totale cumulée.

## Défi 2 : Détection des Positions de Fin de Journees(EndOfDay) Abnormales

Objectif => 

- Identifier les positions qui ont significativement chuté par rapport à leur moyenne mobile sur 10 jours et qui nécessitent une action de vente.

#### Contexte technique:

- Analyse sur le dernier mois de données
- Calcul d'une moyenne mobile sur 10 jours pour chaque position
- Définition d'un threshold (seuil) acceptable, avec une fourchette négative et positive
- Toutes positions descendant en dessous ou au dessus du threshold doivent être identifiées
>Threshold: 10% de la position.

#### Livrable attendu
- Une liste des positions à vendre qui ont dépassées la fourchette.

## Défi 3 : Calcul de la VaR (Value at Risk)

Objectif => 
- Calculer la VaR Live pour évaluer le risque et la volatilité des actifs du portefeuille de Digo Company. Les investisseurs préfèrent des actifs avec une VaR basse, indiquant une faible volatilité.

#### Méthodologie

Le calcul de la VaR suit un processus en plusieurs étapes :

1. Génération des simulations : Une matrice de simulations est générée la veille de la journée courante
2. Fusion avec les données d'assurance : Combiner les simulations avec un fichier fourni par l'équipe assurance contenant les informations financières des positions
3. Extraction du notionnel : Récupérer la valeur notionnel_devise_origine (valeur du notionnel dans n'importe quelle devise)
4. Matching des positions : Associer les simulations aux positions via leurs clés
5. Transformation : Convertir les noms de positions en security_identifier (identifiant des positions dans le portefeuille)
>Voir annexe A pour Transformation
6. Calcul du facteur : Diviser la valeur de la position dans le portefeuille par le notionnel
7. Ajustement d'inflation : Multiplier le facteur obtenu par un indice d'inflation
8. Application aux simulations : Multiplier ce résultat par chaque simulation du security_identifier
9. Agrégation : Sommer toutes les simulations => Exemple( Sommer simulation 1 : resultat 1 , Sommer simulation 2: resultat 2 ....)
10. Calcul final : Identifier la 3e déviation standard de la distribution pour obtenir la VaR Live

#### Livrable attendu

- Implémentation complète du calcul de VaR
- Documentation du processus
- Rapport présentant les VaR calculées pour chaque actif du portefeuille

- Annexe A:
    Dictionnaire de transformation
     ```python
    symbols = {
    "11_215" : "AX",
    "11_125" : "BZ",
    "11_370" : "CQ",
    "OSR3": "DW",
    "0SM": "EV",
    "MM3": "FP",
    "MMA": "GU",
    "ZIN": "HT",
    "A1E": "JR",
    "B3C": "KL",
    "6Z7": "ZY"
    }
    months = {
    "JAN" : "QX",
    "FEB" : "AZ",
    "MAR" : "LK",
    "APR" : "MP",
    "MAY" : "DR",
    "JUN" : "TY",
    "JUL" : "GV",
    "AUG" : "HN",
    "SEP" : "BF",
    "OCT" : "JC",
    "NOV" : "WU",
    "DEC" : "SE"
    }
    ```

## Défi 4 : Tableaux de Bord Analytiques avec Apache Superset

Objectif => 
- Créer des dashboards interactifs et visuellement attrayants dans Apache Superset pour visualiser et analyser les données financières de Digo Company.
Tâches à accomplir

- Suivre le quickstart guide: [Procedure](https://superset.apache.org/docs/quickstart)

- Importer les fichiers CSV contenant les données financières dans Superset
- Concevoir des visualisations pertinentes (graphiques, tableaux, indicateurs clés)
- Créer des tableaux de bord cohérents permettant une analyse rapide et efficace
>Assurer que les dashboards répondent aux besoins des différents intervenants (direction, équipe finance, analystes)

#### Livrable attendu

- Des dashboards fonctionnels dans Apache Superset
- Documentation expliquant la structure des dashboards et comment les interpréter
- Captures d'écran ou export des visualisations créées


## Instructions générales
Pour chaque défi, vous devez :

1. Documenter votre code de manière claire et professionnelle
2. Expliquer vos choix techniques et méthodologiques

Des questions vous seront poser a travers la fin de semaine sur les defis pour tester votre comprehension du probleme mais aussi
de l'aspect des donnees et de comment bien effectuer des pipelines de donnees. 
A partir de 16h le samedi vous pourrez demander a la personne organisatrice de vous poser les questions sur les defis. Il pourrait avoir de 3 a 5 questions par defi !!

Ici les problemes sont fait avec des formats de fichier plutot statique mais imaginez la puissance d'analyse si ces donnees 
arrivaient en temps reel !


Bonne chance dans vos analyses ! L'équipe de Digo Company compte sur votre expertise pour prendre des décisions financières éclairées. 🚀