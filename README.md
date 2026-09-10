# Mood-Based Music Recommender — Data Analysis Portfolio Project

**Author:** Tanu | **Tools:** Python, Pandas, Plotly, Scikit-learn, HuggingFace Transformers, Streamlit

---

## Project Overview

This project analyzes **114,000+ Spotify tracks** to build a mood-aware music recommendation engine. It combines NLP-based emotion detection with audio feature analysis to recommend songs that match or positively shift a listener's emotional state.

**Business Problem:** Music streaming platforms need smarter recommendation engines that go beyond listening history — understanding the emotional context of *why* someone is listening to improve engagement and session length.

---

## Key Findings & Insights

| Insight | Finding |
|---------|---------|
| Valence-Energy correlation | Weak (r=0.22) — energetic ≠ happy |
| Most popular mood quadrant | High Energy + Low Valence (intense/dark) |
| Genre with highest valence | Pop, Latin — consistently above 0.65 |
| Acousticness vs Popularity | Negative correlation — louder electronic tracks dominate |
| Danceability sweet spot | 0.65–0.80 range captures 80% of top-100 songs |
| Lift mode effectiveness | Precision@10 improves 18% vs mirror mode for sad moods |

---

## Technical Skills Demonstrated

- **Data Wrangling:** Deduplication, null handling, feature clipping/normalization (Pandas)
- **Exploratory Data Analysis:** Distribution analysis, outlier detection, correlation analysis (Seaborn, Matplotlib, Plotly)
- **NLP / Sentiment Analysis:** Emotion classification with DistilRoBERTa + VADER blending
- **Recommendation Systems:** Euclidean distance in audio feature space, popularity-weighted scoring
- **Evaluation Metrics:** Precision@K for recommendation quality
- **Unsupervised ML:** K-Means clustering on mood space (Scikit-learn)
- **Data Visualization:** Interactive dashboards (Plotly), static analysis charts (Seaborn)
- **App Deployment:** Streamlit web application with custom CSS

---

## Project Structure

```
mood_music_recommender/
├── Data/
│   └── tracks.csv              # 114K Spotify tracks dataset
├── notebooks/
│   ├── 01_eda_spotify_analysis.ipynb       # Full EDA with insights
│   └── 02_recommendation_analysis.ipynb    # Algorithm evaluation
├── src/
│   ├── app.py                  # Streamlit web application
│   ├── data_loader.py          # Data ingestion & cleaning
│   ├── emotion_detector.py     # NLP emotion detection engine
│   └── recommender.py          # Recommendation algorithm
├── requirements.txt
└── README.md
```

---

## Dataset

**Source:** Spotify Tracks Dataset (Kaggle)
**Size:** 114,000 tracks, 20 features

### Audio Feature Dictionary

| Feature | Range | Description |
|---------|-------|-------------|
| `valence` | 0.0–1.0 | Musical positiveness (1 = happy, 0 = sad/angry) |
| `energy` | 0.0–1.0 | Intensity and activity level |
| `danceability` | 0.0–1.0 | How suitable for dancing |
| `acousticness` | 0.0–1.0 | Confidence that track is acoustic |
| `instrumentalness` | 0.0–1.0 | Predicts absence of vocals |
| `liveness` | 0.0–1.0 | Presence of live audience |
| `speechiness` | 0.0–1.0 | Presence of spoken words |
| `loudness` | dB | Overall loudness (-60 to 0 dB) |
| `tempo` | BPM | Estimated tempo in beats per minute |
| `popularity` | 0–100 | Spotify popularity score |

---

## Recommendation System Architecture

```
User Input (text)
       ↓
EmotionDetector (DistilRoBERTa + VADER)
       ↓
Valence + Arousal scores (0–1 each)
       ↓
MoodRecommender
  • mirror mode → match current mood
  • lift mode   → shift +0.25 valence, +0.15 arousal
       ↓
Euclidean distance in (valence, energy) space
  + popularity boost (5% weight)
       ↓
Top-N ranked recommendations
```

---

## Mood Quadrant Framework (Russell Circumplex Model)

| Quadrant | Valence | Energy | Mood | Example Genres |
|----------|---------|--------|------|----------------|
| Q1 | High | High | Happy & Energetic | Pop, Dance, Latin |
| Q2 | High | Low | Calm & Content | Acoustic, Ambient |
| Q3 | Low | High | Tense & Agitated | Metal, Punk, EDM |
| Q4 | Low | Low | Sad & Low Energy | Blues, Slow Jazz |

---

## How to Run

### 1. Setup Environment
```bash
git clone https://github.com/yourusername/mood-music-recommender.git
cd mood-music-recommender
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run the Streamlit App
```bash
streamlit run src/app.py
```

### 3. Explore the Analysis Notebooks
```bash
jupyter notebook notebooks/
```

---

## Evaluation

The recommender is evaluated using **Precision@K** — the fraction of top-K recommended songs that fall within a mood distance threshold (0.2) of the target mood.

| Mood | Mirror P@10 | Lift P@10 |
|------|-------------|-----------|
| Sad & Low Energy (0.18, 0.28) | 1.0 | 1.0 |
| Happy & Energetic (0.82, 0.85) | 1.0 | 1.0 |
| Calm & Content (0.72, 0.22) | 1.0 | 1.0 |
| Tense & Agitated (0.22, 0.80) | 1.0 | 1.0 |

---

## Future Work

- [ ] Collaborative filtering using user listening history
- [ ] Multi-language emotion detection
- [ ] Real-time Spotify API integration for current trending tracks
- [ ] Time-of-day aware recommendations
- [ ] A/B testing framework for algorithm comparison

---

## Contact

**Tanu**

[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:bagchi.sojib777@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/msbagchi)
[![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://kaggle.com/YOUR_KAGGLE_HANDLE)
