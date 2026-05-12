"""Build all interactive visualizations for the website."""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

PATH = r'C:\Users\18356\Desktop\02806\socialdata2026\Shootings_(2006-Present)_20260420.csv'
raw = pd.read_csv(PATH)
df = raw.copy()
df['OCCUR_DATE'] = pd.to_datetime(df['OCCUR_DATE'])
df['YEAR']    = df['OCCUR_DATE'].dt.year
df['MONTH']   = df['OCCUR_DATE'].dt.month
df['WEEKDAY'] = df['OCCUR_DATE'].dt.day_name()
df['HOUR']    = pd.to_datetime(df['OCCUR_TIME'], format='%H:%M:%S', errors='coerce').dt.hour
df = df.drop(columns=['LOCATION_DESC', 'X_COORD_CD', 'Y_COORD_CD'])
df['LOC_CLASSFCTN_DESC'] = df['LOC_CLASSFCTN_DESC'].fillna('UNKNOWN')
invalid_geo = df['Latitude'].isna() | (df['Latitude'] == 0.0)
geo = df[~invalid_geo].copy()
print(f"df: {df.shape}, geo: {geo.shape}")

BOROUGHS = ['BROOKLYN', 'BRONX', 'QUEENS', 'MANHATTAN', 'STATEN ISLAND']
BORO_COLOR = {
    'BROOKLYN':      '#c0392b',
    'BRONX':         '#e67e22',
    'QUEENS':        '#f39c12',
    'MANHATTAN':     '#2980b9',
    'STATEN ISLAND': '#27ae60',
}

# ── 1. Annual trend: city total only, with annotations ───────────────────────
annual_total = df.groupby('YEAR').size().reset_index(name='count')

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=annual_total['YEAR'], y=annual_total['count'],
    mode='lines+markers',
    line=dict(color='#c0392b', width=3),
    marker=dict(size=7),
    fill='tozeroy', fillcolor='rgba(192,57,43,0.1)',
    hovertemplate='%{x}: <b>%{y}</b> incidents<extra></extra>'
))
fig.update_layout(
    annotations=[
        dict(x=2013, y=annual_total.loc[annual_total.YEAR==2013,'count'].values[0],
             text='Stop-and-Frisk<br>ruling (2013)',
             showarrow=True, arrowhead=2, ax=55, ay=-50, font_size=11,
             bgcolor='rgba(255,255,255,0.85)', bordercolor='#999'),
        dict(x=2020, y=annual_total.loc[annual_total.YEAR==2020,'count'].values[0],
             text='COVID-19<br>+97% vs 2019',
             showarrow=True, arrowhead=2, ax=-70, ay=-50, font_size=11,
             bgcolor='rgba(255,255,255,0.85)', bordercolor='#c0392b'),
    ],
    xaxis=dict(title='Year', tickmode='linear', dtick=1, tickangle=45, gridcolor='#eee'),
    yaxis=dict(title='Incidents', gridcolor='#eee'),
    plot_bgcolor='white', paper_bgcolor='white',
    margin=dict(l=60, r=30, t=30, b=60),
    height=410, hovermode='x unified',
    showlegend=False
)
fig.write_html('viz_annual.html', include_plotlyjs='cdn', config={'displayModeBar': False})
print("Saved viz_annual.html")

# ── 2. Heatmap: borough dropdown ─────────────────────────────────────────────
weekday_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

def make_pivot(data):
    return (data.groupby(['WEEKDAY','HOUR']).size()
               .unstack(fill_value=0)
               .reindex(weekday_order)
               .values.T.tolist())

groups = {'All NYC': df}
for b in BOROUGHS:
    groups[b.title()] = df[df['BORO'] == b]

# Build one heatmap trace per group, only first visible
hm_traces = []
for i, (label, data) in enumerate(groups.items()):
    z = make_pivot(data)
    hm_traces.append(go.Heatmap(
        z=z, x=weekday_order, y=list(range(24)),
        colorscale='YlOrRd',
        colorbar=dict(title='Incidents', thickness=14),
        hovertemplate='<b>%{x}</b> at %{y}:00<br>Incidents: <b>%{z}</b><extra></extra>',
        visible=(i == 0),
        name=label
    ))

dropdown_buttons = []
for i, label in enumerate(groups.keys()):
    vis = [j == i for j in range(len(groups))]
    dropdown_buttons.append(dict(label=label, method='update', args=[{'visible': vis}]))

fig2 = go.Figure(hm_traces)
fig2.update_layout(
    updatemenus=[dict(
        type='dropdown', direction='down',
        x=0.01, xanchor='left', y=1.13, yanchor='top',
        buttons=dropdown_buttons,
        bgcolor='white', bordercolor='#ccc',
        font=dict(size=13)
    )],
    annotations=[dict(text='<b>Borough:</b>', x=0.01, xref='paper',
                      y=1.17, yref='paper', showarrow=False, font=dict(size=13))],
    xaxis=dict(title=''),
    yaxis=dict(title='Hour of Day', tickmode='linear', dtick=1,
               ticktext=[f'{h:02d}:00' for h in range(24)],
               tickvals=list(range(24)), autorange='reversed'),
    plot_bgcolor='white', paper_bgcolor='white',
    margin=dict(l=70, r=20, t=70, b=40),
    height=540,
)
fig2.write_html('viz_heatmap.html', include_plotlyjs='cdn', config={'displayModeBar': False})
print("Saved viz_heatmap.html")

# ── 3. Map: density heatmap with year animation slider ───────────────────────
# Sample per year for performance (max 800 points/year)
sampled = (geo.groupby('YEAR', group_keys=False)
             .apply(lambda g: g.sample(min(len(g), 800), random_state=42)))

fig3 = px.density_mapbox(
    sampled,
    lat='Latitude', lon='Longitude',
    animation_frame='YEAR',
    zoom=10, center=dict(lat=40.7128, lon=-74.006),
    mapbox_style='open-street-map',
    radius=18,
    color_continuous_scale='YlOrRd',
    range_color=[0, 12],
    labels={'YEAR': 'Year'},
)
fig3.update_layout(
    coloraxis_showscale=False,
    margin=dict(l=0, r=0, t=0, b=0),
    height=520,
)
fig3.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 600
fig3.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 300

fig3.write_html('viz_map.html', include_plotlyjs='cdn', config={'displayModeBar': False})
print("Saved viz_map.html")

print("\nAll visualizations generated.")
