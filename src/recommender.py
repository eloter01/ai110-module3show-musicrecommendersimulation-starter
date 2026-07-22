import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        prefs = _profile_to_prefs(user)
        ranked = sorted(self.songs, key=lambda s: score_song(prefs, asdict(s))[0], reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        prefs = _profile_to_prefs(user)
        score, reasons = score_song(prefs, asdict(song))
        return "; ".join(reasons) if reasons else f"no strong matches (score {score})"


def _profile_to_prefs(user: UserProfile) -> Dict:
    """Maps a UserProfile dataclass onto the dict keys score_song expects."""
    return {
        "favorite_genre": user.favorite_genre,
        "favorite_mood": user.favorite_mood,
        "target_energy": user.target_energy,
        "target_acousticness": 1.0 if user.likes_acoustic else 0.0,
    }

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file into a list of dicts,
    converting numeric columns to int/float for scoring.
    Required by src/main.py
    """
    int_fields = {"id", "tempo_bpm"}
    float_fields = {"energy", "valence", "danceability",
                    "acousticness", "instrumentalness", "speechiness"}
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

GENRE_POINTS = 2.0
MOOD_POINTS = 1.0
NUMERIC_WEIGHTS = {
    "energy": 1.0,
    "acousticness": 1.0,
    "instrumentalness": 0.8,
    "valence": 0.6,
    "danceability": 0.6,
    "tempo": 0.5,
    "speechiness": 0.4,
}
TEMPO_MIN, TEMPO_MAX = 60, 160


def _norm_tempo(bpm: float) -> float:
    """Normalizes a tempo in BPM to a 0-1 scale for scoring."""
    return (bpm - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences using the Algorithm Recipe:
    +2.0 genre match, +1.0 mood match, and weighted closeness for numeric features.
    Returns (score, reasons) where reasons explain the points awarded.
    """
    score = 0.0
    reasons = []

    if user_prefs["favorite_genre"] == song["genre"]:
        score += GENRE_POINTS
        reasons.append(f"genre match: {song['genre']} (+{GENRE_POINTS})")
    if user_prefs["favorite_mood"] == song["mood"]:
        score += MOOD_POINTS
        reasons.append(f"mood match: {song['mood']} (+{MOOD_POINTS})")

    for feature, weight in NUMERIC_WEIGHTS.items():
        if feature == "tempo":
            if "target_tempo_bpm" not in user_prefs:
                continue
            target = _norm_tempo(user_prefs["target_tempo_bpm"])
            value = _norm_tempo(song["tempo_bpm"])
        else:
            key = f"target_{feature}"
            if key not in user_prefs or feature not in song:
                continue
            target = user_prefs[key]
            value = song[feature]
        points = weight * (1 - abs(target - value))
        score += points
        if points >= 0.8 * weight:  # surface only the close matches
            reasons.append(f"{feature} close (+{points:.2f})")

    return round(score, 2), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Scores every song with score_song(), then returns the top k
    as (song, score, explanation), highest score first.
    """
    ranked = sorted(
        ((song, *score_song(user_prefs, song)) for song in songs),
        key=lambda item: item[1],
        reverse=True,
    )
    return [(song, score, "; ".join(reasons)) for song, score, reasons in ranked[:k]]
