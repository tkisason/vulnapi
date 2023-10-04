#!/usr/bin/env python3
from datetime import datetime, timedelta

import json, yaml, jwt, time, os, requests, pprint, jinja2
import sqlite3
import logging
from fastapi import Depends, FastAPI, HTTPException, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.requests import Request

SECRET_KEY = "123456"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 600
today = time.strftime("%Y-%m-%d")

accounts_db = json.loads(open("data/accounts.json").read())
users_db = json.loads(open("data/users.json").read())
sqldb = sqlite3.connect("data/data.sqlite")
pp = pprint.PrettyPrinter(depth=4)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class User(BaseModel):
    username: str
    email: str = None
    full_name: str = None
    disabled: bool = None
    admin: bool = None


class Notification(BaseModel):
    email: str


class UserInDB(User):
    hashed_password: str


class Accounts(BaseModel):
    account: str
    username: str
    amount: float


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    for user in db:
        if username == user["username"]:
            return UserInDB(**user)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except:
        raise credentials_exception
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token/", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/accounts/")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    customer = [
        customer
        for customer in accounts_db["data"]
        if customer["username"].find(current_user.username) >= 0
    ]
    return customer


@app.get("/me/notifications/")
async def get_notifications_addr(
    request: Request, current_user: User = Depends(get_current_active_user)
):
    pp.pprint(dict(request.headers))
    for i, user in enumerate(users_db):
        if user["username"] == current_user.username:
            return {"email": user["email"]}


@app.post("/me/notifications/")
async def set_notifications_addr(notification: Notification, request: Request):
    pp.pprint(dict(request.headers))
    email = await request.json()
    for i, user in enumerate(users_db):
        if user["username"] == current_user.username:
            users_db[i] = {**user, **email}
            print(users_db)
    return email


@app.post("/bulk/")
async def yaml_bulk_upload(request: Request, file: UploadFile = File(...)):
    pp.pprint(dict(request.headers))
    contents = await file.read()
    return yaml.load(contents)


@app.get("/bank_codes/")
async def read_some_bank_codes(request: Request, code="1"):
    pp.pprint(dict(request.headers))
    query = sqldb.cursor()
    parameter = f"select * from bank_codes where code='{code}';"
    logging.info("QUERY> " + parameter)
    results = query.execute(parameter).fetchone()
    if results == None:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        return {"bank": results[0], "code": results[1], "swift": results[2]}


@app.get("/exchangerate/")
async def get_current_exchange_rates_from_file_cache(
    request: Request, datestamp=time.strftime("%Y-%m-%d")
):
    pp.pprint(dict(request.headers))
    if os.path.exists("./data/" + datestamp):
        print("./data/" + datestamp)
        return open("./data/" + datestamp).read()
    else:
        data = requests.get("https://api.hnb.hr/tecajn-eur/v3").content
        output = open("./data/" + today, "w")
        output.write(str(data))
        output.close()
        return open("./data/" + datestamp).read()


@app.get("/currentexchangerate/")
async def read_from_hnb_api(request: Request, url="https://api.hnb.hr/tecajn-eur/v3"):
    pp.pprint(dict(request.headers))
    data = requests.get(url).content
    return data


@app.get("/greeter/")
async def greet_the_user(request: Request, name="world"):
    pp.pprint(dict(request.headers))
    data = jinja2.Template("Hello " + name).render()
    return data


@app.trace("/vulnapi/inmemory/usersdb")
async def dump_usersdb():
    return users_db


@app.trace("/vulnapi/inmemory/accounts")
async def dump_accounts():
    return accounts_db


@app.get("/")
async def main(request: Request):
    pp.pprint(dict(request.headers))
    return {"info": "Visit the /docs endpoint for the OpenAPI UI"}
