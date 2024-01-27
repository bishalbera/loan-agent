from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.ai.predict import predict_loan_approval
from sqlalchemy.orm import Session

from backend.db import schemas
from backend.db.connect import get_db_session
from backend.db.models import LoanPredictor

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
async def approval_prediction(approval_req: schemas.LoanPredictorSchema, db: Session = Depends(get_db_session)):
    try:
        request_data = approval_req.dict()
        applied_data = LoanPredictor(**request_data)
        db.add(applied_data)
        db.commit()

        prediction = await predict_loan_approval(**request_data)
        return prediction.json()  
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
