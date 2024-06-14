import pandas as pd
import plotly.graph_objs as go
from scipy import stats

def remove_outliers(df, column_name, z_threshold=3):
    """
    Remove rows with outlier values in a specific column of a DataFrame using the Z-score method.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    column_name (str): The name of the column to check for outliers.
    z_threshold (float): The Z-score threshold to identify outliers. Default is 3.

    Returns:
    pd.DataFrame: DataFrame with outliers removed.
    """
    # Calculate the Z-scores of the specified column
    z_scores = stats.zscore(df[column_name])

    # Create a boolean mask to filter out rows with Z-scores above the threshold
    mask = abs(z_scores) < z_threshold

    # Apply the mask to the DataFrame
    df_no_outliers = df[mask]

    return df_no_outliers

def plot_results(item_name, offer_type, fig, row, col, folder_name, colors=None):
    if colors is None:
        colors = {'stock_price': 'blue', 'vwap': 'orange', 'volume': 'red', 'new_offers': 'lightgreen'}

    df_disappeared = pd.read_csv(f'results/analyzed/{folder_name}_{item_name}_{offer_type}_disappeared_offers.csv')
    df_newoffers = pd.read_csv(f'results/analyzed/{folder_name}_{item_name}_{offer_type}_new_offers.csv')
    df_newoffers['time'] = pd.to_datetime(df_newoffers['cur_time'])
    df_newoffers = df_newoffers.loc[df_newoffers['order_n'].isin([0, 1])]
    df_newoffers = df_newoffers[df_newoffers['quantity'] < 100000]
    df_newoffers = remove_outliers(df_newoffers, 'quantity')

    filtered_df = df_disappeared.loc[df_disappeared['order_n'].isin([0])]
    filtered_df = filtered_df.copy()  # Avoid SettingWithCopyWarning
    #filtered_df['delta_quantity'] = -filtered_df['quantity']
    filtered_df['source'] = 'disappeared'

    df_quant = pd.read_csv(f'results/analyzed/{folder_name}_{item_name}_{offer_type}_quantity_changes.csv')
    df_quant = df_quant.loc[df_quant['delta_quantity'] < 0]
    df_quant = df_quant.copy()  # Avoid SettingWithCopyWarning
    df_quant['source'] = 'changed'

    df = pd.concat([filtered_df, df_quant])

    df = remove_outliers(df, 'prices')

    # Convert timestamp to datetime
    df['time'] = pd.to_datetime(df['cur_time'])
    df = df.sort_values(by='time')
    df['cur_time'] = pd.to_datetime(df['cur_time'])
    df['volume'] = abs(df['delta_quantity'])

    df['price_volume'] = df['prices'] * df['volume']

    cumulative_price_volume = df['price_volume'].cumsum()
    cumulative_volume = df['volume'].cumsum()
    df['vwap'] = cumulative_price_volume / cumulative_volume
    df = df[df['prices'] < 1000000]
    df = df[df['prices'] > 1000]

    # Add stock price trace
    fig.add_trace(
        go.Scatter(x=df['time'], y=df['prices'], mode='lines', name='Item Price',
                   line=dict(color=colors['stock_price'])),
        row=row, col=col, secondary_y=False,
    )

    # Add VWAP trace
    fig.add_trace(
        go.Scatter(x=df['time'], y=df['vwap'], mode='lines', name='VWAP', line=dict(dash='dash', color=colors['vwap'])),
        row=row, col=col, secondary_y=False,
    )

    # Add volume bars
    fig.add_trace(
        go.Bar(x=df['time'], y=df['volume'], name='Volume', opacity=1, marker=dict(color=colors['volume'])),
        row=row, col=col, secondary_y=True,
    )

    # Add new offers bars
    fig.add_trace(
        go.Bar(x=df_newoffers['time'], y=df_newoffers['quantity'], name='New Offers', opacity=1,
               marker=dict(color=colors['new_offers'])),
        row=row, col=col, secondary_y=True,
    )

    # Update x and y axes for every subplot
    fig.update_xaxes(title_text='Time', title_font=dict(size=18), tickfont=dict(size=14), row=row, col=col)
    fig.update_yaxes(title_text='Price', title_font=dict(size=18), tickfont=dict(size=14), row=row, col=col,
                     secondary_y=False)
    fig.update_yaxes(title_text='Volume', title_font=dict(size=18), tickfont=dict(size=14), row=row, col=col,
                     secondary_y=True)

    df.to_csv(f'results/analyzed/plotted/{folder_name}_{item_name}_{offer_type}_plotted.csv', index=False)
