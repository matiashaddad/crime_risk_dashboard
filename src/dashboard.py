import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
import os

# DB config
# DATABASE_FILE = '../db/risk_database.db'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE_PATH = os.path.join(BASE_DIR, '..', 'db', 'risk_database.db')
# db_abs_path = os.path.abspath(DATABASE_FILE)
DB_URL = f"sqlite:///{DATABASE_FILE_PATH}"
#DB_URL = f"sqlite:///{db_abs_path}"

# FOR GITHUB PAGES
GITHUB_REPO_NAME = '/crime_risk_dashboard/'

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                #requests_pathname_prefix=GITHUB_REPO_NAME,
                #routes_pathname_prefix=GITHUB_REPO_NAME
                serve_locally=True
               )

# Connection to db
engine = create_engine(DB_URL)

def get_data_from_db():
    # Read data from crime_data
    try:
        query = "SELECT * FROM crime_data"
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print(f"Error while reading database: {e}")
        return pd.DataFrame()

# Load initial data
df_full = get_data_from_db()

# Dash config
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout components
header = dbc.Container([
    html.H1("Visualization Dashboard: Crime Risk (2023)",
            className="text-center my-4"),
    html.P("Crime and Safety Index Analysis at global level.",
           className="lead text-center")
], fluid=True)

# Filter controls
filter_controls_content = dbc.Container([
    dbc.Row([
        dbc.Col(
            # Country Dropdown
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': country, 'value': country}
                         for country in sorted(df_full['country'].unique())],
                placeholder="Select Country (Optional)",
                multi=True,
                style={'backgroundColor': '#f8f9fa'}

            ),
            width=6,
            className="mb-3"
        ),
        dbc.Col([
            # Slider
            html.Label("Risk Filter",
                       className="fw-bold mb-2"),
            # Slider with Crime Index
            dcc.Slider(
                id='crime-index-slider',
                min=df_full['crime_index'].min(),
                max=df_full['crime_index'].max(),
                step=5,
                value=df_full['crime_index'].max(),
                marks={i: str(i) for i in range(0, 101, 10)},
                tooltip={"placement": "bottom", "always_visible": True}
            ),
        ],
            width=6,
            className="mb-3"
        ),
    ]),
], fluid=True, className="mb-4")

# Final layout
app.layout = dbc.Container([
    header,
    dbc.Row(dbc.Col(html.Hr())),
    dbc.Row([
        # Graphic 1: Crime Index Heat Map
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H4("Crime Index per Country", className="card-title"),
                    dcc.Graph(id='choropleth-map')
                ]),
                className="mb-4 shadow"
            ),
            md=12
        ),
        # Graphic 2: Scatter Plot (Crime Index vs Safety Index)
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H4("Crime Index vs. Safety Index by City", className="card-title"),
                    html.P([
                        "Risk Scale (0 to 100): ",
                        html.Span("Below 40 = Low Risk ", style={'color': 'green', 'font-weight': 'bold'}),
                        "|",
                        html.Span(" 40-60 = Moderate Risk ", style={'color': 'orange', 'font-weight': 'bold'}),
                        "|",
                        html.Span(" Above 60 = High Risk", style={'color': 'red', 'font-weight': 'bold'})
                    ], className="text-center small mb-3"),
                    # Filter controls
                    filter_controls_content,

                    dcc.Graph(id='scatter-plot')
                ]),
                className="mb-4 shadow"
            ),
            md=12
        ),
    ]),

    dbc.Row(dbc.Col(html.Footer(
        html.P("Source: World Crime Index 2023",
               className="text-muted text-center py-3")
    )))
], fluid=True)

# Callbacks for Interactivity

@app.callback(
    [Output('choropleth-map', 'figure'),
     Output('scatter-plot', 'figure')],
    [Input('country-dropdown', 'value'),
     Input('crime-index-slider', 'value')]
)
def update_graphs(selected_countries, max_crime_index):
    # Filter by Crime Index
    df_filtered = df_full[df_full['crime_index'] <= max_crime_index].copy()

    # Filter by Country (if selection made)
    if selected_countries:
        df_filtered = df_filtered[df_filtered['country'].isin(selected_countries)]

    # 1. Choroplethic Map (Crime Index by Country - Global Risk)
    # Group and average Crime Index by Country
    df_map = df_full.groupby('country')['crime_index'].mean().reset_index()
    df_map.columns = ['country', 'avg_crime_index']

    # df_full for map to show global context
    # color basaded on crime index
    fig_map = px.choropleth(
        df_map,
        locations='country',
        locationmode='country names',
        color='avg_crime_index',
        hover_name='country',
        color_continuous_scale=px.colors.sequential.Reds, # Red scale for risk
        title='Average Crime Index by Country',
        template='plotly_white'
    )
    fig_map.update_layout(margin={"r":0,"t":50,"l":0,"b":0})

    # 2. Scatter Plot (Connection between indices - Specific Risk)
    fig_scatter = px.scatter(
        df_filtered,
        x='crime_index',
        y='safety_index',
        color='country',
        hover_data=['city', 'rank'],
        title=f'Cities with Crime Index <= {max_crime_index}',
        template='plotly_white'
    )
    fig_scatter.update_xaxes(title="Crime Index (High Risk ->)")
    fig_scatter.update_yaxes(title="Security Index (Low Risk ->)")

    return fig_map, fig_scatter

# Execute app
if __name__ == '__main__':
    print("Iniziating Dashboard. Go to http://127.0.0.1:8050/")
    app.run(debug=True)
