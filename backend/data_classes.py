from pydantic import BaseModel


class SSOCode(BaseModel):
    SSOCode: str


class ContractData(BaseModel):
    session_token: str
