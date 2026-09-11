import re
import pandas as pd
from config import DATA_PATH, RECOMMENDATION_COLS, FULL_COLS, GENRE_LANGUAGE_MAP

_BENGALI    = re.compile(r'[\u0980-\u09FF]')
_DEVANAGARI = re.compile(r'[\u0900-\u097F]')


def _detect_language(track_name, artists, genre):
    text = f"{track_name} {artists}"
    if _BENGALI.search(text):
        return "Bengali"
    if _DEVANAGARI.search(text):
        return "Hindi"
    return GENRE_LANGUAGE_MAP.get(genre, "English")


def load_spotify_data(path=None, full=False):
    """Load and clean the Spotify tracks dataset.

    Args:
        path: Override the default CSV path.
        full: If True, return all 20 columns (for EDA).
    """
    if path is None:
        path = DATA_PATH

    raw = pd.read_csv(path)
    raw = raw.drop_duplicates(subset=["track_id"])
    raw = raw.dropna(subset=["track_name", "artists", "valence", "energy", "tempo"])

    genre_col = raw["track_genre"] if "track_genre" in raw.columns else pd.Series([""] * len(raw), index=raw.index)

    languages = [
        _detect_language(n, a, g)
        for n, a, g in zip(raw["track_name"], raw["artists"], genre_col)
    ]

    raw = raw.assign(
        language=languages,
        valence=raw["valence"].clip(0, 1),
        energy=raw["energy"].clip(0, 1),
    )

    cols = FULL_COLS if full else RECOMMENDATION_COLS + ["language"]
    cols = [c for c in cols if c in raw.columns]

    print(f"Loaded {len(raw):,} songs.")
    return raw[cols].reset_index(drop=True)


if __name__ == "__main__":
    df = load_spotify_data()
    print(df["language"].value_counts())
