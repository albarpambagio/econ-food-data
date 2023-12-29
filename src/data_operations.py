# data_operations.py

import pandas as pd

def tidy_operations(data):
    """
    Perform tidy operations on the data.

    This function extracts a subset of columns with mixed data types and prints the count of unique data types for each column.

    Parameters:
    - data (pd.DataFrame): Input data.

    Returns:
    - pd.DataFrame: Tidied data.
    """
    try:
        mixed_type_columns = data.iloc[:, [4, 5, 12, 13]]
        print(mixed_type_columns.applymap(type).nunique())
        return data
    except Exception as e:
        raise Exception(f"Error during tidy operations: {str(e)}") from e

def preprocess_data(data):
    """
    Preprocess the data.

    This function handles data cleaning tasks such as converting columns to appropriate data types, extracting date components,
    dropping unnecessary columns, handling missing values, and updating column names.

    Parameters:
    - data (pd.DataFrame): Input data.

    Returns:
    - pd.DataFrame: Preprocessed data.
    """
    try:
        data['price'] = pd.to_numeric(data['price'], errors='coerce')
        data['date'] = pd.to_datetime(data['date'], errors='coerce', format='%Y-%m-%d')
        data = data.assign(
            data_year=data['date'].dt.year,
            data_month=data['date'].dt.month,
            data_day=data['date'].dt.day
        )
        data = data.drop(['admin1', 'admin2', 'latitude', 'longitude', 'usdprice'], axis=1).copy()
        data = data.drop(data.index[0])
        data = data.rename(columns={'data_year': 'year', 'data_month': 'month', 'data_day': 'day'})
        categorical_columns = ['market', 'category', 'commodity', 'unit', 'priceflag', 'pricetype', 'currency']
        data[categorical_columns] = data[categorical_columns].astype('category')
        data['priceflag'] = data['priceflag'].str.replace('#', '').astype('category')
        data['pricetype'] = data['pricetype'].str.replace('#', '').astype('category')
        data['priceflag'] = data['priceflag'].astype(str)
        data_info = data.info()
        data_duplicate = data.duplicated().sum()
        print(f"Number of duplicated rows: {data_duplicate}")
        data_info = data.columns
        print(data_info)
        return data
    except Exception as e:
        raise Exception(f"Error during data preprocessing: {str(e)}") from e