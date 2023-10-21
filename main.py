from queries import CRITICAL_DATES_QUERY, RUPTURE_QUERY, STOCK_COUNT_QUERY
from query_executor import execute_query


def main():
    execute_query(query=CRITICAL_DATES_QUERY, output_file='critical_dates.csv')
    execute_query(query=RUPTURE_QUERY, output_file='ruptures.csv')
    execute_query(query=STOCK_COUNT_QUERY, output_file='stock_count.csv')


if __name__ == "__main__":
    main()
