import pandas as pd
from typing import List
import plotly as py
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pandas.api.types import is_datetime64_any_dtype as is_datetime
import plotly.express as px
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


def timeseries(df: pd.DataFrame, date: str, measurement: str, title: str = "Time Series Plot", line_color: str = 'blue'):
    """
    Plots a time series graph using Plotly based on specified date and measurement columns in a DataFrame.

    Parameters:
    df (pd.DataFrame): DataFrame containing the data for the plot.
    date (str): Column name in `df` representing the date axis.
    measurement (str): Column name in `df` representing the measurement axis.
    title (str, optional): Title of the plot. Default is 'Time Series Plot'.
    line_color (str, optional): Color of the line in the plot. Default is 'blue'.

    Returns:
    None: Displays the plot directly using Plotly.
    """

    # Ensure the date column is in datetime format
    if not is_datetime(df[date]):
        df[date] = pd.to_datetime(df[date], infer_datetime_format=True, errors='coerce')

    # Create the figure
    fig = go.Figure([go.Scatter(x=df[date], y=df[measurement], line=dict(color=line_color))])
    fig.update_layout(title=title, xaxis_title=date, yaxis_title=measurement)
    fig.show()


def timeseries_slider_selector(df: pd.DataFrame, date: str, measurement: str, 
                                title: str = "Time Series Plot"):

    """
    Plots a time series graph with a range slider and range selector for easy navigation through time-based data.

    Parameters:
    df (pd.DataFrame): DataFrame containing the data for the plot.
    date (str): Column name in `df` representing the date axis.
    measurement (str): Column name in `df` representing the measurement axis.
    title (str, optional): Title of the plot. Default is 'Time Series Plot'.

    Returns:
    None: Displays the plot directly using Plotly.
    """

    # Ensure the date column is in datetime format
    if not is_datetime(df[date]):
        df[date] = pd.to_datetime(df[date], infer_datetime_format=True, errors='coerce')

    # Create the figure with range slider and selector
    fig = px.line(df, x=date, y=measurement, title=title)
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    fig.show()


def multi_timeseries(df: pd.DataFrame, date: str, measurements: List[str], 
                                title: str = "Time Series Plot"):

    """
    Plots a multi-measurement time series graph using Plotly. Each measurement is represented as a separate line.

    Parameters:
    df (pd.DataFrame): df (pd.DataFrame): DataFrame containing the data for the plot.
    date (str): Column name in `df` representing the date axis.
    measurements (List[str]): List of column names in `df` representing the multiple measurement axes.
    title (str, optional): Title of the plot. Default is 'Time Series Plot'.

    Returns:
    None: Directly displays the plot using Plotly.

    Raises:
    ValueError: If the specified columns do not exist in the DataFrame or if the date column is not in a proper date format.
    """
    # Ensure the date column is in datetime format
    if not is_datetime(df[date]):
        df[date] = pd.to_datetime(df[date], infer_datetime_format=True, errors='coerce')
    
    # Create the figure with multiple time series
    fig = px.line(df, x=date, y=measurements, hover_data={date: "|%B %d, %Y"}, title=title)

    # Update x-axis formatting
    fig.update_xaxes(dtick="M1", tickformat="%b\n%Y")

    # Display the figure
    fig.show()


def ohlc_chart(df: pd.DataFrame, date: str, open: str, high: str, low: str, close: str, volume: str):
    """
    Plots an OHLC (Open, High, Low, Close) chart using Plotly, suitable for financial data analysis.

    Parameters:
    df (pd.DataFrame): DataFrame containing the OHLC data.
    date (str): Column name in `df` representing the dates.
    open (str): Column name in `df` representing the opening prices.
    high (str): Column name in `df` representing the highest prices.
    low (str): Column name in `df` representing the lowest prices.
    close (str): Column name in `df` representing the closing prices.
    volume (str): Column name in `df` representing the trading volume

    Returns:
    None: Directly displays the OHLC chart using Plotly.
    """

    # Ensure the date column is in datetime format
    if not is_datetime(df[date]):
        df[date] = pd.to_datetime(df[date], infer_datetime_format=True, errors='coerce')

    fig = make_subplots(rows=2, cols=1)

    #OHLC Plot
    fig.add_trace(go.Ohlc(x=df[date], open=df[open], high=df[high], low=df[low], close=df[close], name='Price'), row=1, col=1)
    #Volume PLot
    fig.add_trace(go.Scatter(x=df[date], y=df[volume], name='Volume'), row=2, col=1)

    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.show()


