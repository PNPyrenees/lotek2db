from lib.Database import Database
from lib.api import Api

# temporaire por test
#from lib.logger import Logger
#import json

def main():
    """Fonction principale de mise à jour des données GPS"""

    # Initialisation de la connexion à la base de données
    database = Database()

    # Authentification auprès de l'API (->récupération token)
    api = Api()

    # Récupération de la liste des capteur actif 
    # et de leur date de dernière synchronisation
    capteurs = database.selectCapteurs()

    # On boucle sur les capteurs pour récupérer les données
    for capteur in capteurs:
        capt_id = capteur['capt_id']
        deviceId = capteur['capt_id_constructeur']
        dtStart = capteur['loc_date_utc'].strftime("%Y-%m-%dT%H:%M:%S")
        
        responses = api.getlocalisation(deviceId, dtStart)

        #logger = Logger()

        if responses is not None:
            # On boucle sur les nouvelles localisations GPS
            for response in responses:
            
                #logger.writeLog("999-1", json.dumps(response))
                
                loc_long = response['Longitude']
                loc_lat = response['Latitude']
                loc_dop = response['PDOP']
                loc_altitude_capteur = response['Altitude']
                loc_temperature_capteur = response['Temperature']
                loc_date_capteur_utc = response['RecDateTime']
                rxstatut_bin = bin(response['RxStatus'])
                fix_status_id = int(rxstatut_bin[len(rxstatut_bin) - 3 : len(rxstatut_bin)], 2) # Extraction de 3 premiers bit du RxStatut correspondant à l'identifiant du fix_status
                loc_nb_satellites = int(rxstatut_bin[rxstatut_bin.index('b') + 1 : len(rxstatut_bin) - 3], 2) # Extraction des 4 bit suivant du RxStatut correspondant aunombre de satellites

                if loc_long == 0 and loc_lat == 0:
                    # Ici on n'a pas de coordonnées pour ce capteur à cette date
                    loc_commentaire = 'Erreur : Pas de coordonnées'
                    loc_anomalie = True

                    database.insertNoLocData(
                        capt_id, 
                        loc_dop, 
                        loc_altitude_capteur, 
                        loc_temperature_capteur, 
                        loc_date_capteur_utc, 
                        loc_commentaire, 
                        loc_anomalie,
                        fix_status_id,
                        loc_nb_satellites
                    )
                else:
                    # Ici il n'y a pas d'anomalie dans les coordonnées
                    database.insertLocData(
                        capt_id, 
                        loc_long, 
                        loc_lat, 
                        loc_dop, 
                        loc_altitude_capteur, 
                        loc_temperature_capteur, 
                        loc_date_capteur_utc,
                        fix_status_id,
                        loc_nb_satellites
                    )

    # Fermeture de la connexion à la base de données
    database.close()

if __name__ == '__main__':
    main()



