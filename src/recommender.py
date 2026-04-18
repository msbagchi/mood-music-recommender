import numpy as np
import pandas as pd

class MoodRecommender:
    def __init__(self, df):
        self.df = df.copy()

    def recommend(self, valence, arousal, mode="mirror", top_n=10):
        """
        mode = 'mirror' : match current mood
        mode = 'lift'   : gradually shift toward happier/energetic
        """
        df = self.df.copy()

        # Lift mode shifts target toward positive
        if mode == "lift":
            valence = min(1.0, valence + 0.25)
            arousal = min(1.0, arousal + 0.15)

        # Calculate Euclidean distance in valence-arousal space
        df['distance'] = np.sqrt(
            (df['valence'] - valence) ** 2 +
            (df['energy'] - arousal) ** 2
        )

        # Popularity boost — slightly prefer popular songs
        df['popularity_score'] = df['popularity'] / 100.0

        # Final score: closer distance + higher popularity
        df['final_score'] = df['distance'] - (0.05 * df['popularity_score'])

        # Get top N recommendations
        results = df.nsmallest(top_n, 'final_score')[
            ['track_name', 'artists', 'valence', 'energy',
             'tempo', 'danceability', 'popularity', 'distance']
        ].reset_index(drop=True)

        results['rank'] = results.index + 1
        results['valence'] = results['valence'].round(3)
        results['energy'] = results['energy'].round(3)
        results['distance'] = results['distance'].round(3)

        return results

    def precision_at_k(self, valence, arousal, k=10, threshold=0.2):
        """
        Precision@K: fraction of top-K songs within
        threshold distance of target mood
        """
        results = self.recommend(valence, arousal, top_n=k)
        relevant = results[results['distance'] <= threshold]
        return round(len(relevant) / k, 3)


if __name__ == "__main__":
    from data_loader import load_spotify_data

    df = load_spotify_data()
    recommender = MoodRecommender(df)

    print("\n--- Test 1: Sad & Tired (mirror mode) ---")
    results = recommender.recommend(valence=0.183, arousal=0.302, mode="mirror")
    print(results[['rank', 'track_name', 'artists', 'valence', 'energy']].to_string())

    print("\n--- Test 2: Sad & Tired (lift mode) ---")
    results = recommender.recommend(valence=0.183, arousal=0.302, mode="lift")
    print(results[['rank', 'track_name', 'artists', 'valence', 'energy']].to_string())

    print("\n--- Precision@10 ---")
    p = recommender.precision_at_k(valence=0.183, arousal=0.302, k=10)
    print(f"Precision@10: {p}")