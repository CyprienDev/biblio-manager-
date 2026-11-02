# Protocole d'évaluation temporelle

## Coupure réelle et traçabilité

Le jalon est le commit de publication de ce document, identifié par son SHA
réel et éventuellement le tag cours-03. Relever ensuite ce SHA dans le journal
d'expérience et les fichiers de prédictions. Un tag doit désigner ce commit
sans être déplacé. La publication effective remplace la date prévue du 30 octobre.
Ce protocole est publié après le début de novembre ; il ne constitue pas un
gel effectué avant novembre. Ne pas antidater les commits ou les expériences.

## Population et cible

Inclure les fichiers métier .py existant sous src/biblio à la coupure,
hors __init__.py. Exclure tests, docs et fichiers apparus ensuite.
La cible est au moins une correction de bug du fichier dans les 28 jours
suivant la coupure, du lendemain à J+28 inclus selon Europe/Paris.
Cela prédit une correction future, pas la présence certaine d'un défaut.
Relever les dates réelles avant de construire les labels et documenter
les renommages. N'évaluer les négatifs qu'après la fin de la fenêtre.

## Features et données d'apprentissage

Calculer taille, âge, historique de changements et complexité uniquement
avec les commits et le code accessibles à la coupure. Entraîner uniquement
sur des fenêtres dont les labels sont entièrement connus à cette date.
Une validation rétrospective de développement ne vaut pas test prospectif.
Expliquer les chevauchements temporels et ne pas employer de split aléatoire.

## Paramètres et prédictions à figer

Avant toute utilisation des observations futures, enregistrer dans le journal
d'expérience : SHA du code d'extraction, versions des outils, features, données
d'entraînement, traitement des valeurs manquantes, modèle, hyperparamètres et
graine. Exporter chemin, score et rang pour tous les fichiers de la population.
Conserver également les classements churn et complexité. Départager les scores
égaux par chemin croissant ; utiliser k = min(5, nombre de fichiers).
Le présent document ne prétend pas que le modèle ou les prédictions sont déjà
produits : leur gel exige ces artefacts horodatés. Si l'équipe a déjà consulté
les bugs prévus ou des labels futurs, déclarer cette connaissance et limiter
l'exercice à une démonstration rétrospective ; ne pas revendiquer un test aveugle.

## Mesures et limites

Comparer sur une même population précision et rappel à k, average precision
(aire résumée de la courbe précision-rappel) et comptes TP, FP, FN.
Sans positif, indiquer que rappel et average precision ne sont pas définis.
Ne pas ajuster le modèle après observation de la fenêtre de test. Documenter
les divergences entre labels par messages et vérité terrain privée fournie
séparément, sans modifier les prédictions figées. Peu de fichiers et de bugs,
un historique pédagogique construit et des fenêtres dépendantes limitent
fortement la portée des résultats. Une validation externe reste nécessaire.
