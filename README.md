# biblio-manager

Petite application Python de gestion de médiathèque : catalogue de livres, gestion des emprunts, calcul des amendes de retard, file de réservation et notifications aux adhérents.

Ce dépôt sert de support au cas pratique du cours **« Prédiction des anomalies logicielles par l'IA »** (ESGI, 2026-2027). Son historique Git a été construit volontairement, avec des commits correctifs identifiés, afin de permettre aux étudiants d'extraire l'historique, de construire des features de risque, puis d'entraîner et d'évaluer un modèle de Machine Learning prédisant les fichiers les plus susceptibles de contenir une anomalie.

## Fonctionnalités

- **Catalogue** : ajout, suppression et recherche de livres (`catalog.py`)
- **Emprunts** : création, retour et prolongation d'un emprunt (`loan_manager.py`)
- **Amendes** : calcul du montant dû en cas de retard (`fine_calculator.py`)
- **Réservations** : file d'attente lorsqu'un livre est indisponible (`reservation.py`)
- **Notifications** : rappels d'échéance et avis de retard, simulés (`notifications.py`)
- **Rapports** : statistiques d'usage et suivi des retards (`reports.py`)

## Prérequis

- Python 3.10 ou supérieur
- pip

## Installation

```bash
git clone <url-du-depot>
cd biblio-manager
python -m venv venv
source venv/bin/activate        # sous Windows : venv\Scripts\activate
pip install -r requirements.txt
```

## Utilisation

```python
from biblio.catalog import Catalog
from biblio.models.book import Book
from biblio.models.member import Member
from biblio.loan_manager import LoanManager

catalog = Catalog()
catalog.add_book(Book(id=1, titre="1984", auteur="George Orwell", isbn="9780451524935", exemplaires_total=3))

member = Member(id=1, nom="Jeanne Martin", email="jeanne.martin@example.com")

loan_manager = LoanManager(catalog)
loan = loan_manager.create_loan(book_id=1, member=member)
```

## Lancer les tests

```bash
pytest tests/
```

## Structure du projet

```
biblio-manager/
├── README.md
├── requirements.txt
├── src/biblio/
│   ├── __init__.py
│   ├── exceptions.py
│   ├── utils.py
│   ├── models/
│   │   ├── book.py
│   │   ├── member.py
│   │   └── loan.py
│   ├── catalog.py
│   ├── loan_manager.py
│   ├── fine_calculator.py
│   ├── reservation.py
│   ├── notifications.py
│   └── reports.py
└── tests/
    ├── test_catalog.py
    ├── test_loan_manager.py
    ├── test_fine_calculator.py
    └── test_reservation.py
```

## Contexte pédagogique

Ce dépôt n'est pas destiné à un usage en production. Il a été conçu comme **fil rouge du cas pratique** du cours sur la prédiction des anomalies logicielles par l'IA :

1. Extraction de l'historique Git et identification des commits de correction.
2. Construction de features de risque par fichier (taille, complexité, churn, nombre de commits, nombre de développeurs, ancienneté).
3. Construction d'un dataset supervisé (features + label `bug`).
4. Entraînement et évaluation d'un modèle de classification.
5. Priorisation des tests à partir des probabilités de risque du modèle.

## Licence

MIT — dépôt pédagogique créé pour les besoins du cours.
