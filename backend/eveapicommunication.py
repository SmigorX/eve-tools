def exchange_sso_token(auth_code: str) -> dict:
    '''
    Exchenges the single use token received after login for a refresh token and an access token
    '''
    secret_client_id = os.environ["APPLICATION_ID"]
    code_challenge = secrets.token_urlsafe(100)[:128]

    request_url = "https://login.eveonline.com/oauth/token"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    body = {
        'grant_type': "authorization_code",
        'code': f"{auth_code}",
        'code_verifier': f"{code_challenge}",
        'client_id': f"{secret_client_id}",
    }

    response = requests.post(request_url, headers=headers, data=body)

    if response.status_code == 200:
        return response.json()
    else:
        # TODO rewrite proper error logging
        raise Exception(
            "Error, could not exchange the auth code for a token " +
            str(response.status_code)
        )


def get_character_id(access_token: str) -> int:
    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    response = requests.get('https://esi.evetech.net/verify', headers=headers)

    if response.status_code == 200:
        return response.json()['CharacterID']
    else:
        # TODO rewrite proper error logging
        raise Exception(
            "Error, could not get the character ID " + str(response.status_code))


def get_character_portraits(character_id: int) -> str:
    request_url = f"https://esi.evetech.net/latest/characters/{character_id}/portrait/?datasource=tranquility"

    headers = {
        'accept': 'application/json',
        'Cache-Control': 'no-cache',
    }

    response = requests.get(request_url, headers=headers).json()

    if response.status_code == 200:
        return response.json()
    else:
        # TODO rewrite proper error logging
        raise Exception(
            "Error, could not get the character portrait " +
            str(response.status_code)
        )


def get_corp_id(character_id: int) -> int:
    headers = {
        'accept': 'application/json',
        'Cache-Control': 'no-cache',
    }

    params = {
        'datasource': 'tranquility',

    }

    response = requests.get(f'https://esi.evetech.net/latest/characters/{character_id}/',
                            params=params, headers=headers)
    corporation_id = int(response.json()["corporation_id"])

    if response.status_code == 200:
        return corporation_id
    else:
        # TODO rewrite proper error logging
        raise Exception(
            "Error, could not get the corporation ID " +
            str(response.status_code)
        )


def get_contract(corporation_id: int):
    secret_client_id = os.environ["APPLICATION_ID"]

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {secret_client_id}",
        "Cache-Control": "no-cache",
    }

    params = {
        "datasource": "tranquility"
    }

    response = requests.get(
        f"https://esi.evetech.net/latest/corporations/{corporation_id}/contracts/",
        headers=headers,
        params=params)

    if response.status_code == 200:
        return response.json()
    else:
        # TODO rewrite proper error logging
        raise Exception(
            "Error, could not get the contracts " +
            str(response.status_code)
        )

