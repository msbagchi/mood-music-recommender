import pandas as pd
import os
from config import DATA_PATH, RECOMMENDATION_COLS, FULL_COLS


def load_spotify_data(path=None, full=False):
    """Load and clean the Spotify tracks dataset.

    Args:
        path: Override the default CSV path.
        full: If True, return all 20 columns (for EDA). Default returns
              the 11 recommendation-relevant columns.
    """
    if path is None:
        path = DATA_PATH

    df = pd.read_csv(path)
    df = df.drop_duplicates(subset=["track_id"])
    df = df.dropna(subset=["track_name", "artists", "valence", "energy", "tempo"])

    cols = FULL_COLS if full else RECOMMENDATION_COLS
    # only keep columns that actually exist in this CSV version
    cols = [c for c in cols if c in df.columns]
    df = df[cols]

    df["valence"] = df["valence"].clip(0, 1)
    df["energy"] = df["energy"].clip(0, 1)

    print(f"Loaded {len(df):,} songs.")
    return df


if __name__ == "__main__":
    df = load_spotify_data()
    print(df.head())
