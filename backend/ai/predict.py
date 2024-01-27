import json
import uuid
import asyncio
import requests

MINDSDB_QUERY_ENDPOINT = "http://127.0.0.1:47334/api/sql/query"


async def mindsdb_query(MINDSDB_QUERY_ENDPOINT, sql_query):
    headers = {"Content-Type": "application/json"}
    response = await asyncio.to_thread(requests.post, MINDSDB_QUERY_ENDPOINT, json={"query": sql_query}, headers=headers)
    return response


async def predict_loan_approval(
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

    sql_query_2 = f"""
    CREATE JOB loan_agent.status_to_mail (
    CREATE OR REPLACE TABLE test.saved_prediction (
        SELECT m.Loan_Status, m.Email, m.id
        FROM loan_agent.loan_approval_predictor AS m
        JOIN test.loan_data AS d
    );
    );
    """

    response = await mindsdb_query(MINDSDB_QUERY_ENDPOINT, sql_query_2)

    await asyncio.sleep(10)

    sql_query_3 = f"""
    SELECT  Loan_Status, id
    FROM test.saved_prediction
    ORDER BY id DESC
    LIMIT 1;
    """

    response = await mindsdb_query(MINDSDB_QUERY_ENDPOINT, sql_query_3)
    response_text =  response.text 
    response_data = json.loads(response_text) 
    print(response_data) 
    loan_status = response_data['data'][0][0]
    print(loan_status)

    # Prepare the context string with user data
    context_data = f"Email: {Email}, Gender: {Gender}, Married: {Married}, Dependents: {Dependents}, " \
                   f"Education: {Education}, Self_Employed: {Self_Employed}, ApplicantIncome: {ApplicantIncome}, " \
                   f"CoapplicantIncome: {CoapplicantIncome}, LoanAmount: {LoanAmount}, " \
                   f"Loan_Amount_Term: {Loan_Amount_Term}, Credit_History: {Credit_History}, " \
                   f"Property_Area: {Property_Area}"
    question = "The lender has declined the users loan. Now give suggestions briefly to improve the users loan approval chance based on the given user data. Dont use the user word instead use your"

    sql_query_suggestions = f"""
    SELECT answer
    FROM loan_agent.lendswift
    WHERE question='{question}'
    AND context='{context_data}';
    """
    
    if loan_status == 'Y':
     subject = 'Loan Aprroved'
     body = 'Congratulations! Your loan data has potential to be approved.'
    else:
          # Execute the query and get the response
     response_suggestions = await mindsdb_query(MINDSDB_QUERY_ENDPOINT, sql_query_suggestions)
    #  suggestions = json.loads(response_suggestions.text)['data'][0][0]
     suggestions = json.loads(response_suggestions.text)['data'][0][0]
     body = suggestions.replace('"', '\\"')

     
     subject = 'Loan Rejected'

    
   
       

    sql_query_4 = f"""
INSERT INTO my_gmail.emails (message_id, to_email, subject, body)
VALUES ("{message_id}", "{Email}", "{subject}", "{body}");
"""
    
    response = await mindsdb_query(MINDSDB_QUERY_ENDPOINT, sql_query_4)

    print(response.text)
    return response


