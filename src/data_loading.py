# data_loading.py

import pandas as pd

def load_data(csv_file_path):
    """
    Load data from a CSV file.

    Parameters:
    - csv_file_path (str): Path to the CSV file.

    Returns:
    - pd.DataFrame: Loaded data.

    Raises:
    - FileNotFoundError: If the specified file is not found.
    """
    
    try:
        data = pd.read_csv(csv_file_path, low_memory=False)
        return data
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {csv_file_path}") from e
    except Exception as e:
        raise Exception(f"Error loading data from {csv_file_path}: {str(e)}") from e
