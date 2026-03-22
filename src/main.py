"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

Recommender logic is in recommender.py: load_songs, score_song, recommend_songs.
"""

try:
    from recommender import load_songs, recommend_songs
except ImportError:
    from src.recommender import load_songs, recommend_songs


def main() -> None:
    """Load songs, score them for a sample user, and print top recommendations."""
    songs = load_songs("data/songs.csv")

    user_prefs = {"genre": "pop", "mood": "happy", "target_energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations\n")
    print("-" * 40)
    for song, score, reasons in recommendations:
        print(f"\n{song['title']}")
        print(f"  Final score: {score:.2f}")
        print("  Reasons:")
        if reasons:
            for line in reasons:
                print(f"    • {line}")
        else:
            print("    (no matching signals)")
        print()


if __name__ == "__main__":
    main()
