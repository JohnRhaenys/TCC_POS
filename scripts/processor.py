import pandas as pd
from src.helpers.utils import save_dataframe_to_csv, save_dataframe_to_xlsx
import os

PROCESSED_CSV_PATH = os.path.join(os.getcwd(), '..\\data\\processed\\processed.csv')
PROCESSED_XLSX_PATH = os.path.join(os.getcwd(), '..\\data\\processed\\processed.xlsx')


def join_data(critical_dates, ruptures, stock_count):
    print('Joining critical dates and ruptures ...')
    critical_dates = critical_dates.rename(columns={
        'quantidade': 'quantidadeDataCritica',
        'medida': 'medidaDataCritica',
        'lote': 'loteDataCritica'
    })
    stock_count = stock_count.rename(columns={
        'quantidade': 'quantidadeEstoque',
        'medida': 'medidaQuantidadeEstoque'
    })

    crit_rup = pd.merge(
        critical_dates,
        ruptures,
        on=['dataRegistroResposta', 'productId', 'storeId'],
        how='inner'
    )

    print('Joining critical dates, ruptures and stock count ...')
    result = pd.merge(
        crit_rup,
        stock_count,
        on=['dataRegistroResposta', 'productId', 'storeId'],
        how='inner'
    )
    result = result.drop_duplicates()
    desired_columns = ['productId', 'nomeProduto', 'nomeMarca', 'cnpjIndustria',
                       'razaoSocialIndustria', 'nomeFantasiaIndustria',
                       'dataRegistroResposta', 'quantidadeEstoque',
                       'medidaQuantidadeEstoque', 'dataCritica',
                       'quantidadeDataCritica', 'medidaDataCritica',
                       'loteDataCritica', 'storeId', 'nomeLoja',
                       'nomeBandeira', 'nomeRede']
    result = result[desired_columns]
    return result


def write_duplicated_rows_to_csv(dataframe, output_path):
    duplicate_rows = dataframe[dataframe.duplicated(keep=False)]
    if not duplicate_rows.empty:
        duplicate_rows.to_csv(output_path, index=False)


def filter_data(joined_data):
    filtered_data = joined_data.loc[joined_data['nomeBandeira'] != 'Bandeira Treinamento']
    return filtered_data


def process_data(critical_dates, ruptures, stock_count):
    print('Processing data ...')
    joined_data = join_data(critical_dates, ruptures, stock_count)
    filtered_joined_data = filter_data(joined_data)
    print('Saving joined dataframe to csv ...')
    save_dataframe_to_csv(dataframe=filtered_joined_data, output_path=PROCESSED_CSV_PATH)
    print('Dataframe successfully saved to csv!')
    print('Saving joined dataframe to xlsx ...')
    save_dataframe_to_xlsx(dataframe=filtered_joined_data, output_path=PROCESSED_XLSX_PATH)
    print('Dataframe successfully saved to xlsx!')
