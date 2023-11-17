import pandas as pd
import mysql.connector as mysql
from decouple import config


def connect_to_db():
    return mysql.connect(
        host=config('DB_HOST'),
        user=config('DB_USER'),
        passwd=config('DB_PASS'),
        db=config('DB_NAME')
    )


def execute_query(query):
    db = connect_to_db()
    dataframe = pd.read_sql(query, con=db)
    db.close()
    return dataframe
