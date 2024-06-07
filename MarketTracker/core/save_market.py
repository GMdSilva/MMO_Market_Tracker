import pandas as pd


def read_and_append_unique(item_name, folder_name):

    """
    Reads a dataframe from disk and appends new rows to it if there are no duplicates in specified columns.

    Parameters:
    file_path (str): The path to the CSV file to read and write.
    new_data (pd.DataFrame): The new data to append.
    key_columns (list): The columns to check for duplicates.

    Returns:
    pd.DataFrame: The updated dataframe.
    """

    for offer_type in ['ask', 'bid']:
        # Read the existing dataframe from the file
        new_data = pd.read_csv(f'results/{folder_name}/{item_name}/{offer_type}_instant.csv')
        try:
            df_existing = pd.read_csv(f'results/{folder_name}/{item_name}/{offer_type}_base.csv')
            updated_data = df_existing.copy()
            scan_n = updated_data['scan'].iloc[-1]
        except FileNotFoundError:
            df_existing = new_data  # If file does not exist, create an empty dataframe
            df_existing['scan'] = 1
            updated_data = new_data.copy()
            scan_n = 1

        # Append the new data
        new_data['scan'] = scan_n + 1
        combined_data = pd.concat([updated_data, new_data])

        # Write the updated dataframe back to the file
        combined_data.to_csv(f'results/{folder_name}/{item_name}/{offer_type}_base.csv', index=False)
