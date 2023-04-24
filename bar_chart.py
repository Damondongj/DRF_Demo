import pandas as pd
import plotly.express as px

data = {'Method': ['Method 1', 'Method 2', 'Method 3'], 'Accuracy': [0.85, 0.92, 0.78]}
df = pd.DataFrame(data)

fig = px.bar(df, x='Method', y='Accuracy', text=df['Accuracy'].apply(lambda x: f'{x:.2%}'))
fig.update_traces(textposition='auto')
fig.update_layout(
    width=500, height=380, title='Method Comparison', xaxis_title='Methods', yaxis_title='Accuracy'
)
fig.write_image('method_comparison.png')
