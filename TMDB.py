# TMDB.py
import requests
import pandas as pd

api_key = '7be4893584f0163699702351130411a2'

# Load once
movies_df = pd.read_csv("movies.csv")
links_df = pd.read_csv("links.csv")
merged_df = pd.merge(movies_df, links_df, on="movieId")

def get_poster_url(tmdb_id, api_key=api_key):
    if pd.isna(tmdb_id):
        return None
    url = f"https://api.themoviedb.org/3/movie/{int(tmdb_id)}?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None

def get_poster_url_by_title(title):
    row = merged_df[merged_df["title"] == title]
    if row.empty:
        return None
    tmdb_id = row.iloc[0]["tmdbId"]
    return get_poster_url(tmdb_id)
