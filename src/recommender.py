import numpy as np
import pandas as pd
from config import (
    POPULARITY_BOOST_WEIGHT, LIFT_VALENCE_DELTA,
    LIFT_AROUSAL_DELTA, DEFAULT_TOP_N, PRECISION_THRESHOLD
)


class MoodRecommender:
    def __init__(self, df):
        self.df = df.copy()
        self._language_warning = None

    def recommend(self, valence, arousal, mode="mirror", top_n=DEFAULT_TOP_N, language=None):
        """Recommend tracks based on target mood.

        Args:
            valence:  Target valence (0–1).
            arousal:  Target arousal/energy (0–1).
            mode:     'mirror' matches current mood; 'lift' shifts target toward
                      higher valence and energy.
            top_n:    Number of tracks to return.
            language: Optional language filter ('Hindi', 'Bengali', 'English', etc.).
                      Falls back to all languages if fewer than top_n tracks are found.
        """
        self._language_warning = None
        df = self.df.copy()

        if language and language != "All" and "language" in df.columns:
            filtered = df[df["language"] == language]
            if len(filtered) >= top_n:
                df = filtered
            else:
                self._language_warning = (
                    f"Not enough '{language}' songs in the dataset for this mood. "
                    f"Showing results from all languages."
                )

        if mode == "lift":
            valence = min(1.0, valence + LIFT_VALENCE_DELTA)
            arousal = min(1.0, arousal + LIFT_AROUSAL_DELTA)

        df = df.assign(
            distance=np.sqrt(
                (df["valence"] - valence) ** 2 +
                (df["energy"] - arousal) ** 2
            )
        )
        df = df.assign(
            popularity_score=df["popularity"] / 100.0
        )
        df = df.assign(
            final_score=df["distance"] - (POPULARITY_BOOST_WEIGHT * df["popularity_score"])
        )

        results = df.nsmallest(top_n, "final_score")[
            ["track_name", "artists", "valence", "energy",
             "tempo", "danceability", "popularity", "distance"]
        ].reset_index(drop=True)

        results = results.assign(
            rank=results.index + 1,
            valence=results["valence"].round(3),
            energy=results["energy"].round(3),
            distance=results["distance"].round(3),
        )

        return results

    def precision_at_k(self, valence, arousal, k=DEFAULT_TOP_N,
                       threshold=PRECISION_THRESHOLD):
        """Fraction of top-K recommendations within threshold distance of target mood."""
        results = self.recommend(valence, arousal, top_n=k)
        return round((results["distance"] <= threshold).sum() / k, 3)


if __name__ == "__main__":
    from data_loader import load_spotify_data

    df = load_spotify_data()
    recommender = MoodRecommender(df)

    print("\n--- Sad & Tired (mirror) ---")
    print(recommender.recommend(0.183, 0.302, mode="mirror")[
        ["rank", "track_name", "artists", "valence", "energy"]
    ].to_string())

    print("\n--- Hindi recommendations ---")
    print(recommender.recommend(0.5, 0.6, language="Hindi")[
        ["rank", "track_name", "artists", "valence", "energy"]
    ].to_string())

    print(f"\nPrecision@10: {recommender.precision_at_k(0.183, 0.302)}")