def candlestick_chart(df: pd.DataFrame, date: str, open: str, high: str, low: str, close: str):
    """
    Plots a candlestick chart using Plotly, typically used for financial data analysis to visualize price movements.

    Parameters:
    df (pd.DataFrame): DataFrame containing the data for the candlestick chart.
    date (str): Column name in `df` representing the dates.
    open (str): Column name in `df` representing the opening prices.
    high (str): Column name in `df` representing the highest prices during the period.
    low (str): Column name in `df` representing the lowest prices during the period.
    close (str): Column name in `df` representing the closing prices.

    Returns:
    None: Directly displays the candlestick chart using Plotly.
    """

    # Ensure the date column is in datetime format
    if not is_datetime(df[date]):
        df[date] = pd.to_datetime(df[date], infer_datetime_format=True, errors='coerce')

    # Create and display the candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=df[date], open=df[open], high=df[high], low=df[low], close=df[close])])
    fig.show()


def plot_moving_averages(df: pd.DataFrame, date_col: str, close_col: str):
    """
    Plots Exponential Moving Averages (EMA) and Simple Moving Averages (SMA) along with the closing price using Plotly.

    Parameters:
    df (pd.DataFrame): DataFrame containing the data for the plot. Must include 'Date' and 'Close' columns.
    date_col (str): Column name in `df` representing the date axis.
    close_col (str): Column name in `df` representing the closing price.

    Returns:
    None: Directly displays the plot using Plotly.

    Note:
    The function calculates and plots EMA for 9 and 22 periods and SMA for 5, 10, 15, and 30 periods.
    The closing price is plotted for reference, with lower opacity.
    """

    # Ensure the date column is in datetime format
    if not is_datetime(df[date_col]):
        df[date_col] = pd.to_datetime(df[date_col], infer_datetime_format=True, errors='coerce')

    # Calculate EMA and SMA
    df['EMA_9'] = df[close_col].ewm(9).mean().shift()
    df['EMA_22'] = df[close_col].ewm(22).mean().shift()
    df['SMA_5'] = df[close_col].rolling(5).mean().shift()
    df['SMA_10'] = df[close_col].rolling(10).mean().shift()
    df['SMA_15'] = df[close_col].rolling(15).mean().shift()
    df['SMA_30'] = df[close_col].rolling(30).mean().shift()

    # Create and display the plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[date_col], y=df['EMA_9'], name='EMA 9'))
    fig.add_trace(go.Scatter(x=df[date_col], y=df['EMA_22'], name='EMA 22'))
    fig.add_trace(go.Scatter(x=df[date_col], y=df['SMA_5'], name='SMA 5'))
    fig.add_trace(go.Scatter(x=df[date_col], y=df['SMA_10'], name='SMA 10'))
    fig.add_trace(go.Scatter(x=df[date_col], y=df['SMA_15'], name='SMA 15'))
    fig.add_trace(go.Scatter(x=df[date_col], y=df['SMA_30'], name='SMA 30'))
    fig.add_trace(go.Scatter(x=df[date_col], y=df[close_col], name='Close', opacity=0.3))
    
    fig.show()


def plot_rsi(df: pd.DataFrame, date_col: str, close_col: str, n: int = 14):
    """
    Calculates and plots the Relative Strength Index (RSI) using Plotly.

    The RSI is a momentum oscillator that measures the speed and change of price movements.

    Parameters:
    df (pd.DataFrame): DataFrame containing the data for the calculation. Must include 'Date' and 'Close' columns.
    date_col (str): Column name in `df` representing the date axis.
    close_col (str): Column name in `df` representing the closing price.
    n (int, optional): The number of periods to use for RSI calculation. Default is 14.

    Returns:
    None: Directly displays the RSI plot using Plotly.

    Note:
    The RSI value ranges from 0 to 100. Typically, an RSI above 70 indicates that a security is overbought, while an RSI below 30 indicates oversold conditions.
    """

    # Ensure the date column is in datetime format
    if not is_datetime(df[date_col]):
        df[date_col] = pd.to_datetime(df[date_col], infer_datetime_format=True, errors='coerce')

    # RSI calculation
    delta = df[close_col].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=n, min_periods=0).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=n, min_periods=0).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    # Create and display the RSI plot
    fig = go.Figure(go.Scatter(x=df[date_col], y=rsi, name='RSI'))
    fig.show()


