"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Taste profile: pop / happy cluster
    user_profile = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "target_valence": 0.85,
        "target_danceability": 0.80,
        "target_acousticness": 0.15,
        "target_tempo_bpm": 120,
        "target_instrumentalness": 0.05,
        "target_speechiness": 0.06,
    }

    recommendations = recommend_songs(user_profile, songs, k=5)

    print(f"\nTop {len(recommendations)} recommendations "
          f"for {user_profile['favorite_genre']} / {user_profile['favorite_mood']}:\n")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"#{rank}  {song['title']} - {song['artist']}")
        print(f"    Score: {score:.2f}")
        print("    Reasons:")
        for reason in explanation.split("; "):
            print(f"      - {reason}")
        print()


if __name__ == "__main__":
    main()
