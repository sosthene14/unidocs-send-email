import random
import string
import time
from dotenv import load_dotenv, dotenv_values
import os

from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # Applique CORS à l'application


def mongoDb(email):
    client = MongoClient(
        "mongodb+srv://sosthenemounsambote14:bmLsNa0unEp3k8PZ@bibliothequenumerique.eo3khoj.mongodb.net"
        "/bibliothequeNumerique?retryWrites=true&w=majority")
    db = client["bibliothequeNumerique"]
    collection = db["users"]
    search_filter = {"email": email}
    result = collection.find_one(search_filter)
    if result:
        return True
    else:
        return False


def generate_random_code(length):
    result = ""
    characters = string.ascii_uppercase + string.digits
    for i in range(length):
        result += random.choice(characters)
    return result


def send_email(received_id, random_code):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = os.getenv("EMAIL")
    smtp_password = os.getenv("PASSWORD")

    # Création de l'objet de message MIME
    msg = MIMEMultipart()
    msg['From'] = 'UNIDOCS'
    msg['To'] = received_id
    msg['Subject'] = 'Code de confirmation'

    # Contenu HTML du corps du message
    html = """<div style="background-color: #f5f5f5; padding: 20px;">
          <h2 style="color: #333;">Veuillez confirmer votre adresse e-mail</h2>
          <p style="background-color: #fff; padding: 10px; border: 1px solid #ccc;">
            Veuillez confirmer votre adresse e-mail afin de vous connecter à votre compte. Votre code de confirmation est :
            <span style="color: blue; font-weight: bold;">"""f'{random_code}'"""</span>
          </p>
          <p style="color: #333;">Ignorez ce message si vous n'avez pas fait de demande d'inscription</p>
          <p style="color: #333;">Merci de faire confiance à Unidocs.</p>
          <p style="color: red; font-weight: bold;">Cordialement,<br/>
          L'équipe Unidocs</p> 
        </div>
        """

    # Création de la partie HTML du message
    part = MIMEText(html, 'html')
    msg.attach(part)

    # Établissement de la connexion au serveur SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    # Fermeture de la connexion SMTP
    server.quit()


def send_email2(received_id, random_code):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = os.getenv("EMAIL")
    smtp_password = os.getenv("PASSWORD")

    # Création de l'objet de message MIME
    msg = MIMEMultipart()
    msg['From'] = 'UNIDOCS'
    msg['To'] = received_id
    msg['Subject'] = 'Réenitialisation du mot de passe'

    # Contenu HTML du corps du message
    html = """<div style="background-color: #f5f5f5; padding: 20px;">
          <h2 style="color: #333;">Vous avez fait une demande de réenitialisation de votre mot de passe</h2>
          <p style="background-color: #fff; padding: 10px; border: 1px solid #ccc;">
            Votre code de réenitialisation est :
            <span style="color: blue; font-weight: bold;">"""f'{random_code}'"""</span>
          </p>
          <p style="color: #333;">Ignorez ce message si vous n'avez pas fait de demande</p>
          <p style="color: #333;">Merci de faire confiance à Unidocs.</p>
          <p style="color: red; font-weight: bold;">Cordialement,<br/>
          L'équipe Unidocs</p> 
        </div>
        """

    # Création de la partie HTML du message
    part = MIMEText(html, 'html')
    msg.attach(part)

    # Établissement de la connexion au serveur SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    # Fermeture de la connexion SMTP
    server.quit()


def process_received_id(data):
    received_id = data.get('email')
    random_code = generate_random_code(6)
    send_email(received_id, random_code)
    response_data = {'status': '200', 'received_code': random_code}
    return response_data


def process_received_id2(data):
    received_id = data.get('email')
    random_code = generate_random_code(6)
    send_email2(received_id, random_code)
    response_data = {'status': '200', 'received_code': random_code}
    return response_data


@app.route('/sendId', methods=['POST'])  # Définition de la route et de la méthode
def receive_id():
    data = request.get_json()  # Récupération des données JSON envoyées
    response_data = process_received_id(data)
    return jsonify(response_data)


@app.route("/sendIdRT", methods=['POST'])
def receive_id2():
    data = request.get_json()  # Récupération des données JSON envoyées
    response_data = process_received_id2(data)
    return jsonify(response_data)


@app.route("/hi")
def index():
    return "sup!"

