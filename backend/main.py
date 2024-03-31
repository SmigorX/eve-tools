from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import psycopg2
import uuid
import time
import base64
from data_classes import SSOCode, ContractData
from dbdupe import Database
from eveapicommunication import *
import os
import secrets
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


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


def access_token_validity_checker(session_token: str):
    secret_client_id = os.environ["APPLICATION_ID"]
    secret_key = os.environ["APPLICATION_KEY"]

    access_token_expiration = db.UserSessions.retrieve_access_token_expiration(
        session_token)

    if time.time() > access_token_expiration:
        refresh_token = db.UserSessions.retrieve_refresh_token(session_token)

        client_authorization = base64.b64encode(
            f"{secret_client_id}:{secret_key}".encode("utf-8")).decode("utf-8")

        request_url = "https://login.eveonline.com/oauth/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "login.eveonline.com",
            "Authorization": f"Basic {client_authorization}"
        }
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        response = requests.post(request_url, headers=headers, data=data)

        if response.status_code == 200:
            if refresh_token != response.json()["refresh_token"]:
                # TODO rewrite proper error logging
                raise Exception("Error, refresh token mismatch")
            else:
                db.Characters.refresh_access_token(
                    session_token,
                    response.json()["access_token"],
                    response.json()["refresh_token"],
                    time.time() + response.json()["expires_in"]
                )
        else:
            raise HTTPException(status_code=504, detail=f"Error, could not refresh token. Status code: {response.status_code}, Response: {response.text}")


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

            character_portraits = get_character_portraits(character_id)

            return {
                "session_token": session_token,
                "creation_time": creation_time,
                "character_portrait": character_portraits,
            }
        except Exception:
            raise HTTPException(
                status_code=500, detail="Internal server error")
    else:
        raise HTTPException(status_code=400, detail="No sso code provided")


@app.get("/dev/contracts")
def contracts_endpoint(request_data: ContractData):
    try:
        session_token = request_data.session_token
        access_token_validity_checker(session_token)
        character_id = db.UserSessions.retrieve_character_id()
        print(str(character_id))
        corp_id = get_corp_id(character_id)
        print(str(corp_id) + "corp_id")
        contracts = get_contract(corp_id)
        return contracts
    except KeyError:
        raise HTTPException(
            status_code=400, detail="No session token provided")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == '__main__':
    db = database_connection()


    uvicorn.run(app, host='localhost', port=5000)
