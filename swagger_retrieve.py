"""
Author: Gago
"""

import requests
import http.client as http_client
import logging
import sys

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
    login_url = "https://dataone.prep.corner.local/ghibli-rest/v2/login"
    credentials = {
        "username": "gago",
        "password": "cydeon86!"
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

def get_grouped_results(token):
    partners_url = "https://dataone.prep.corner.local/ghibli-rest/v2/actors/ilist?max-items=20&getCompanies=true&getIncomingCallPartners=true&getApplications=true&getActorIcon=false"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(partners_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Errore durante il recupero dei partner: {response.status_code} - {response.text}")
    partners = response.json()

    results = []
    for partner in partners:
        iContractIdentifier = partner.get("profileIdentifier")
        if not iContractIdentifier:
            continue
        contracts_url = f"https://dataone.prep.corner.local/ghibli-rest/v2/contracts?iContractIdentifier={iContractIdentifier}"
        contracts_response = requests.get(contracts_url, headers=headers)
        if contracts_response.status_code != 200:
            continue
        contracts_data = contracts_response.json()
        print(f"CONTRACTS: {contracts_data}")

        if isinstance(contracts_data, list):
            contracts = contracts_data
        elif isinstance(contracts_data, dict):
            contracts = contracts_data.get("items", [])
        else:
            contracts = []
        for contract in contracts:
            results.append({
                "Contract": contract.get("contractIdentifier"),
                "Status": contract.get("contractStatus"),
                "Type": contract.get("contractType"),
                "Descriptions": contract.get("contractDescription"),
                "Partner": contract.get("partnerName"),
                "OutDated": contract.get("contractOutdated"),
            })
    grouped_results = {}
    for result in results:
        name = result["Partner"]
        if name not in grouped_results:
            grouped_results[name] = []
        grouped_results[name].append(result)
    return grouped_results

def print_colored(text, color):
    colors = {
        "red": "\033[91m",
        "reset": "\033[0m"
    }
    return f"{colors.get(color, '')}{text}{colors['reset']}"

def main():
    try:
        token = get_token()
        grouped_results = get_grouped_results(token)
        partner_names = list(grouped_results.keys())
        if not partner_names:
            print("Nessun partner trovato.")
            sys.exit(0)
        print("\nLista Partner:")
        for idx, name in enumerate(partner_names, 1):
            print(f"{idx}. {name}")
        while True:
            try:
                choice = int(input("\nSeleziona il numero del partner per vedere i contratti (0 per uscire): "))
                if choice == 0:
                    print("Uscita.")
                    break
                if 1 <= choice <= len(partner_names):
                    selected = partner_names[choice - 1]
                    contracts = grouped_results[selected]
                    print(f"\nContratti per {selected}:")
                    print("-" * 80)
                    for c in contracts:
                        status = c["Status"] or ""
                        contract_str = f"Contract: {c['Contract']}, \nStatus: {status}, \nType: {c['Type']}, \nUpdated: {c['Updated']},\n"
                        if status != "ENABLED":
                            print(print_colored(contract_str, "red"))
                        else:
                            print(contract_str)
                    print("-" * 60)
                else:
                    print("Selezione non valida.")
            except ValueError:
                print("Inserisci un numero valido.")
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    main()