from src.scripts.data_manager import get_data
from src.scripts.processor import process_data


def main():
    critical_dates, ruptures, stock_count = get_data()
    process_data(critical_dates, ruptures, stock_count)


if __name__ == "__main__":
    main()
