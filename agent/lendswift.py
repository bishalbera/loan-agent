import requests
from backend.env import config

MINDSDB_QUERY_ENDPOINT = "http://127.0.0.1:47334/api/sql/query"


def mindsdb_query(MINDSDB_QUERY_ENDPOINT, sql_query):
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(MINDSDB_QUERY_ENDPOINT, json={
                                 "query": sql_query}, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the HTTP request: {str(e)}")
        return None


API_KEY = config("API_KEY")

def create_model():

    sql_query = f"""
CREATE MODEL my_model
PREDICT answer
USING
    engine = 'langchain_engine',
    question_column = 'question',
    api_key = '{API_KEY}', 
    user_column = 'question' ,
    assistant_column = 'answer',
    model_name='gpt-3.5-turbo', 
    verbose=true,
    mode = 'conversational',
    prompt_template='
Hi there, LendSwift here! <assume that you are a lender who can predict loan status using a simple decision making algorithm . user will give some data based on that you have to predict his loan status(dont need to think of some other factors). if your prediction says loan status will be approved then reply with " Congratulations! Your loan application has potential to be approved." or else reply with "We regret to inform you that your loan data lacks potential to be approved." providing cause for not approving and giving some suggestion what the user can improve. ';
"""
    res = mindsdb_query(MINDSDB_QUERY_ENDPOINT, sql_query)
    if res is not None:
        if res.status_code == 200:
            print("Model created successfully")
        else:
            print(
                f"Failed to create model. HTTP status code: {res.status_code}")
    else:
        print("Failed to create model. No response received.")

    create_model()

def create_skill():

    sql_query = f"""
CREATE SKILL loan_skill
    USING
    type = 'text_to_sql',
    database = 'test', 
    tables = ['loan_data'];
    """
    res = mindsdb_query(MINDSDB_QUERY_ENDPOINT, sql_query)
    if res is not None:
        if res.status_code == 200:
            print("Skill created successfully")
        else:
            print(
                f"Failed to create skill. HTTP status code: {res.status_code}")
    else:
        print("Failed to create skill. No response received.")


    create_skill()

def create_agent():

    sql_query = f"""
CREATE AGENT my_loan_agent
USING
   model = 'my_model',
   skills = ['loan_skill'];
   """
    res = mindsdb_query(MINDSDB_QUERY_ENDPOINT, sql_query)
    if res is not None:
        if res.status_code == 200:
            print("Agent created successfully")
        else:
            print(
                f"Failed to create agent. HTTP status code: {res.status_code}")
    else:
        print("Failed to create agent. No response received.")

create_agent()

def create_chatbot():

    sql_query = f"""
CREATE CHATBOT lendswift_chatbot
USING
    database = 'mindsdb_slack', 
    agent = 'my_loan_agent', 
    enable_dms = true;
    """

    res = mindsdb_query(MINDSDB_QUERY_ENDPOINT, sql_query)
    if res is not None:
        if res.status_code == 200:
            print("Chatbot created successfully")
        else:
            print(
                f"Failed to create chatbot. HTTP status code: {res.status_code}")

    else:
        print("Failed to create chatbot. No response received.")
create_chatbot()