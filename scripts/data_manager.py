import os
import pandas as pd

from src.database.queries import CRITICAL_DATES_QUERY, RUPTURE_QUERY, STOCK_COUNT_QUERY
from src.database.query_executor import execute_query
from src.helpers.utils import save_dataframe_to_csv

CRITICAL_DATES_CSV_PATH = os.path.join(os.getcwd(), '..\\data\\raw\\critical_dates.csv')
RUPTURES_CSV_PATH = os.path.join(os.getcwd(), '..\\data\\raw\\ruptures.csv')
STOCK_COUNT_CSV_PATH = os.path.join(os.getcwd(), '..\\data\\raw\\stock_count.csv')


def files_exist():
    return (
            os.path.exists(CRITICAL_DATES_CSV_PATH) and
            os.path.exists(RUPTURES_CSV_PATH) and
            os.path.exists(STOCK_COUNT_CSV_PATH)
    )


def get_data_from_csv():
    print('Reading critical dates from csv ...')
    critical_dates = pd.read_csv(CRITICAL_DATES_CSV_PATH)
    print('Reading ruptures from csv ...')
    ruptures = pd.read_csv(RUPTURES_CSV_PATH)
    print('Reading stock count from csv ...')
    stock_count = pd.read_csv(STOCK_COUNT_CSV_PATH)
    print('Data successfully read from csv files!')
    return critical_dates, ruptures, stock_count


def get_data():
    if files_exist():
        critical_dates, ruptures, stock_count = get_data_from_csv()
    else:
        print('Executing critical dates query ...')
        critical_dates = execute_query(query=CRITICAL_DATES_QUERY)
        print(f'Critical dates query successfully executed! {len(critical_dates)} results returned.')
        print('Saving critical dates to csv file ...')
        save_dataframe_to_csv(
            dataframe=critical_dates,
            output_path=CRITICAL_DATES_CSV_PATH
        )
        print('Critical dates saved successfully to csv file!')
        print('Executing ruptures query ...')
        ruptures = execute_query(query=RUPTURE_QUERY)
        print(f'Ruptures query successfully executed! {len(ruptures)} results returned.')
        print('Saving ruptures to csv file ...')
        save_dataframe_to_csv(
            dataframe=ruptures,
            output_path=RUPTURES_CSV_PATH
        )
        print('Ruptures saved successfully to csv file!')
        print('Executing stock_count query ...')
        stock_count = execute_query(query=STOCK_COUNT_QUERY)
        print(f'Stock count query successfully executed! {len(stock_count)} results returned.')
        print('Saving stock count to csv file ...')
        save_dataframe_to_csv(
            dataframe=stock_count,
            output_path=STOCK_COUNT_CSV_PATH
        )
        print('Stock count saved successfully to csv file!')

    return critical_dates, ruptures, stock_count
