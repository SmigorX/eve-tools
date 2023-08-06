from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from Secrets import secret_client_id
import secrets
import requests

app = FastAPI()

origins = [                         # origin of requests
    "http://localhost:5173",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/dev/token")
async def receive_data(data: dict):
    received_auth_token = data.get('authToken')
    if received_auth_token:
        auth_token = await token_exchange(received_auth_token)
        if isinstance(auth_token, str):
            login_return_data = await handle_logging(auth_token)
            if isinstance(login_return_data, dict):
                print("returning data " + str(login_return_data))
                return login_return_data


async def token_exchange(authCode: int) -> str:
    client_id = secret_client_id
    code_challenge = secrets.token_urlsafe(100)[:128]
    request_url = "https://login.eveonline.com/oauth/token"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    body = {
        'grant_type': "authorization_code",
        'code': f"{authCode}",
        'code_verifier': f"{code_challenge}",
        'client_id': f"{client_id}",
    }
    token = requests.post(request_url, headers=headers, data=body)

    if token.status_code == 200:
        return str(token.json()['access_token'])
    else:
        return token.status_code


async def handle_logging(token: str) -> dict:
    char_id_headers = {
        'Authorization': f"Bearer {token}",
    }

    character_id_response = requests.get('https://esi.evetech.net/verify', headers=char_id_headers)

    if character_id_response.status_code == 200:
        character_id = character_id_response.json()['CharacterID']
    else:
        character_id = character_id_response.status_code

    character_portrait_headers = {
        'Accept': 'application/json',
        'Cache-Control': 'no-cache',
    }

    character_portrait_response = requests.get(f'https://esi.evetech.net/latest/characters/{character_id}/portrait/?datasource=tranquility', headers=character_portrait_headers)

    if character_portrait_response.status_code == 200:
        character_portrait = character_portrait_response.json()["px64x64"]
    else:
        character_portrait = character_portrait_response.status_code

    if character_id_response.status_code == 200 and character_portrait_response.status_code == 200:
        login_response = {
            'character_id': character_id,
            'character_portrait': character_portrait
        }
        return login_response
    else:
        return (f"Character id: {character_id}, character portrait: {character_portrait}")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=5000)
