import pandas as pd

file = pd.read_csv('Articles.csv')
events = file.copy().loc[file['total_events']]
events = events.sort_values('total_events', ascending=True)
output = events[['title', 'total_events']].head(20)