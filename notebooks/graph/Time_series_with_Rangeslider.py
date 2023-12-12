## Time Series with Rangeslider

import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

fig = px.line(df, x='Date', y='High', title='Time Series with Rangeslider')

fig.update_xaxes(rangeslider_visible=True)
fig.show()