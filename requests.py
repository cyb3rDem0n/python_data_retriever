import requests

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
    response.raise_for_status()
    token = response.json().get("access_token")
    if not token:
        raise Exception("Token non trovato nella risposta di autenticazione")
    return token

def get_actors(token):
    url = "https://dataone.prep.corner.local/ghibli-rest/v2/actors/ilist"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()  # Deve essere una lista di dict

def get_contracts(token, profile_identifier):
    url = f"https://dataone.prep.corner.local/ghibli-rest/v2/contracts?iContractIdentifier={profile_identifier}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()  # Deve essere una lista di dict

def main():
    try:
        token = get_token()
        actors = get_actors(token)
        if not actors:
            print("Nessun partner trovato.")
            return

        print("Lista partner:")
        for idx, actor in enumerate(actors, 1):
            print(f"{idx}. idProfile: {actor.get('idProfile')} - profileIdentifier: {actor.get('profileIdentifier')}")

        while True:
            try:
                choice = int(input("Seleziona il numero del partner: "))
                if 1 <= choice <= len(actors):
                    selected = actors[choice - 1]
                    break
                else:
                    print("Selezione non valida.")
            except ValueError:
                print("Inserisci un numero valido.")

        contracts = get_contracts(token, selected["profileIdentifier"])
        if not contracts:
            print("Nessun contratto trovato.")
            return

        print(f"\nContratti trovati: {len(contracts)}")
        for contract in contracts:
            print(f"contractIdentifier: {contract.get('contractIdentifier')}")
            print(f"contractStatus: {contract.get('contractStatus')}")
            print(f"contractDescription: {contract.get('contractDescription')}")
            print(f"contractType: {contract.get('contractType')}")
            print(f"partnerName: {contract.get('partnerName')}")
            print("-" * 40)
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    main()