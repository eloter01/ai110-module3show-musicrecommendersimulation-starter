"""
Command line runner for the Music Recommender Simulation.

Runs the recommender against several taste profiles, including two
"adversarial" profiles with internally conflicting preferences, so the
scoring logic can be stress-tested from the terminal.
"""

from src.recommender import load_songs, recommend_songs

# Each profile is a full taste dict. The last two are deliberately
# self-contradicting to probe how the additive score handles conflict.
PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop", "favorite_mood": "intense",
        "target_energy": 0.95, "target_valence": 0.80, "target_danceability": 0.90,
        "target_acousticness": 0.05, "target_tempo_bpm": 130,
        "target_instrumentalness": 0.03, "target_speechiness": 0.08,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi", "favorite_mood": "chill",
        "target_energy": 0.35, "target_valence": 0.58, "target_danceability": 0.55,
        "target_acousticness": 0.85, "target_tempo_bpm": 78,
        "target_instrumentalness": 0.85, "target_speechiness": 0.03,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock", "favorite_mood": "intense",
        "target_energy": 0.92, "target_valence": 0.45, "target_danceability": 0.60,
        "target_acousticness": 0.10, "target_tempo_bpm": 150,
        "target_instrumentalness": 0.15, "target_speechiness": 0.07,
    },
    # Adversarial: "sad but hype" — high energy/tempo paired with a
    # melancholic mood and low valence. Mood/valence pull one way, energy
    # pulls the other, so no single song can satisfy both.
    "Adversarial: Sad but Hype": {
        "favorite_genre": "metal", "favorite_mood": "melancholic",
        "target_energy": 0.95, "target_valence": 0.10, "target_danceability": 0.85,
        "target_acousticness": 0.05, "target_tempo_bpm": 160,
        "target_instrumentalness": 0.05, "target_speechiness": 0.06,
    },
    # Adversarial: genre that does not exist in the catalog + every numeric
    # target pinned to 0.5. Genre points are unreachable, so ranking falls
    # entirely to the tie-prone "everything is average" numeric term.
    "Adversarial: No-Match Neutral": {
        "favorite_genre": "polka", "favorite_mood": "nonexistent",
        "target_energy": 0.50, "target_valence": 0.50, "target_danceability": 0.50,
        "target_acousticness": 0.50, "target_tempo_bpm": 110,
        "target_instrumentalness": 0.50, "target_speechiness": 0.50,
    },
}


def print_recommendations(name: str, profile: dict, songs: list) -> None:
    recommendations = recommend_songs(profile, songs, k=5)
    print(f"\n=== Profile: {name} "
          f"({profile['favorite_genre']} / {profile['favorite_mood']}) ===")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"#{rank}  {song['title']} - {song['artist']}")
        print(f"    Score: {score:.2f}")
        print("    Reasons:")
        for reason in explanation.split("; "):
            print(f"      - {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")
    for name, profile in PROFILES.items():
        print_recommendations(name, profile, songs)


if __name__ == "__main__":
    main()
