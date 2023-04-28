import pandas as pd
import plotly.express as px

data = {'Method': ['Method 1', 'Method 2', 'Method 3', 'Method 4', 'Method 5', 'Method 6'], 'Accuracy': [0.85, 0.92, 0.78, 0.34, 0.78, 0.34]}
df = pd.DataFrame(data)

colors = px.colors.qualitative.Plotly[:len(df)]

fig = px.bar(df, x='Method', y='Accuracy', text=df['Accuracy'].apply(lambda x: f'{x:.2%}'), color=colors)
fig.update_traces(textposition='auto')
fig.update_layout(
    width=500, height=380, title='能力图谱分析', xaxis_title='', yaxis_title='准确率', showlegend=False
)
fig.write_image('plotly_4.png')
