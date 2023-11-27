import requests
import base64

# Définissez les informations d'authentification de votre application Dropbox
app_key = "qeubsdg1i0wk7dm"
app_secret = "9szm46gpu2fsaok"
refresh_token = "1jqkJyvaztkAAAAAAAAAAbU3M3LzODgtfmEtnzI-vhS5zdft65vvSNY3oR2ssGJ9"

# Construisez l'en-tête d'authentification
base64authorization = base64.b64encode(f"{app_key}:{app_secret}".encode()).decode()
headers = {"Authorization": f"Basic {base64authorization}"}

# Construisez les données de la requête
payload = {"refresh_token": refresh_token, "grant_type": "refresh_token"}

# Effectuez la requête POST
response = requests.post("https://api.dropbox.com/oauth2/token", data=payload, headers=headers)

# Traitez la réponse
if response.status_code == 200:
    response_data = response.json()
    print(response_data)
else:
    print(f"Erreur: {response.status_code} - {response.text}")
