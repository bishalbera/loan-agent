import uuid
import requests

MINDSDB_QUERY_ENDPOINT = "http://127.0.0.1:47334/api/sql/query"


def mindsdb_query(MINDSDB_QUERY_ENDPOINT, sql_query):
    headers = {"Content-Type": "application/json"}
    return requests.post(MINDSDB_QUERY_ENDPOINT, json={"query": sql_query}, headers=headers)


def predict_loan_approval(
    Email,
    Gender="Female",
    Married="No",
    Dependents="0.0",
    Education="Graduate",
    Self_Employed="No",
    ApplicantIncome="2900",
    CoapplicantIncome="0.0",
    LoanAmount="71.0",
    Loan_Amount_Term="360.0",
    Credit_History="1.0",
    Property_Area="Rural",
    raw_request=False
):

    message_id = str(uuid.uuid4())

    # First, get the loan status

    sql_query_1 = f"""
    SELECT Loan_Status 
        FROM mindsdb.loan_approval_predictor 
        WHERE Gender = "{Gender}"
        AND Married = "{Married}"
        AND Dependents = "{Dependents}"
        AND Education = "{Education}"
        AND Self_Employed = "{Self_Employed}"
        AND ApplicantIncome = "{ApplicantIncome}"
        AND CoapplicantIncome = "{CoapplicantIncome}"
        AND LoanAmount = "{LoanAmount}"
        AND Loan_Amount_Term = "{Loan_Amount_Term}"
        AND Credit_History = "{Credit_History}"
        AND Property_Area = "{Property_Area}";
        """
    response = mindsdb_query(MINDSDB_QUERY_ENDPOINT, sql_query_1)
    loan_status = response.json()['data'][0][0]

    subject = 'Loan Approved' if loan_status == 'Y' else 'Loan Rejected'
    body = 'Congratulations! Your loan has been approved.' if loan_status == 'Y' else 'We regret to inform you that your loan application has been rejected.'

    # Based on the Loan_Status send mail to the provided email

    sql_query_2 = f"""
    INSERT INTO my_gmail.emails (message_id, to_email, subject, body)
     VALUES ("{message_id}", "{Email}", "Loan approval status", "{body}");
     """
    
    # Automate this whole process using Mindsdb Job Statement

    sql_query = f"""
    CREATE JOB loan_to_gmail (
     {sql_query_1} {sql_query_2}
    );
    """

    response = mindsdb_query(MINDSDB_QUERY_ENDPOINT, sql_query)

    return response