def plot_macd(df: pd.DataFrame, date_col: str, close_col: str):
    """
    Calculates and plots the Moving Average Convergence Divergence (MACD) and its signal line along with the closing price.

    MACD is a trend-following momentum indicator that shows the relationship between two moving averages of a security’s price.

    Parameters:
    df (pd.DataFrame): DataFrame containing the data for the calculation. Must include 'Date' and 'Close' columns.
    date_col (str): Column name in `df` representing the date axis.
    close_col (str): Column name in `df` representing the closing price.

    Returns:
    None: Directly displays the MACD plot using Plotly.

    Note:
    The MACD line is calculated as the difference between the 12-period and 26-period Exponential Moving Averages (EMA). 
    The signal line is the 9-period EMA of the MACD line. The plot includes the closing price for reference.
    """

    # Ensure the date column is in datetime format
    if not is_datetime(df[date_col]):
        df[date_col] = pd.to_datetime(df[date_col], infer_datetime_format=True, errors='coerce')

    # Calculate EMA 12, EMA 26, MACD, and MACD signal
    EMA_12 = df[close_col].ewm(span=12, min_periods=12).mean()
    EMA_26 = df[close_col].ewm(span=26, min_periods=26).mean()
    df['MACD'] = EMA_12 - EMA_26
    df['MACD_signal'] = df['MACD'].ewm(span=9, min_periods=9).mean()

    # Create and display the MACD plot
    fig = make_subplots(rows=2, cols=1)
    fig.add_trace(go.Scatter(x=df[date_col], y=df[close_col], name='Close'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df[date_col], y=EMA_12, name='EMA 12'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df[date_col], y=EMA_26, name='EMA 26'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df[date_col], y=df['MACD'], name='MACD'), row=2, col=1)
    fig.add_trace(go.Scatter(x=df[date_col], y=df['MACD_signal'], name='Signal line'), row=2, col=1)
    fig.show()


def plot_waterfall(x_labels: list, y_values: list, text_labels: list, title: str = "Profit and Loss"):
    """
    Creates and displays a waterfall chart using Plotly, typically used for financial analysis to show changes in metrics.

    Parameters:
    x_labels (list): A list of strings representing the categories or stages in the waterfall chart.
    y_values (list): A list of numerical values corresponding to each category or stage. Positive values represent increases, and negative values represent decreases.
    text_labels (list): A list of strings for annotations on each bar. Should correspond to the values in `y_values`.
    title (str, optional): Title of the plot. Default is "Profit and Loss".

    Returns:
    None: Directly displays the waterfall chart using Plotly.

    """

    # Constructing the measure list
    measure = ['relative'] * (len(x_labels) - 1) + ['total']

    # Create and display the waterfall chart
    fig = go.Figure(go.Waterfall(
        name = "20", orientation = "v",
        measure = measure,
        x = x_labels,
        textposition = "outside",
        text = text_labels,
        y = y_values,
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
    ))

    fig.update_layout(title = title, showlegend = True)

    fig.show()


def plot_funnel_chart(data: pd.DataFrame, x_col: str, y_col: str, title: str = "Funnel Chart"):
    """
    Creates and displays a funnel chart using Plotly Express, ideal for representing stages in a process or pipeline.

    Parameters:
    data (pd.DataFrame): A dictionary with keys representing column names and values as lists of data points. 
                 It should contain data for both 'x' and 'y' axes of the funnel chart.
    x_col (str): The column from data to be used as values (quantitative axis) of the funnel.
    y_col (str): The column from data to be used as stages (qualitative axis) of the funnel.
    title (str, optional): Title of the plot. Default is "Funnel Chart".

    Returns:
    None: Directly displays the funnel chart using Plotly Express.
    """

    # Create and display the funnel chart
    fig = px.funnel(data, x=x_col, y=y_col)
    fig.update_layout(title=title)
    fig.show()


def plot_pie_chart(labels: list, values: list, title: str = "Pie Chart"):
    """
    Creates and displays a pie chart using Plotly, suitable for showing the composition of a dataset.

    Parameters:
    labels (list): A list of labels for each segment of the pie chart.
    values (list): A list of values corresponding to each label. These values determine the size of each pie segment.
    title (str, optional): Title of the pie chart. Default is "Pie Chart".

    Returns:
    None: Directly displays the pie chart using Plotly.
    """

    # Create and display the pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent', insidetextorientation='radial')])
    fig.update_layout(title=title)
    fig.show()