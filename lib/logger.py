from datetime import datetime
from email.message import EmailMessage
import logging
import smtplib
import yaml
import sys

class Logger:

    # initialisation de la connexion à la base de données
    def __init__(self):
        """ Initialisation des paramètres 
         - chemin vers le fichier de log 
         - Configuration pour l'envois des erreur par mail """
        with open("config/config.yml", "r") as config_data:
            config = yaml.load(config_data, Loader=yaml.BaseLoader)

            self.logFile = config["log"]["logFile"]

            self.mailHost = config["mail"]["mailHost"]
            self.mailPort = config["mail"]["mailPort"]
            self.mailId = config["mail"]["mailId"]
            self.mailPass = config["mail"]["mailPass"]

        # Initialisation du fichier de log
        logging.basicConfig(filename=self.logFile, filemode='w', level=logging.DEBUG)

    # Fonction se chargeant d'écrire dans le fichier de log
    def writeLog(self, code, message, exception=None):
        logging.error("["+datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"] - [CODE:"+code+"] "+message)
        if exception:
            logging.debug(str(exception))

    # Fonction se chargeant d'envoyer les logs par email
    def sendLogByMail(self):
        msg = EmailMessage()
        msg['Subject']="[BDD-Bouquetin] - ERREUR integration"
        msg['From']="contact@parc-pyrenees.fr"
        msg['To']="ludovic.lepontois@pyrenees-parcnational.fr"

        with open(self.logFile) as f:
            msg.set_content(f.read())

        server = smtplib.SMTP(self.mailHost, self.mailPort)
        server.ehlo()
        server.starttls()
        server.login(self.mailId, self.mailPass)
        server.send_message(msg)
        server.close()

    # Fonction d'écriture des erreurs
    def logError(self, code, message, exception=None):
        """ Ecriture des erreur dans le fichier de logs 
        et envois par email """
        self.writeLog(code, message)
        self.sendLogByMail()
        # Erreur majeur, on interrompt le script
        sys.exit()

    # Fonction d'écriture des alertes (non bloquant)
    def logWarning(self, code, message, exception=None):
        """ Ecriture des erreur dans le fichier de logs 
        et envois par email """
        self.writeLog(code, message)        
        self.sendLogByMail()