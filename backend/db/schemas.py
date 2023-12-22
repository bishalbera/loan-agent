from pydantic import BaseModel, EmailStr


class LoanPredictorSchema(BaseModel):

    Gender: str
    Married: str
    Dependents: str
    Education: str
    Self_Employed: str
    ApplicantIncome: int
    CoapplicantIncome: float
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: float
    Property_Area: str
    Loan_Status: str
    Email: EmailStr
