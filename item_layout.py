from dash import html, dcc, Input, Output
from dash.dependencies import State
import pandas as pd
from TMDB import get_poster_url_by_title
from datetime import datetime
import dash_bootstrap_components as dbc

df = pd.read_csv('ratings.csv')
df2 = pd.read_csv('movies.csv')
sim_df = pd.read_csv('similarity.csv.gz', index_col=0)

movie_merge = pd.merge(df, df2, on='movieId')
movie_merge['timestamp'] = movie_merge['timestamp'].apply(lambda x: datetime.utcfromtimestamp(x))
movie_merge = movie_merge[['userId', 'movieId', 'title', 'genres', 'timestamp', 'rating']]
#movies = movie_merge.head(500)  # Limit for faster load
#utility_matrix = movies.pivot(index='movieId', columns='userId', values='rating')
movies = movie_merge[movie_merge['movieId'].isin(sim_df.index)]

APP_THEME = {
    'background': 'linear-gradient(rgba(0, 10, 20, 0.85), rgba(0, 20, 40, 0.9)), url("https://i.pinimg.com/736x/3b/88/8a/3b888ae33caddd009ea0262a6dace304.jpg")',
    'minHeight': '100vh',
    'color': '#e0e7e9',
    'padding': '2rem 0',
}

CARD_STYLE = {
    'background': 'rgba(10, 20, 40, 0.8)',
    'border': '1px solid rgba(0, 163, 224, 0.3)',
    'borderRadius': '10px',
    'boxShadow': '0 4px 20px rgba(0, 163, 224, 0.1)',
    'marginBottom': '1.5rem',
    'transition': 'all 0.3s ease',
    'backdropFilter': 'blur(5px)'
}

SELECT_STYLE = {
    'backgroundColor': 'rgba(0, 100, 150, 0.8)',
    'color': 'white',
    'border': '1px solid rgba(0, 163, 224, 0.5)',
    'borderRadius': '8px',
    'width': '100%',
    'padding': '0.5rem',
    'transition': 'all 0.3s ease'
}

POSTER_CARD_STYLE = {
    'margin': '1rem',
    'textAlign': 'center',
    'width': '160px',
    'transition': 'all 0.3s ease',
    'cursor': 'pointer',
    'background': 'rgba(15, 30, 50, 0.7)',
    'borderRadius': '10px',
    'overflow': 'hidden',
    'border': '1px solid rgba(0, 163, 224, 0.2)'
}

POSTER_IMAGE_STYLE = {
    'width': '100%',
    'height': '240px',
    'objectFit': 'cover',
    'borderRadius': '8px 8px 0 0',
    'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
    'marginBottom': '0.5rem',
    'transition': 'all 0.3s ease'
}

def layout():
    return html.Div(style=APP_THEME, children=[
        dbc.Container([
            # Header
            dbc.Row([
                dbc.Col([
                    html.Div(className="d-flex justify-content-between align-items-center mb-4", children=[
                        dcc.Link(
                            dbc.Button(
                                html.I(className="fas fa-arrow-left me-2"),
                                "Back to Main",
                                color="primary",
                                outline=True,
                                className="px-3",
                                style={'transition': 'all 0.3s ease'}
                            ),
                            href="/"
                        ),
                        html.H1(
                            "Item-Based Recommendations",
                            className="m-0",
                            style={
                                'color': '#00A3E0',
                                'fontWeight': '600',
                                'textShadow': '0 2px 4px rgba(0, 163, 224, 0.3)'
                            }
                        ),
                        html.Div(style={'width': '100px'})  
                    ]),
                    html.Hr(style={
                        'borderTop': '1px solid rgba(0, 163, 224, 0.3)',
                        'margin': '0 auto 2rem',
                        'width': '80%'
                    })
                ], width=12)
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Select a Movie", className="card-title mb-3", style={'color': "#FFFFFF"}),
                            dbc.Select(
                                id='item-input',
                                options=[{'label': title, 'value': title} for title in movies['title'].unique()],
                                placeholder="Choose a movie...",
                                style=SELECT_STYLE,
                                className='mb-3'
                            ),
                            dbc.Spinner(html.Div(id='selected-movie'))
                        ])
                    ], style=CARD_STYLE),

                    html.Div(id='recommendation-controls-item', children=[
                        dbc.Card([
                            dbc.CardBody([
                                html.Div(className="d-flex justify-content-between align-items-center mb-3", children=[
                                    html.H4("Recommendation Settings", className="m-0", style={'color': "#FFFFFF"}),
                                    dbc.Button(
                                        "Hide Settings",
                                        id="toggle-settings",
                                        color="white",
                                    )
                                ]),
                                dbc.Collapse(
                                    dbc.Row([
                                        dbc.Col([
                                            html.Label("Number of Recommendations", className="mb-2"),
                                            dcc.Slider(
                                                id='item-num-movies-slider',
                                                min=1,
                                                max=10,
                                                step=1,
                                                value=5,
                                                marks={i: str(i) for i in range(1, 11)},
                                                tooltip={"placement": "bottom", "always_visible": True}
                                            )
                                        ], md=12)
                                    ]),
                                    id="settings-collapse",
                                    is_open=True
                                )
                            ])
                        ], style=CARD_STYLE),

                        dbc.Card([
                            dbc.CardBody([
                                html.Div(className="d-flex justify-content-between align-items-center mb-3", children=[
                                    html.H4("Recommended Movies", className="m-0", style={'color': "#FFFFFF"}),
                                    html.Small("Recommended based on genre similarity.", className="text-muted")
                                ]),
                                dbc.Alert(
                                    "Select a movie to see recommendations",
                                    id="recommendations-placeholder",
                                    color="secondary",
                                    className="text-center"
                                ),
                                dbc.Spinner(
                                    html.Div(
                                        id='item-output-posters',
                                        className="d-flex flex-wrap justify-content-center"
                                    )
                                )
                            ])
                        ], style=CARD_STYLE)
                    ])
                ], xs=12, sm=12, md=10, lg=9, xl=8, className="mx-auto")
            ]),

            dbc.Row([
                dbc.Col(
                    html.Div([
                        html.Hr(style={
                            'borderTop': '1px solid rgba(0, 163, 224, 0.2)',
                            'margin': '2rem auto',
                            'width': '50%'
                        }),
                        html.P("MOVIE RECOMMENDATION ENGINE", 
                              className="text-center mt-3",
                              style={
                                  'letterSpacing': '0.1em',
                                  'fontSize': '0.8rem',
                                  'color': 'rgba(224, 231, 233, 0.5)'
                              })
                    ]),
                    width=12
                )
            ])
        ], fluid=True)
    ])


