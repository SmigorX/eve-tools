from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import psycopg2
from Secrets import secret_client_id, secret_key
import secrets
import requests
import uuid
import time
import base64
from data_classes import SSOCode, ContractData
from db import Database

app = FastAPI()

origins = [
    "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#def token_refresh_handler(session_token: str):
#    expiration_time = db
#    get_access_token_expiration(session_token)
#    print(expiration_time)
#    #if time.time() > expiration_time:
#    if False:
#        refresh_token = db.get_refresh_token(session_token)
#        client_credentials = f"{secret_client_id}:{secret_key}"
#        client_authorization = base64.b64encode(client_credentials.encode("utf-8")).decode("utf-8")
#
#        request_url = "https://login.eveonline.com/oauth/token"
#        headers = {
#            'Content-Type': 'application/x-www-form-urlencoded',
#            'Host': 'login.eveonline.com',
#            'Authorization': f'Basic {client_authorization}'
#        }
#        data = {
#            'grant_type': 'refresh_token',
#            'refresh_token': refresh_token,
#        }
#
#        token = requests.post(request_url, headers=headers, data=data)
#
#        new_expiration_time = time.time() + token.json()["expires_in"]
#
#        if token.status_code == 200:
#            if refresh_token != token.json()["refresh_token"]:
#                raise Exception("Error, refresh token mismatch")
#            db.refresh_access_token(token.json()["access_token"], refresh_token, new_expiration_time)
#        else:
#            raise HTTPException(status_code=504, detail=f"Error, could not refresh token. Status code: {token.status_code}, Response: {token.text}")
#    return


@app.post("/dev/token")
async def sso_token_endpoint(request_data: SSOCode) -> dict:
    access_token_lifetime = 20*60*1000

    if request_data is not None:
        try:
            sso_code = request_data.SSOCode
            token_response = exchange_sso_token(sso_code)
            access_token = token_response["access_token"]
            character_id = get_character_id(access_token)
            creation_time = time.time()
            session_token = str(uuid.uuid4())

            db.insert_new_session(
                session_token=session_token,
                character_id=get_character_id(access_token),
                access_token=access_token,
                refresh_token=token_response["refresh_token"],
                creation_time=creation_time,
                access_token_expiration_time=creation_time + access_token_lifetime
            )

            character_portrait = get_character_portrait(character_id)

            return {
                "session_token": session_token,
                "creation_time": creation_time,
                "character_portrait": character_portrait,
            }
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")
    else:
        raise HTTPException(status_code=400, detail="No sso code provided")


def exchange_sso_token(auth_code: str) -> dict:
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
    token = requests.post(request_url, headers=headers, data=body)

    if token.status_code == 200:
        return token.json()


def get_character_id(access_token: str) -> int:
    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    response = requests.get('https://esi.evetech.net/verify', headers=headers)
    if response.status_code == 200:
        return response.json()['CharacterID']
    else:
        raise Exception("Error, could not get the character ID " + str(response.status_code))


def get_character_portrait(character_id: int) -> str:
    request_url = f"https://esi.evetech.net/latest/characters/{character_id}/portrait/?datasource=tranquility"
    headers = {
        'accept': 'application/json',
        'Cache-Control': 'no-cache',
    }
    character_portrait = requests.get(request_url, headers=headers).json()
    return character_portrait["px128x128"]


@app.get("/dev/contracts")
def contracts_endpoint(request_data: ContractData):
    try:
        session_token = request_data.session_token
        token_refresh_handler(session_token)
        character_id = db.get_character_id(session_token)
        print(str(character_id))
        corp_id = get_corp_id(character_id)
        print(str(corp_id) + "corp_id")
        contracts = get_contract(corp_id)
        return contracts
    except KeyError:
        raise HTTPException(status_code=400, detail="No session token provided")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


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
        raise HTTPException(status_code=response.status_code,
                            detail=f"Error, could not get the corporation ID. Response: {response.text}")


def get_contract(corporation_id: int):
    try:
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
    except Exception as e:
        print(e)
    print(response.status_code)
    if response.status_code == 200:
        return response.json()


if __name__ == '__main__':
    db = Database("postgresql://postgres:postgres@localhost:5432/postgres")
    print(db.retrieve_character_id("1"))
    uvicorn.run(app, host='localhost', port=5000)
