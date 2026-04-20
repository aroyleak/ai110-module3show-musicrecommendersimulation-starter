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
    
    # Define three distinct user preference profiles
    profiles = {
        "High-Energy Pop": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.9
        },
        "Chill Lofi": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.4,
            "likes_acoustic": True
        },
        "Deep Intense Rock": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.9
        }
    }
    
    # Run recommender for each profile
    for profile_name, user_prefs in profiles.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        # Display user profile
        print("\n" + "="*80)
        print(f"🎵 MUSIC RECOMMENDER SIMULATION - {profile_name}")
        print("="*80)
        print(f"\n📋 Your Profile:")
        print(f"   • Favorite Genre: {user_prefs['genre'].upper()}")
        print(f"   • Favorite Mood: {user_prefs['mood'].upper()}")
        print(f"   • Target Energy: {user_prefs['energy']}")
        if user_prefs.get('likes_acoustic'):
            print(f"   • Likes Acoustic: YES")
        
        print(f"\n🏆 Top {len(recommendations)} Recommendations:\n")
        print("-"*80)
        
        for idx, rec in enumerate(recommendations, 1):
            song, score, explanation = rec
            artist = song.get('artist', 'Unknown Artist')
            
            print(f"\n#{idx} {song['title']}")
            print(f"    Artist: {artist}")
            print(f"    Genre: {song.get('genre', 'Unknown').upper()}")
            print(f"    Score: {score:.2f}/4.5 ⭐")
            print(f"    Why: {explanation}")
        
        print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