def register_item_callbacks(app):
    @app.callback(
        Output('selected-movie', 'children'),
        Input('item-input', 'value'),
    )
    def show_selected_movie(title):
        if not title:
            return ""
        
        try:
            movie_data = movies[movies['title'] == title].iloc[0]
            poster_url = get_poster_url_by_title(title)
            
            return dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(
                            html.Img(
                                src=poster_url,
                                style={
                                    'width': '100%',
                                    'maxWidth': '300px',
                                    'borderRadius': '8px',
                                    'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.3)'
                                },
                                alt=title,
                                className="img-fluid"
                            ),
                            md=4
                        ),
                        dbc.Col([
                            html.H4(title, className="mb-3"),
                            html.P(f"Genres: {movie_data['genres']}", className="text-muted mb-2"),
                            html.P(f"Average Rating: {movie_data['rating']:.1f}/5", className="mb-2"),
                            html.Small(
                                f"Last rated: {movie_data['timestamp'].strftime('%Y-%m-%d')}",
                                className="text-muted"
                            )
                        ], md=8)
                    ])
                ])
            ], style=CARD_STYLE)
        except Exception as e:
            return dbc.Alert(
                f"Could not load movie details: {str(e)}",
                color="danger"
            )

    @app.callback(
        Output('item-output-posters', 'children'),
        Output('recommendations-placeholder', 'is_open'),
        Output('recommendation-controls-item', 'style'),
        Output('item-num-movies-slider', 'max'),
        Input('item-input', 'value'),
        Input('item-num-movies-slider', 'value'),
    )
    def recommend_movies(title, num_movies):
        if title is None:
            return [], True, {'display': 'none'}, 10
        
        try:
            movie_row = movies[movies['title'] == title]
            if movie_row.empty:
                return [], True, {'display': 'none'}, 10

            movie_id = movie_row['movieId'].values[0]
            val = sim_df[str(movie_id)].sort_values(ascending=False)
            val = val.loc[val.index != movie_id].head(20)

            valid_ids = [int(i) for i in val.index]
            filtered = movies[movies['movieId'].isin(valid_ids)].drop_duplicates(subset='movieId')
            filtered = filtered.set_index('movieId').loc[valid_ids].reset_index()

            max_recommendations = min(10, len(filtered))
            filtered = filtered.head(num_movies)

            poster_cards = []
            for _, row in filtered.iterrows():
                try:
                    poster_url = get_poster_url_by_title(row['title'])
                    poster_cards.append(
                        dbc.Card([
                            dbc.CardBody([
                                html.Img(
                                    src=poster_url,
                                    style=POSTER_IMAGE_STYLE,
                                    alt=row['title'],
                                    className="mb-2"
                                ),
                                html.H5(
                                    row['title'],
                                    className="h6 mb-1",
                                    style={
                                        'whiteSpace': 'nowrap',
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis'
                                    }
                                ),
                                html.Small(
                                    f"{row['rating']:.1f} ★ | {row['genres'].split('|')[0]}",
                                    className="text-muted"
                                )
                            ])
                        ], 
                        style={
                            **POSTER_CARD_STYLE,
                            ':hover': {
                                'transform': 'translateY(-5px)'
                            }
                        },
                        className="h-100")
                    )
                except:
                    continue

            return poster_cards, False, {'display': 'block'}, max_recommendations
        
        except Exception as e:
            return [dbc.Alert(
                f"Error generating recommendations: {str(e)}",
                color="danger"
            )], False, {'display': 'block'}, 10

    @app.callback(
        Output("settings-collapse", "is_open"),
        Input("toggle-settings", "n_clicks"),
        State("settings-collapse", "is_open"),
    )
    def toggle_settings(n, is_open):
        if n:
            return not is_open
        return is_open