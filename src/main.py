"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    # Display user profile
    print("\n" + "="*80)
    print("🎵 MUSIC RECOMMENDER SIMULATION")
    print("="*80)
    print(f"\n📋 Your Profile:")
    print(f"   • Favorite Genre: {user_prefs['genre'].upper()}")
    print(f"   • Favorite Mood: {user_prefs['mood'].upper()}")
    print(f"   • Target Energy: {user_prefs['energy']}")
    
    print(f"\n🏆 Top {len(recommendations)} Recommendations:\n")
    print("-"*80)
    
    for idx, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        artist = song.get('artist', 'Unknown Artist')
        
        print(f"\n#{idx} {song['title']}")
        print(f"    Artist: {artist}")
        print(f"    Score: {score:.2f}/4.5 ⭐")
        print(f"    Why: {explanation}")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
