import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# Read the CSV file
df = pd.read_csv('youtubecleaned.csv')

# 1. Genre Distribution
genre_views = df.groupby('genre')['views'].sum().sort_values(ascending=False)
genre_percentages = (genre_views / genre_views.sum() * 100).round(2)

# 2. Top 10 Videos
top_10_videos = df.nlargest(10, 'views')[['title', 'channel_title', 'views']]

# 3. Views vs. Likes Correlation
views_likes_corr = df['views'].corr(df['likes'])

# 4. Category Distribution
category_counts = df['category_id'].value_counts()

# 5. Time Series of Video Uploads
df['publish_date'] = pd.to_datetime(df['publish_time']).dt.date
video_uploads = df.groupby('publish_date').size().reset_index(name='count')

# Create the dashboard
fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=("Genre Distribution", "Top 10 Videos by Views", 
                    "Views vs. Likes Scatter Plot", "Category Distribution",
                    "Time Series of Video Uploads", "Views vs. Likes Correlation"),
    specs=[[{"type": "pie"}, {"type": "bar"}],
           [{"type": "scatter"}, {"type": "bar"}],
           [{"type": "scatter"}, {"type": "indicator"}]]
)

# 1. Genre Distribution
fig.add_trace(go.Pie(labels=genre_percentages.index[:5], values=genre_percentages.values[:5], name="Genre Distribution"),
              row=1, col=1)

# 2. Top 10 Videos
fig.add_trace(go.Bar(x=top_10_videos['views'], y=top_10_videos['title'], orientation='h', name="Top 10 Videos"),
              row=1, col=2)

# 3. Views vs. Likes Scatter Plot
fig.add_trace(go.Scatter(x=df['views'], y=df['likes'], mode='markers', name="Views vs. Likes"),
              row=2, col=1)

# 4. Category Distribution
fig.add_trace(go.Bar(x=category_counts.index, y=category_counts.values, name="Category Distribution"),
              row=2, col=2)

# 5. Time Series of Video Uploads
fig.add_trace(go.Scatter(x=video_uploads['publish_date'], y=video_uploads['count'], mode='lines', name="Video Uploads"),
              row=3, col=1)

# 6. Views vs. Likes Correlation
fig.add_trace(go.Indicator(
    mode = "gauge+number",
    value = views_likes_corr,
    title = {'text': "Correlation"},
    gauge = {'axis': {'range': [-1, 1]},
             'steps' : [
                 {'range': [-1, -0.5], 'color': "lightgray"},
                 {'range': [-0.5, 0.5], 'color': "gray"},
                 {'range': [0.5, 1], 'color': "darkgray"}],
             'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': views_likes_corr}}),
    row=3, col=2)

# Update layout
fig.update_layout(height=1200, width=1000, title_text="YouTube Data Dashboard")
fig.update_xaxes(title_text="Views", row=2, col=1)
fig.update_yaxes(title_text="Likes", row=2, col=1)
fig.update_xaxes(title_text="Category ID", row=2, col=2)
fig.update_yaxes(title_text="Count", row=2, col=2)
fig.update_xaxes(title_text="Date", row=3, col=1)
fig.update_yaxes(title_text="Number of Uploads", row=3, col=1)

# Save the dashboard as an HTML file
fig.write_html("youtube_dashboard.html")

print("Dashboard has been created and saved as 'youtube_dashboard.html'")

# Display some key statistics
print("\
Key Statistics:")
print(f"Total number of videos: {len(df)}")
print(f"Average views per video: {df['views'].mean():,.2f}")
print(f"Average likes per video: {df['likes'].mean():,.2f}")
print(f"Average dislikes per video: {df['dislikes'].mean():,.2f}")
print(f"Correlation between views and likes: {views_likes_corr:.2f}")