from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Emotion to Valence/Arousal mapping
# Based on Russell Circumplex Model
EMOTION_TO_VA = {
    "joy":        (0.85, 0.75),
    "happiness":  (0.85, 0.75),
    "love":       (0.80, 0.60),
    "excitement": (0.75, 0.90),
    "surprise":   (0.60, 0.80),
    "neutral":    (0.50, 0.50),
    "calm":       (0.65, 0.25),
    "sadness":    (0.20, 0.30),
    "fear":       (0.25, 0.70),
    "anger":      (0.20, 0.85),
    "disgust":    (0.20, 0.50),
    "grief":      (0.10, 0.20),
}

class EmotionDetector:
    def __init__(self):
        print("Loading emotion model... (first time may take a minute)")
        self.emotion_pipe = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            top_k=3
        )
        self.vader = SentimentIntensityAnalyzer()
        print("Emotion model loaded!")

    def detect(self, text):
        # Get top 3 emotions with scores
        results = self.emotion_pipe(text)[0]

        # Get VADER sentiment score
        vader_score = self.vader.polarity_scores(text)
        compound = vader_score['compound']  # -1 to +1

        # Calculate weighted valence and arousal
        total_score = sum(r['score'] for r in results)
        valence = 0.0
        arousal = 0.0

        for r in results:
            label = r['label'].lower()
            score = r['score'] / total_score
            v, a = EMOTION_TO_VA.get(label, (0.5, 0.5))
            valence += v * score
            arousal += a * score

        # Blend VADER compound score into valence
        vader_valence = (compound + 1) / 2  # convert -1~1 to 0~1
        valence = 0.7 * valence + 0.3 * vader_valence

        return {
            "emotions": results,
            "valence": round(valence, 3),
            "arousal": round(arousal, 3),
            "vader_compound": round(compound, 3)
        }

    def describe_mood(self, valence, arousal):
        if valence >= 0.6 and arousal >= 0.6:
            return "Happy & Energetic"
        elif valence >= 0.6 and arousal < 0.6:
            return "Calm & Content"
        elif valence < 0.6 and arousal >= 0.6:
            return "Tense & Agitated"
        else:
            return "Sad & Low Energy"


if __name__ == "__main__":
    detector = EmotionDetector()

    test_inputs = [
        "I feel tired and sad",
        "I am so happy and excited today!",
        "I am anxious and stressed about my exam",
        "Feeling peaceful and relaxed"
    ]

    for text in test_inputs:
        print(f"\nInput: '{text}'")
        result = detector.detect(text)
        mood = detector.describe_mood(result['valence'], result['arousal'])
        print(f"Emotions: {result['emotions']}")
        print(f"Valence: {result['valence']}  Arousal: {result['arousal']}")
        print(f"Mood Quadrant: {mood}")