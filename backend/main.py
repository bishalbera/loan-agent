from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.ai.predict import predict_loan_approval

from backend.db import schemas

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/")
def hello():
    return "Hello World 🖤"

@app.post("/loan-agent")
def approval_prediction(approval_req: schemas.LoanPredictorSchema):
    request_data = approval_req.dict()
    prediction = predict_loan_approval(
        **request_data
    )

    return prediction.json()