import pandas as pd
import numpy as np

def load_spotify_data(path="data/spotify_tracks.csv"):
    df = pd.read_csv(path)
    
    # Drop duplicates and nulls
    df = df.drop_duplicates(subset=['track_id'])
    df = df.dropna(subset=['track_name', 'artists', 'valence', 'energy', 'tempo'])
    
    # Keep only useful columns
    cols = ['track_id', 'track_name', 'artists', 'album_name',
            'popularity', 'valence', 'energy', 'tempo',
            'danceability', 'acousticness', 'instrumentalness']
    df = df[cols]
    
    # Normalize valence and energy to 0-1 range
    df['valence'] = df['valence'].clip(0, 1)
    df['energy'] = df['energy'].clip(0, 1)
    
    print(f"Loaded {len(df)} songs successfully!")
    return df

if __name__ == "__main__":
    df = load_spotify_data()
    print(df.head())
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nValence range: {df['valence'].min():.2f} - {df['valence'].max():.2f}")
    print(f"Energy range:  {df['energy'].min():.2f} - {df['energy'].max():.2f}")