import pandas as pd
import numpy as np
import os

def load_spotify_data(path=None):
    if path is None:
        # Works both locally and on Streamlit Cloud
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	path = os.path.join(base_dir, "Data", "tracks.csv")
    df = pd.read_csv(path)

    # Drop duplicates and nulls
    df = df.drop_duplicates(subset=['track_id'])
    df = df.dropna(subset=['track_name', 'artists', 'valence', 'energy', 'tempo'])

    # Keep only useful columns
    cols = ['track_id', 'track_name', 'artists', 'album_name',
            'popularity', 'valence', 'energy', 'tempo',
            'danceability', 'acousticness', 'instrumentalness']
    df = df[cols]

    df['valence'] = df['valence'].clip(0, 1)
    df['energy']  = df['energy'].clip(0, 1)

    print(f"Loaded {len(df)} songs successfully!")
    return df

if __name__ == "__main__":
    df = load_spotify_data()
    print(df.head())