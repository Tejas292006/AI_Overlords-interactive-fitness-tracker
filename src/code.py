import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

data = pd.read_csv("/kaggle/input/fitbit/mturkfitbit_export_3.12.16-4.11.16/Fitabase Data 3.12.16-4.11.16/dailyActivity_merged.csv")

print("\nFirst 5 rows of the dataset:\n", data.head())
print("\nMissing Values in Each Column:\n", data.isnull().sum())
print("\nDataset Info:\n")
data.info()


# Changing datatype of ActivityDate
data["ActivityDate"] = pd.to_datetime(data["ActivityDate"], 
                                      format="%m/%d/%Y")
print(data.info())


data["TotalMinutes"] = (
    data["VeryActiveMinutes"] +
    data["FairlyActiveMinutes"] +
    data["LightlyActiveMinutes"] +
    data["SedentaryMinutes"]
)



data["Day"] = data["ActivityDate"].dt.day_name()


# Statistical summary of numeric columns
print("\nStatistical Summary:\n", data.describe())



# Visualization 1: Relationship between Calories and Total Steps
scatter_fig = px.scatter(
    data_frame=data, 
    x="Calories", 
    y="TotalSteps", 
    size="VeryActiveMinutes", 
    trendline="ols", 
    title="Relationship between Calories & Total Steps"
)
scatter_fig.show()



# Visualization 2: Breakdown of Active Minutes
active_labels = ["Very Active Minutes", "Fairly Active Minutes", "Lightly Active Minutes", "Inactive Minutes"]
active_counts = data[["VeryActiveMinutes", "FairlyActiveMinutes", "LightlyActiveMinutes", "SedentaryMinutes"]].mean()
colors = ['gold', 'lightgreen', 'pink', 'blue']

active_pie_fig = go.Figure(data=[
    go.Pie(labels=active_labels, values=active_counts, marker=dict(colors=colors, line=dict(color='black', width=2)))
])
active_pie_fig.update_layout(title_text="Total Active Minutes")
active_pie_fig.show()



# Visualization 3: Active Minutes by Day of the Week
bar_fig = go.Figure()
bar_fig.add_trace(go.Bar(x=data["Day"], y=data["VeryActiveMinutes"], name='Very Active', marker_color='purple'))
bar_fig.add_trace(go.Bar(x=data["Day"], y=data["FairlyActiveMinutes"], name='Fairly Active', marker_color='green'))
bar_fig.add_trace(go.Bar(x=data["Day"], y=data["LightlyActiveMinutes"], name='Lightly Active', marker_color='pink'))
bar_fig.update_layout(
    barmode='group', 
    title_text="Active Minutes by Day of the Week",
    xaxis_tickangle=-45
)
bar_fig.show()


# Visualization 4: Sedentary Minutes Distribution by Day
sedentary_pie_fig = go.Figure(data=[
    go.Pie(labels=data["Day"].value_counts().index, values=data["SedentaryMinutes"], 
           marker=dict(colors=colors, line=dict(color='black', width=2)))
])
sedentary_pie_fig.update_layout(title_text="Inactive Minutes by Day")
sedentary_pie_fig.show()



# Visualization 5: Calories Burned by Day
calories_pie_fig = go.Figure(data=[
    go.Pie(labels=data["Day"].value_counts().index, values=data["Calories"], 
           marker=dict(colors=colors, line=dict(color='black', width=2)))
])
calories_pie_fig.update_layout(title_text="Calories Burned by Day")
calories_pie_fig.show()