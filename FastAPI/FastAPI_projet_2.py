import json
import pickle
from fastapi import FastAPI, Depends, HTTPException, status
from starlette.responses import RedirectResponse
from data_preparation import prepare_data
from donnees import Features, Prediction
from fastapi.security import HTTPBasic, HTTPBasicCredentials

api = FastAPI()
security = HTTPBasic()

with open("./data/model.pkl", "rb") as f:
    model = pickle.load(f)


with open("./users.json", "r") as f:
    users = json.load(f)


def check_credentials(credentials: HTTPBasicCredentials = Depends(security)):

    user = list(filter(lambda u: u["username"] == credentials.username, users))

    if not len(user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    user = user[0]

    if user["password"] != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username


@api.post("/prediction", response_model=Prediction)
def make_prediction(data: Features, username: str = Depends(check_credentials)):

    df = prepare_data(data)

    proba = round(model.predict_proba(df)[0][1], 4)
    prediction = int(model.predict(df)[0])

    return {"prediction": prediction, "proba": proba}


@api.get("/")
def redirect_to_docs():

    return RedirectResponse(url="/docs")

