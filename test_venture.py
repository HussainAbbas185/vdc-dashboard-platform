
import pandas as pd
import altair as alt
from src.startup_data import get_high_growth_startups

df_startups = get_high_growth_startups()
print("Data fetched successfully")
print(df_startups.columns)

avg_equity = df_startups['equity'].mean()
high_skill_firms = len(df_startups[df_startups['skill_index'] > 0.9])
total_valuation = df_startups['equity'].sum()
top_sector = df_startups['sector'].mode()[0]
print("Metrics calculated successfully")

hubs = df_startups['hq'].apply(lambda x: x.split(', ')[1]).value_counts().reset_index()
print("Hubs calculated successfully")
print(hubs)
hubs.columns = ['state', 'count']
print("Columns assigned successfully")
