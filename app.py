import dash
from dash import html, dcc
from item_layout import layout as item_layout, register_item_callbacks
from user_layout import layout as user_layout, register_user_callbacks
from dash import Dash
import dash_bootstrap_components as dbc

app = Dash(__name__, suppress_callback_exceptions=True, 
                 external_stylesheets=[
                     dbc.themes.DARKLY,
                     "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
                 ])
server = app.server

MOVIE_THEME = {
    'background': 'linear-gradient(rgba(0, 10, 20, 0.85), rgba(0, 20, 40, 0.6)), url("https://i.pinimg.com/736x/3b/88/8a/3b888ae33caddd009ea0262a6dace304.jpg")',
    'backgroundSize': 'cover',
    'backgroundPosition': 'center',
    'backgroundAttachment': 'fixed',
    'minHeight': '100vh',
    'color': '#E0E7E9',  
    'padding': '1rem',
    'backdropFilter': 'blur(3px)',
    'overflowX': 'hidden'
}

def main_layout():
    return html.Div(style=MOVIE_THEME, children=[
        dbc.Container([
            dbc.Row(
                dbc.Col(
                    html.Div([
                        html.H1("RECOMMEND IT", 
                               className="text-center mb-3 mb-md-4", 
                               style={
                                   'fontWeight': 'bold',
                                   'color': '#00A3E0',  # Cyan for the title
                                   'textShadow': '0 0 10px rgba(0, 163, 224, 0.8)',
                                   'letterSpacing': '0.2em',
                                   'animation': 'glow 2s ease-in-out infinite alternate',
                                   'fontSize': 'clamp(2rem, 5vw, 3.5rem)'
                               }),
                        html.Hr(style={
                            'borderTop': '1px solid rgba(0, 163, 224, 0.5)',  
                            'width': '80%', 
                            'margin': '0 auto'
                        })
                    ]),
                    width=12,
                    className="mb-4 mb-md-5"
                )
            ),

            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        [
                            html.Div(className="text-center p-3 p-md-4", children=[
                                html.I(className="fa-solid fa-users",
                                      style={
                                          'color': '#E0E7E9',  
                                          'filter': 'drop-shadow(0 0 8px #00A3E0)',  
                                          'transition': 'all 0.3s ease',
                                          'fontSize': 'clamp(2.5rem, 6vw, 4rem)'
                                      })
                            ]),
                            dbc.CardBody([
                                html.H4("USER RECOMMENDATION", 
                                       className="card-title text-center mb-2 mb-md-3",
                                       style={'fontSize': 'clamp(1rem, 2vw, 1.25rem)', 'color': '#E0E7E9'}),
                                dbc.Button(
                                    "Enter",
                                    href="/user",
                                    className="stretched-link mt-2",
                                    style={
                                        "backgroundColor": "#00A3E0",  
                                        "color": "#E0E7E9",
                                        "border": "none",
                                        "padding": "0.5rem 1.5rem",
                                        "borderRadius": "20px",
                                        "transition": "all 0.3s ease",
                                        "boxShadow": "0 0 10px rgba(0, 163, 224, 0.5)",
                                        "fontSize": "clamp(0.8rem, 1.5vw, 1rem)"
                                    }
                                )
                            ])
                        ],
                        className="h-100 text-center shadow-lg",
                        style={
                            'background': 'rgba(10, 20, 40, 0.7)', 
                            'border': '1px solid rgba(0, 163, 224, 0.5)',  
                            'borderRadius': '15px',
                            'transition': 'all 0.3s ease',
                            'cursor': 'pointer',
                            'boxShadow': '0 0 20px rgba(0, 163, 224, 0.3)',
                            'backdropFilter': 'blur(5px)',
                            'marginBottom': '1rem'
                        },
                        id="user-card"
                    ),
                    xs=12, sm=10, md=6, lg=5, xl=4,
                    className="mb-3 mb-md-4 px-2 px-sm-3"
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            html.Div(className="text-center p-3 p-md-4", children=[
                                html.I(className="fa-solid fa-film",
                                      style={
                                          'color': '#E0E7E9',  
                                          'filter': 'drop-shadow(0 0 8px #00A3E0)',  
                                          'transition': 'all 0.3s ease',
                                          'fontSize': 'clamp(2.5rem, 6vw, 4rem)'
                                      })
                            ]),
                            dbc.CardBody([
                                html.H4("MOVIE RECOMMENDATION", 
                                       className="card-title text-center mb-2 mb-md-3",
                                       style={'fontSize': 'clamp(1rem, 2vw, 1.25rem)', 'color': '#E0E7E9'}),
                                dbc.Button(
                                    "Enter",
                                    href="/item",
                                    className="stretched-link mt-2",
                                    style={
                                        "backgroundColor": "#00A3E0",  
                                        "color": "#E0E7E9",
                                        "border": "none",
                                        "padding": "0.5rem 1.5rem",
                                        "borderRadius": "20px",
                                        "transition": "all 0.3s ease",
                                        "boxShadow": "0 0 10px rgba(0, 163, 224, 0.5)",
                                        "fontSize": "clamp(0.8rem, 1.5vw, 1rem)"
                                    }
                                )
                            ])
                        ],
                        className="h-100 text-center shadow-lg",
                        style={
                            'background': 'rgba(10, 20, 40, 0.7)',  
                            'border': '1px solid rgba(0, 163, 224, 0.5)',  
                            'borderRadius': '15px',
                            'transition': 'all 0.3s ease',
                            'cursor': 'pointer',
                            'boxShadow': '0 0 20px rgba(0, 163, 224, 0.3)',
                            'backdropFilter': 'blur(5px)',
                            'marginBottom': '1rem'
                        },
                        id="item-card"
                    ),
                    xs=12, sm=10, md=6, lg=5, xl=4,
                    className="mb-3 mb-md-4 px-2 px-sm-3"
                )
            ], justify="center", className="g-0 g-md-4"),
            
            dbc.Row(
                dbc.Col(
                    html.Div([
                        html.Hr(style={
                            'borderTop': '1px solid rgba(0, 163, 224, 0.3)',  
                            'width': '70%', 
                            'margin': '1.5rem auto'
                        }),
                        html.P("YOUR PREMIERE MOVIE RECOMMENDATION PLATFORM", 
                              className="text-center mt-2 mt-md-3",
                              style={
                                  'letterSpacing': '0.1em',
                                  'fontSize': 'clamp(0.7rem, 1.5vw, 0.9rem)',
                                  'color': 'rgba(224, 231, 233, 0.6)', 
                                  'textShadow': '0 2px 4px rgba(0, 163, 224, 0.3)'
                              })
                    ]),
                    width=12
                )
            )
        ], fluid=True, className="py-3 py-md-4"),
        
        dcc.Markdown("""
            <style>
                @keyframes glow {
                    from {
                        text-shadow: 0 0 10px rgba(0, 163, 224, 0.8);
                    }
                    to {
                        text-shadow: 0 0 15px rgba(0, 163, 224, 1), 
                                     0 0 20px rgba(0, 163, 224, 0.8);
                    }
                }
                
                .stretched-link:hover {
                    background-color: rgba(0, 163, 224, 1) !important;
                    transform: scale(1.05);
                    box-shadow: 0 0 15px rgba(0, 163, 224, 0.8) !important;
                }
                
                @media (max-width: 767.98px) {
                    .container-fluid {
                        padding-left: 15px;
                        padding-right: 15px;
                    }
                    
                    .card {
                        margin-bottom: 1.5rem;
                    }
                    
                    .fa-users, .fa-film {
                        font-size: 3rem !important;
                    }
                }
                
                @media (max-width: 575.98px) {
                    h1 {
                        font-size: 2rem !important;
                        letter-spacing: 0.1em !important;
                    }
                    
                    .card-title {
                        font-size: 1.1rem !important;
                    }
                    
                    .btn {
                        padding: 0.4rem 1rem !important;
                    }
                }
            </style>
        """, dangerously_allow_html=True)
    ])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/user':
        return user_layout()
    elif pathname == '/item':
        return item_layout()
    return main_layout()

