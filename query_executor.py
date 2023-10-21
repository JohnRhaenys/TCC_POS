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


def execute_query(query, output_file):
    db = connect_to_db()
    df = pd.read_sql(query, con=db)
    df.to_csv(output_file, index=False)
    db.close()
