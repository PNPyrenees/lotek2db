# Lotek2db
Script Python permettant l'alimentation automatique d'une base de données avec les localisations GPS du constructeur  [LOTEK] via son API.

# Fonctionnement général
- Récupération de la liste des capteurs dont les données doivent être récupérées
- Interrogation de l'API LOTEK pour télécharger les denières localisations
- Intégration des localisations dans la base de données

**En cas d'erreur lors de l'exécution du script, un mail sera envoyé (voir configuration)**

# Environnement
Le script a été réalisé sous Ubuntu 20.04 et développé en Python3 avec une base de données est PostgreSQL 10 et l'extension PostGIS.

D'autres configurations doivent pouvoir correspondre mais reste à tester

# Récupération des codes sources
Récupérer les codes sources avec git :
```sh
$ git clone https://github.com/PNPyrenees/lotek2db.git
```

# Installation
 - Exécuter le script d'initialisation de la base de données (install/install_db.sql)
 - Installer le paquet libpq-dev
 ```sh
$ sudo apt-get install libpq-dev
```
 - Créer un environnement virtuel python
```sh
$ cd <pathTo>/lotek2db
$ virtualenv --python=/usr/bin/python3 venv
```
 - Installer les dépendances Python
```sh
$ source venv/bin/activate
(venv) $ pip install -r install/requirements.txt
(venv) $ deactivate
```
 
# Configuration
 - Copier le fichier config/config.yml.default en le renommant config.yml
```sh
$ cp config/config.yml.default config/config.yml
```
 - éditer le fichier config.yml en renseignant chacun des paramètres
```yaml
# YAML
database:
    dbHost: 
    dbName: 
    dbPort: 
    dbUser: 
    dbPassword: 
api:
    apiUser: 
    apiPassword: 
mail:
    mailHost: 
    mailPort: 
    mailId: 
    mailPass: 
log:
    logFile: log/lotek2db.logl
```

# Automatisation
Modifier le script lotek2db.sh de sorte que le chemin vers le dossier du projet corresponde à votre environnement local (ligne 5)

Ensuite, automatiser l'exécution du script en programmant une tâche avec cron
```
$ crontab -e 
```

Exemple d'une configuration cron pour la récupération toutes les heures des données GPS
```sh
5 */1  * * * /<PathTo>/lotek2db.sh
```
Le chemin doit être en absolu.

# Focus sur le RxStatut

La données RxStatut délivré par l'API LOTEK permet de déterminer le *fix status* et le *nombre de satellites* utilisés pour la localisation.
La valeur de RxStatut est passé en binaire.
Le trois premiers bits renseignent le fix statut et les autres le nombre de satellite.

Table de correspondance du code fx_status:
| fix code  | value |
| ------------ | ------------ |
| 0 | No Fix |
| 1 | 1_SV KF Solution |
| 2 | 2_SV KF |
| 3 | 3_SV KF |
| 4 | 4 or more SV KF |
| 5 | 2-D least-squares |
| 6 | 3-D least-squares |
| 7 | DR |

**Exemple avec un RxStatut à 76 :**
```
- valeur binaire : 01001100
- trois premieris bits : 100 corespondant à 4 en base10 (décimal) -> soit "4 or more SV KF"
- les autres bits : 01001 correspondant à 9 en base 10 -> soit 9 satellites
```

#License
----
 - OpenSource - GPL-3.0
 
[![N|Solid](http://www.pyrenees-parcnational.fr/sites/parc-pyrenees.com/files/logo_pnp.jpg)](http://www.pyrenees-parcnational.fr)

   [LOTEK]: <https://www.lotek.com/>