app.clientside_callback(
    """
    function(n_clicks) {
        return window.location.href.includes('user') 
            ? {
                'transform': 'scale(1)',
                'boxShadow': '0 8px 32px rgba(0, 163, 224, 0.4)',
                'border': '1px solid rgba(0, 163, 224, 0.7)',
                'backdropFilter': 'blur(10px)',
                'background': 'rgba(15, 25, 45, 0.8)'
              }
            : {
                'transform': 'scale(1.05)',
                'boxShadow': '0 12px 28px rgba(0, 163, 224, 0.6)',
                'border': '1px solid rgba(0, 163, 224, 0.9)',
                'backdropFilter': 'blur(8px)',
                'background': 'rgba(20, 30, 50, 0.9)'
              };
    }
    """,
    dash.dependencies.Output("user-card", "style"),
    [dash.dependencies.Input("url", "pathname")],
    prevent_initial_call=False
)

app.clientside_callback(
    """
    function(n_clicks) {
        return window.location.href.includes('item') 
            ? {
                'transform': 'scale(1)',
                'boxShadow': '0 8px 32px rgba(0, 163, 224, 0.4)',
                'border': '1px solid rgba(0, 163, 224, 0.7)',
                'backdropFilter': 'blur(10px)',
                'background': 'rgba(15, 25, 45, 0.8)'
              }
            : {
                'transform': 'scale(1.05)',
                'boxShadow': '0 12px 28px rgba(0, 163, 224, 0.6)',
                'border': '1px solid rgba(0, 163, 224, 0.9)',
                'backdropFilter': 'blur(8px)',
                'background': 'rgba(20, 30, 50, 0.9)'
              };
    }
    """,
    dash.dependencies.Output("item-card", "style"),
    [dash.dependencies.Input("url", "pathname")],
    prevent_initial_call=False
)

register_item_callbacks(app)
register_user_callbacks(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
