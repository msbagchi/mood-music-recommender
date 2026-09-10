import numpy as np
import pandas as pd
from config import (
    POPULARITY_BOOST_WEIGHT, LIFT_VALENCE_DELTA,
    LIFT_AROUSAL_DELTA, DEFAULT_TOP_N, PRECISION_THRESHOLD
)


class MoodRecommender:
    def __init__(self, df):
        self.df = df.copy()

    def recommend(self, valence, arousal, mode="mirror", top_n=DEFAULT_TOP_N):
        """Recommend tracks based on target mood.

        Args:
            valence: Target valence (0–1).
            arousal: Target arousal/energy (0–1).
            mode: 'mirror' matches current mood; 'lift' shifts target toward
                  higher valence and energy to improve the listener's mood.
            top_n: Number of tracks to return.

        Returns:
            DataFrame with ranked recommendations.
        """
        df = self.df.copy()

        if mode == "lift":
            valence = min(1.0, valence + LIFT_VALENCE_DELTA)
            arousal = min(1.0, arousal + LIFT_AROUSAL_DELTA)

        df["distance"] = np.sqrt(
            (df["valence"] - valence) ** 2 +
            (df["energy"] - arousal) ** 2
        )

        df["popularity_score"] = df["popularity"] / 100.0
        df["final_score"] = df["distance"] - (POPULARITY_BOOST_WEIGHT * df["popularity_score"])

        results = df.nsmallest(top_n, "final_score")[
            ["track_name", "artists", "valence", "energy",
             "tempo", "danceability", "popularity", "distance"]
        ].reset_index(drop=True)

        results["rank"] = results.index + 1
        results["valence"] = results["valence"].round(3)
        results["energy"] = results["energy"].round(3)
        results["distance"] = results["distance"].round(3)

        return results

    def precision_at_k(self, valence, arousal, k=DEFAULT_TOP_N,
                       threshold=PRECISION_THRESHOLD):
        """Fraction of top-K recommendations within threshold distance of target mood."""
        results = self.recommend(valence, arousal, top_n=k)
        relevant = results[results["distance"] <= threshold]
        return round(len(relevant) / k, 3)


if __name__ == "__main__":
    from data_loader import load_spotify_data

    df = load_spotify_data()
    recommender = MoodRecommender(df)

    print("\n--- Sad & Tired (mirror) ---")
    print(recommender.recommend(0.183, 0.302, mode="mirror")[
        ["rank", "track_name", "artists", "valence", "energy"]
    ].to_string())

    print("\n--- Sad & Tired (lift) ---")
    print(recommender.recommend(0.183, 0.302, mode="lift")[
        ["rank", "track_name", "artists", "valence", "energy"]
    ].to_string())

    print(f"\nPrecision@10: {recommender.precision_at_k(0.183, 0.302)}")
