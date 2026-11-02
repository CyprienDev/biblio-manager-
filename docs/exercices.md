# Analyse temporelle de l'historique Git

## 1. Définir la photographie étudiée

Relever le SHA du jalon autorisé, sa date réelle et le fuseau horaire.
Lister les fichiers métier Python présents à cette révision dans src/biblio,
en excluant tests, documentation et __init__.py. Travailler sur une copie
de cette révision ; ne pas utiliser le contenu actuel pour une ancienne coupure.
Documenter les renommages, suppressions et la convention de suivi des chemins.

## 2. Extraire les changements disponibles

À partir du SHA, extraire l'historique accessible avec git log --numstat.
Conserver pour chaque changement son SHA, sa date, son auteur, son message,
son chemin et ses nombres de lignes ajoutées et supprimées. Ne prendre aucun
commit postérieur au jalon. Documenter le traitement des merges et binaires.
Les dates peuvent différer du calendrier pédagogique : utiliser Git.

## 3. Construire les métriques par fichier

Calculer nombre de commits, nombre d'auteurs, ajouts, suppressions et churn
(ajouts + suppressions), âge depuis première apparition et taille à la coupure.
Si une complexité est utilisée, préciser l'outil, sa version et son agrégation.
Ne jamais calculer les features depuis les correctifs de la fenêtre future.
Vérifier manuellement deux fichiers et conserver les commandes et paramètres.

## 4. Établir une baseline

Classer les fichiers par churn décroissant ; départager les ex æquo par chemin.
Choisir k avant consultation des résultats, puis conserver le classement.
Comparer ensuite une baseline de complexité et le modèle sur les mêmes fichiers.
Un classement de risque n'est pas une preuve qu'un fichier contient un bug.

## 5. Préparer l'évaluation

La cible est une correction future d'un fichier existant à la coupure dans
les 28 jours suivants. Les labels ne deviennent définitifs qu'après cette fenêtre.
Les messages fix, patch ou résolution donnent des candidats, pas une vérité
terrain certaine. Documenter la règle de détection et ses limites ; les labels
enseignants sont distribués séparément. Aucun découpage aléatoire fichier-date.
Les fenêtres qui se chevauchent ne sont pas des échantillons indépendants.

## Livrables

Fournir SHA de coupure, table des métriques, règles d'extraction, classement
churn et rapport des limites. Conserver séparément features, prédictions et
labels futurs pour éviter les fuites. Ne pas publier de labels privés.
