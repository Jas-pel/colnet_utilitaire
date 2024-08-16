import plotly.graph_objects as go
from datetime import datetime

# Sample data
data = [
    "86.5% (2024-08-16 19:13:34)",
    "87.2% (2024-08-16 19:15:45)",
    "89.1% (2024-08-16 19:20:10)"
    # Add more data points here
]

# Step 1: Parse the data
values = []
timestamps = []

for entry in data:
    # Split the string to extract the percentage and timestamp
    value_str, time_str = entry.split(' (')
    value = float(value_str.rstrip('%'))
    timestamp = datetime.strptime(time_str.rstrip(')'), '%Y-%m-%d %H:%M:%S')
    
    values.append(value)
    timestamps.append(timestamp)

# Step 2: Plot the data using Plotly
fig = go.Figure()

# Add a scatter plot
fig.add_trace(go.Scatter(x=timestamps, y=values, mode='lines+markers', name='Percentage'))

# Customize the layout
fig.update_layout(
    title='Evolution of Numbers Over Time',
    xaxis_title='Time',
    yaxis_title='Percentage (%)',
    xaxis_tickformat='%Y-%m-%d %H:%M:%S',
    xaxis=dict(tickangle=-45),
    template='plotly_dark'
)

# Show the plot
fig.show()
