"""
Author: Gago
"""
import requests
import http.client as http_client
import logging

# Abilita il debug HTTP
http_client.HTTPConnection.debuglevel = 1

# Configura il logging per mostrare le richieste e risposte HTTP
logging.basicConfig(level=logging.CRITICAL)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.CRITICAL)
requests_log.propagate = True

def authenticate_and_retrieve_data():
    # Endpoint di login
    login_url = "https://dataone.test.corner.local/ghibli-rest/v2/login"
    # Credenziali di autenticazione
    credentials = {
        "username": "ghibli",
        "password": "ghibli"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Autenticazione e ottenimento del token
    response = requests.post(login_url, data=credentials, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Errore durante l'autenticazione: {response.status_code} - {response.text}")
    
    token = response.json().get("access_token")
    if not token:
        raise Exception("Token non trovato nella risposta di autenticazione")

    # Header per le chiamate successive
    auth_headers = {
        "Authorization": f"Bearer {token}"
    }

    # Chiamata per ottenere i partner
    partners_url = "https://dataone.test.corner.local/ghibli-rest/v2/partners?max-items=5"
    response = requests.get(partners_url, headers=auth_headers)
    if response.status_code != 200:
        raise Exception(f"Errore durante il recupero dei partner: {response.status_code} - {response.text}")

    print("Lista dei partner trovati:")
    for partner in response.json():
        print(f"- {partner.get('name', 'Nome non disponibile')} (ID: {partner.get('idProfile', 'ID non disponibile')})")
    
    partners = response.json()


    # Creazione della struttura dati per i partner e i loro contratti
    partner_contracts = {}
    contracts_url = "https://dataone.test.corner.local/ghibli-rest/v2/contracts"

    for partner in partners:

        partner_id = partner.get("idProfile")
        if not partner_id:
            continue

        # Chiamata per ottenere i contratti del partner
        response = requests.get(f"{contracts_url}?idPartner={partner_id}", headers=auth_headers)
        if response.status_code != 200:
            raise Exception(f"Errore durante il recupero dei contratti per il partner {partner_id}: {response.status_code} - {response.text}")
        
        contracts = response.json()
        partner_contracts[partner_id] = {
            "partner_info": partner,
            "contracts": contracts
        }

    return partner_contracts

# Esempio di utilizzo
if __name__ == "__main__":
    try:
        data = authenticate_and_retrieve_data()
        print(data)
    except Exception as e:
        print(f"Errore: {e}")