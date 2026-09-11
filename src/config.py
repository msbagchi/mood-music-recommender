import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "Data", "tracks.csv")

AUDIO_FEATURES = [
    "valence", "energy", "danceability",
    "acousticness", "instrumentalness", "speechiness", "liveness"
]

RECOMMENDATION_COLS = [
    "track_id", "track_name", "artists", "album_name",
    "popularity", "valence", "energy", "tempo",
    "danceability", "acousticness", "instrumentalness"
]

FULL_COLS = RECOMMENDATION_COLS + [
    "duration_ms", "explicit", "key", "loudness",
    "mode", "liveness", "speechiness", "time_signature", "track_genre"
]

GENRE_LANGUAGE_MAP = {
    "indian":      "Hindi",
    "cantopop":    "Mandarin",
    "mandopop":    "Mandarin",
    "j-pop":       "Japanese",
    "j-rock":      "Japanese",
    "j-dance":     "Japanese",
    "j-idol":      "Japanese",
    "anime":       "Japanese",
    "k-pop":       "Korean",
    "french":      "French",
    "german":      "German",
    "spanish":     "Spanish",
    "latin":       "Spanish",
    "latino":      "Spanish",
    "reggaeton":   "Spanish",
    "salsa":       "Spanish",
    "turkish":     "Turkish",
    "iranian":     "Persian",
    "malay":       "Malay",
    "brazil":      "Portuguese",
    "samba":       "Portuguese",
    "forro":       "Portuguese",
    "pagode":      "Portuguese",
    "sertanejo":   "Portuguese",
    "mpb":         "Portuguese",
}

POPULARITY_BOOST_WEIGHT = 0.05
LIFT_VALENCE_DELTA = 0.25
LIFT_AROUSAL_DELTA = 0.15
DEFAULT_TOP_N = 10
PRECISION_THRESHOLD = 0.20
