import pandas as pd
import numpy as np



def concatenate_dataframes_with_padding(dfs):

    """
    Concatenate a list of dataframes vertically, ensuring that all dataframes have the same number of rows.
    If a dataframe has fewer rows, it is padded with NaNs.

    :param dfs: List of pandas DataFrames to concatenate
    :return: Concatenated DataFrame
    """
    # Determine the maximum number of rows in any of the dataframes
    max_rows = max(df.shape[0] for df in dfs)

    # Function to pad dataframe with NaNs to match the max number of rows
    def pad_df(df):

        rows_to_add = max_rows - df.shape[0]
        
        if rows_to_add > 0:
            # Create a DataFrame of NaNs with the required number of rows and columns
            padding_df = pd.DataFrame(np.nan, index=range(rows_to_add), columns=df.columns)
            # Use concat instead of append
            return pd.concat([df, padding_df], ignore_index=True)
        
        else:
            return df

    # Pad each dataframe and concatenate them
    padded_dfs = [pad_df(df) for df in dfs]
    concatenated_df = pd.concat(padded_dfs, axis=1)

    return concatenated_df
