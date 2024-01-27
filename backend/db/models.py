from sqlalchemy import Column, Float, Integer, String

from sqlalchemy.orm import  DeclarativeBase


class Base(DeclarativeBase):
    pass


class LoanPredictor(Base):

    __tablename__ = "loan_data"

    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, nullable=False)
    Gender = Column(String)
    Married = Column(String)
    Dependents = Column(Float)
    Education = Column(String)
    Self_Employed = Column(String)
    ApplicantIncome = Column(Integer)
    CoapplicantIncome = Column(Integer)
    LoanAmount = Column(Integer)
    Loan_Amount_Term = Column(Float)
    Credit_History = Column(Float)
    Property_Area = Column(String)
    Loan_Status = Column(String)
    Email = Column(String)
