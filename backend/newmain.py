import time

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import psycopg2
from Secrets import secret_client_id
import secrets
import requests
import uuid
import datetime

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


class Database():
    def __init__(self):
        self.connection = psycopg2.connect(
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432",
            database="postgres"
        )
        self.cursor = self.connection.cursor()

    def insert_new_session(self, session_token: str, character_id: int, auth_token: str, refresh_token: time, creation_time: time):
        try:
            self.cursor.execute("INSERT INTO user_sessions (session_token, character_id, access_token, refresh_token, creation_time) VALUES (%s, %s, %s, %s, %s);",
                                (session_token, character_id, auth_token, refresh_token, creation_time))
            self.connection.commit()
        except Exception as e:
            print(e)

    def get_access_token_expiration(self, session_token: str) -> time:
        try:
            self.cursor.execute("SELECT access_token_expiration FROM user_sessions WHERE session_token = %s", (session_token,))
            return self.cursor.fetchone()
        except Exception as e:
            print(e)

    def close(self):
        self.cursor.close()
        self.connection.close()


@app.post("/api/token")
async def sso_token_endpoint(request_data: dict) -> dict:
    if request_data is not None:
        try:
            sso_code = request_data["SSOCode"]
            token_response = sso_token_exchange(sso_code)
            access_token = token_response["access_token"]
            refresh_token = token_response["refresh_token"]
            character_id = get_character_id(access_token)
            character_portrait = get_character_portrait(character_id)
            session_token = str(uuid.uuid4())
            creation_time = time.time()
            db.insert_new_session(session_token, character_id, access_token, refresh_token, creation_time)
            return {
                "session_token": session_token,
                "creation_time": creation_time,
                "character_portrait": character_portrait,
            }
        except Exception:
            raise HTTPException(status_code=500, detail="Internal server error")
    else:
        raise HTTPException(status_code=400, detail="No sso code provided")


def sso_token_exchange(auth_code: int) -> dict:
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

@app.get("api/contracts")
def contracts_endpoint(request_data: dict):
    session_token = request_data["session_token"]


#def token_expiration_handler(session_token):
#    expiration_time = db.get_access_token_expiration(session_token)
#    if time.time() > expiration_time:





if __name__ == '__main__':
    db = Database()
    uvicorn.run(app, host='localhost', port=5000)
