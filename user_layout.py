from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import pickle
import os
from TMDB import get_poster_url_by_title

os.environ['SURPRISE_DATA_FOLDER'] = '/tmp/surprise_data'

def cached_poster_url(title):
    return get_poster_url_by_title(title)

print("Loading data...")
ratings_df = pd.read_csv('ratings.csv', dtype={'userId': 'int32', 'movieId': 'int32', 'rating': 'float32'})
movies_df = pd.read_csv('movies.csv', dtype={'movieId': 'int32'})

ratings_df['timestamp'] = pd.to_datetime(ratings_df['timestamp'], unit='s')

merged_data = pd.merge(ratings_df, movies_df, on='movieId')

print("Precomputing user data...")
user_rated_movies = ratings_df.groupby('userId')['movieId'].apply(set).to_dict()
all_movie_ids = set(movies_df['movieId'])

print("Loading model...")
with open('svd_model.pkl', 'rb') as f:
    model = pickle.load(f)

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

INPUT_STYLE = {
    'backgroundColor': 'rgba(0, 100, 150, 0.8)',
    'color': 'white',
    'border': '1px solid rgba(0, 163, 224, 0.5)',
    'borderRadius': '8px',
    'width': '100%',
    'padding': '0.5rem',
    'transition': 'all 0.3s ease'
}

def create_movie_card(title, rating, date=None, is_prediction=False):
    rating_text = f"{rating:.1f} ★ (predicted)" if is_prediction else f"{rating:.1f} ★"
    
    return dbc.Card([
        dbc.CardBody([
            html.Img(
                src=cached_poster_url(title),
                style=POSTER_IMAGE_STYLE,
                alt=title,
                className="mb-2 poster-img"
            ),
            html.H5(
                title,
                className="h6 mb-1",
                style={
                    'whiteSpace': 'nowrap',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'color': '#e0e7e9'
                }
            ),
            html.Small(
                f"{rating_text} | {date.strftime('%Y-%m-%d')}" if date else rating_text,
                className="text-muted"
            )
        ])
    ], style=POSTER_CARD_STYLE, className="h-100 poster-card") 

def create_skeleton_loader(count=5):
    return html.Div(
        [dbc.Card([
            dbc.CardBody([
                html.Div(style={
                    'width': '100%',
                    'height': '240px',
                    'backgroundColor': '#1a2a3a',
                    'borderRadius': '5px',
                    'marginBottom': '0.5rem'
                }),
                html.Div(style={
                    'width': '80%',
                    'height': '20px',
                    'backgroundColor': '#1a2a3a',
                    'margin': '0 auto 0.5rem'
                }),
                html.Div(style={
                    'width': '60%',
                    'height': '15px',
                    'backgroundColor': '#1a2a3a',
                    'margin': '0 auto'
                })
            ])
        ], style=POSTER_CARD_STYLE) for _ in range(count)],
        className="d-flex flex-wrap justify-content-center"
    )

def layout():
    return html.Div(style=APP_THEME, children=[
        dbc.Container([
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
                            "User-Based Recommendations",
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
                            html.H4("Enter User ID", className="card-title mb-3", style={'color': '#00A3E0'}),
                            dbc.Input(
                                id='user-id-input',
                                type='number',
                                min=1,
                                max=ratings_df['userId'].max(),
                                placeholder=f'Enter User ID ',
                                style=INPUT_STYLE,
                                className='mb-3',
                                debounce=True
                            ),
                            dbc.Spinner(
                                html.Div(id='user-movie-posters'),
                                color="primary"
                            )
                        ])
                    ], style=CARD_STYLE),
                    
                    html.Div(id='recommendation-controls-user', children=[
                        dbc.Card([
                            dbc.CardBody([
                                html.Div(className="d-flex justify-content-between align-items-center mb-3", children=[
                                    html.H4("Recommended Movies", className="m-0", style={'color': "#FFFFFF"}),
                                    dbc.Button(
                                        "How these were chosen",
                                        id="explanation-popover-target",
                                        color="link",
                                        className="p-0 text-muted"
                                    )
                                ]),
                                dbc.Popover(
                                    "These recommendations are generated using collaborative filtering, finding movies that similar users have enjoyed.",
                                    target="explanation-popover-target",
                                    trigger="hover",
                                    placement="bottom"
                                ),
                                html.Div(
                                    id='user-recommendations',
                                    className="d-flex flex-wrap justify-content-center"
                                )
                            ])
                        ], style=CARD_STYLE)
                    ], style={'display': 'none'})
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

def register_callbacks(app):
    @app.callback(
        Output('user-movie-posters', 'children'),
        Output('user-recommendations', 'children'),
        Output('recommendation-controls-user', 'style'),
        Input('user-id-input', 'value'),
        prevent_initial_call=True
    )
    def update_recommendations(user_id):
        if not user_id or user_id < 1 or user_id > ratings_df['userId'].max():
            return None, None, {'display': 'none'}
        
        try:
            user_id = int(user_id)
            user_ratings = merged_data[merged_data['userId'] == user_id]
            
            if user_ratings.empty:
                return (
                    dbc.Alert(f"No ratings found for user {user_id}", color="warning"),
                    [],
                    {'display': 'none'}
                )

            recent_movies = user_ratings.sort_values('timestamp', ascending=False).head(10)
            
            unseen_movies = list(all_movie_ids - user_rated_movies.get(user_id, set()))
            
            predictions = []
            batch_size = 500
            for i in range(0, min(1000, len(unseen_movies)), batch_size):
                batch = unseen_movies[i:i+batch_size]
                predictions.extend((mid, model.predict(user_id, mid).est) for mid in batch)
            
            top_recommendations = sorted(predictions, key=lambda x: -x[1])[:10]
            rec_movies = pd.merge(
                pd.DataFrame(top_recommendations, columns=['movieId', 'predicted']),
                movies_df,
                on='movieId'
            )
            
            rated_movies_cards = [
                create_movie_card(
                    row['title'],
                    row['rating'],
                    row['timestamp']
                ) for _, row in recent_movies.iterrows()
            ]
            
            recommendation_cards = [
                create_movie_card(
                    row['title'],
                    row['predicted'],
                    is_prediction=True
                ) for _, row in rec_movies.iterrows()
            ]
            
            return (
                dbc.Card([
                    dbc.CardBody([
                        html.H4("User's Recently Rated Movies:", className="card-title mb-3", style={'color': 'white'}),
                        html.Div(
                            className="d-flex flex-wrap justify-content-center",
                            children=rated_movies_cards
                        )
                    ])
                ], style=CARD_STYLE),
                recommendation_cards,
                {'display': 'block'}
            )
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return (
                dbc.Alert("An error occurred while processing your request.", color="danger"),
                [],
                {'display': 'none'}
            )

register_user_callbacks = register_callbacks
