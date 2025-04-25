"""
Author: Gago
"""

import requests
import http.client as http_client
import logging

# Abilita il debug HTTP
http_client.HTTPConnection.debuglevel = 0

# Configura il logging per mostrare le richieste e risposte HTTP
logging.basicConfig(level=logging.CRITICAL)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.CRITICAL)
requests_log.propagate = True

def get_token():
    """
    Effettua la chiamata per ottenere il token di autenticazione.
    """
    login_url = "https://dataone.test.corner.local/ghibli-rest/v2/login"
    credentials = {
        "username": "",
        "password": ""
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(login_url, data=credentials, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Errore durante l'autenticazione: {response.status_code} - {response.text}")
    
    response_json = response.json()
    token = response_json.get("access_token")
    if not token:
        raise Exception("Token non trovato nella risposta di autenticazione")
    
    return token

def get_partners(token):
    """
    Effettua la chiamata per ottenere i partner utilizzando il token di autenticazione.
    """
    partners_url = "https://dataone.test.corner.local/ghibli-rest/v2/partners?max-items=5"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(partners_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Errore durante il recupero dei partner: {response.status_code} - {response.text}")
    
    partners_data = response.json()
    results = []

    # Verifica se la risposta è una lista o un dizionario
    if isinstance(partners_data, list):
        partners = partners_data
    elif isinstance(partners_data, dict):
        partners = partners_data.get("items", [])
    else:
        raise Exception(f"Formato della risposta non previsto: {type(partners_data)}")

    for partner in partners:
        id_partner = partner.get("idProfile")
        if not id_partner:
            continue
        
        contracts_url = f"https://dataone.test.corner.local/ghibli-rest/v2/contracts?idPartner={id_partner}"
        contracts_response = requests.get(contracts_url, headers=headers)

        if contracts_response.status_code != 200:
            raise Exception(f"Errore durante il recupero dei contratti per il partner {id_partner}: {contracts_response.status_code} - {contracts_response.text}")

        contracts_data = contracts_response.json()

        # Verifica se contracts_data è una lista o un dizionario
        if isinstance(contracts_data, list):
            contracts = contracts_data
        elif isinstance(contracts_data, dict):
            contracts = contracts_data.get("items", [])
        else:
            raise Exception(f"Formato della risposta non previsto: {type(contracts_data)}")

        for contract in contracts:
            results.append({
                "Contract": contract.get("contractIdentifier"),
                "Status": contract.get("contractStatus"),
                "Type": contract.get("contractType"),
                "Name": contract.get("partnerName"),
            })

    # Raggruppa i risultati per "Name"
    grouped_results = {}
    for result in results:
        name = result["Name"]
        if name not in grouped_results:
            grouped_results[name] = []
        grouped_results[name].append(result)

    # Stampa i risultati raggruppati in modo chiaro
    for name, contracts in grouped_results.items():
        print(f"\nName: {name}")
        for contract in contracts:
            print(f"  Contract: {contract['Contract']}, Status: {contract['Status']}, Type: {contract['Type']}")



if __name__ == "__main__":
    try:
        token = get_token()
        get_partners(token)
    except Exception as e:
        print(f"Errore: {e}")