from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

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


# ============================================================================
# MOOD SIMILARITY MATRIX - Defines relationships between mood categories
# ============================================================================

MOOD_SIMILARITY = {
    # Exact matches (diagonal)
    ("happy", "happy"): 1.0,
    ("chill", "chill"): 1.0,
    ("intense", "intense"): 1.0,
    ("relaxed", "relaxed"): 1.0,
    ("moody", "moody"): 1.0,
    ("focused", "focused"): 1.0,
    
    # Related calm moods: chill ↔ relaxed (0.8 similarity)
    ("chill", "relaxed"): 0.8,
    ("relaxed", "chill"): 0.8,
    
    # Related energetic moods: happy ↔ focused (0.6 similarity)
    ("happy", "focused"): 0.6,
    ("focused", "happy"): 0.6,
    
    # Intense moods somewhat related: intense ↔ moody (0.5 similarity)
    ("intense", "moody"): 0.5,
    ("moody", "intense"): 0.5,
    
    # All unspecified pairs get 0.0 (no credit for unrelated moods)
}


def get_mood_similarity(song_mood: str, favorite_mood: str) -> float:
    """
    Returns the similarity score between two mood strings.
    
    Args:
        song_mood: The mood of the song
        favorite_mood: The user's favorite mood
        
    Returns:
        A float in [0, 1] representing how similar the moods are
    """
    return MOOD_SIMILARITY.get((song_mood, favorite_mood), 0.0)

# ============================================================================
# ENERGY SCORING - Two approaches for scoring song energy vs user target
# ============================================================================

def score_energy_linear(song_energy: float, target_energy: float) -> float:
    """
    Score energy using absolute difference (linear penalty).
    
    Formula: energy_score = 1 - |song.energy - target_energy|
    
    Args:
        song_energy: The song's energy level [0.0, 1.0]
        target_energy: The user's target energy level [0.0, 1.0]
        
    Returns:
        Score in [0.0, 1.0] where 1.0 is perfect match
    """
    return 1.0 - abs(song_energy - target_energy)


def score_energy_quadratic(song_energy: float, target_energy: float) -> float:
    """
    Score energy using squared difference (quadratic penalty).
    
    Formula: energy_score = 1 - (song.energy - target_energy)^2
    
    More forgiving for small differences, harsher for large ones.
    This creates a "sweet spot" effect.
    
    Args:
        song_energy: The song's energy level [0.0, 1.0]
        target_energy: The user's target energy level [0.0, 1.0]
        
    Returns:
        Score in [0.0, 1.0] where 1.0 is perfect match
    """
    diff = song_energy - target_energy
    return 1.0 - (diff * diff)


# ============================================================================
# MOOD SCORING - Categorical mood matching with partial credit
# ============================================================================

def score_mood(song_mood: str, favorite_mood: str) -> float:
    """
    Score mood based on similarity to user's favorite mood.
    
    Formula:
        mood_score = 1.0 if exact match
                   = w_related if related moods (defined in MOOD_SIMILARITY)
                   = 0.0 otherwise
    
    Args:
        song_mood: The song's mood (string)
        favorite_mood: The user's favorite mood (string)
        
    Returns:
        Score in [0.0, 1.0]
    """
    return get_mood_similarity(song_mood, favorite_mood)


# ============================================================================
# COMBINED SCORING - Weighted combination of energy and mood
# ============================================================================

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Score a single song against user preferences using the Algorithm Recipe.
    
    ALGORITHM RECIPE:
    - Genre match: +2.0 points
    - Mood match: +1.0 point
    - Energy similarity: up to +1.0 point (based on closeness to target energy)
    - Bonus: Acousticness bonus up to +0.5 points (if user likes acoustic songs)
    
    Args:
        user_prefs: Dict with keys 'genre', 'mood', 'energy' (and optionally 'likes_acoustic')
                   Example: {"genre": "pop", "mood": "happy", "energy": 0.8}
        song: Dict with song data from CSV (including 'genre', 'mood', 'energy', etc.)
    
    Returns:
        Tuple of (score: float, reasons: List[str])
        - score: Total points (0.0 to 4.5+)
        - reasons: List of explanation strings for transparency
    
    Example:
        score, reasons = score_song(
            {"genre": "pop", "mood": "happy", "energy": 0.8},
            {"genre": "pop", "mood": "happy", "energy": 0.82, "title": "Sunrise City", ...}
        )
        # Returns: (4.98, ["Genre match: pop (+2.0)", "Mood match: happy (+1.0)", ...])
    """
    score = 0.0
    reasons = []
    
    # Extract user preferences
    user_genre = user_prefs.get("genre", "").lower().strip()
    user_mood = user_prefs.get("mood", "").lower().strip()
    user_energy = user_prefs.get("energy", 0.5)
    likes_acoustic = user_prefs.get("likes_acoustic", False)
    
    # Extract song attributes
    song_genre = song.get("genre", "").lower().strip()
    song_mood = song.get("mood", "").lower().strip()
    song_energy = float(song.get("energy", 0.5))
    song_acousticness = float(song.get("acousticness", 0.0))
    song_title = song.get("title", "Unknown")
    
    # ========== SCORING LOGIC ==========
    
    # 1. GENRE MATCH: +2.0 points for exact match
    if user_genre and song_genre == user_genre:
        score += 2.0
        reasons.append(f"Genre match: {song_genre} (+2.0)")
    
    # 2. MOOD MATCH: +1.0 point for exact match
    if user_mood and song_mood == user_mood:
        score += 1.0
        reasons.append(f"Mood match: {song_mood} (+1.0)")
    
    # 3. ENERGY SIMILARITY: up to +1.0 point based on distance
    #    Score = 1.0 - |song_energy - user_energy|
    #    If energy matches exactly, +1.0. If off by 0.5, +0.5, etc.
    energy_distance = abs(song_energy - user_energy)
    energy_points = max(0.0, 1.0 - energy_distance)
    score += energy_points
    reasons.append(f"Energy similarity (target: {user_energy}, song: {song_energy}) (+{energy_points:.2f})")
    
    # 4. BONUS: ACOUSTICNESS
    #    If user likes acoustic music, reward high acousticness
    if likes_acoustic and song_acousticness >= 0.5:
        acoustic_bonus = song_acousticness * 0.5  # up to +0.5
        score += acoustic_bonus
        reasons.append(f"Acoustic bonus (acousticness: {song_acousticness:.2f}) (+{acoustic_bonus:.2f})")
    
    return score, reasons


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file and converts numerical values to appropriate types.
    
    Args:
        csv_path: Path to the CSV file (e.g., "data/songs.csv")
    
    Returns:
        A list of dictionaries, one per song, with numerical fields converted to float/int.
        
    Example:
        songs = load_songs("data/songs.csv")
        # Returns: [
        #   {'id': 1, 'title': 'Sunrise City', 'artist': 'Neon Echo', ..., 'energy': 0.82, 'tempo_bpm': 118},
        #   ...
        # ]
    """
    songs = []
    
    # Fields that should be converted to floats (for math operations)
    float_fields = {'energy', 'valence', 'danceability', 'acousticness', 'tempo_bpm'}
    
    # Fields that should be converted to integers
    int_fields = {'id', 'tempo_bpm'}
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numerical fields
                for field in float_fields:
                    if field in row and row[field]:
                        row[field] = float(row[field])
                
                # tempo_bpm should be integer (already converted to float above, so cast to int)
                if 'tempo_bpm' in row:
                    row['tempo_bpm'] = int(float(row['tempo_bpm']))
                
                # id should be integer
                if 'id' in row:
                    row['id'] = int(row['id'])
                
                songs.append(row)
        
        print(f"✓ Loaded {len(songs)} songs from {csv_path}")
        return songs
    
    except FileNotFoundError:
        print(f"✗ Error: Could not find file {csv_path}")
        return []
    except Exception as e:
        print(f"✗ Error loading songs: {e}")
        return []

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Recommends the top k songs for a user based on their preferences.
    
    Algorithm:
    1. Score every song in the catalog using score_song()
    2. Sort all scored songs by score (highest first)
    3. Return the top k results with explanations
    
    Args:
        user_prefs: User preferences dict with keys 'genre', 'mood', 'energy'
        songs: List of song dicts loaded from CSV
        k: Number of recommendations to return (default 5)
    
    Returns:
        List of tuples: [(song_dict, score, explanation), ...]
        - Sorted from highest to lowest score
        - Limited to k results
        - explanation is a formatted string joining all reasons
    
    Example:
        recommendations = recommend_songs(
            {"genre": "pop", "mood": "happy", "energy": 0.8},
            songs,
            k=5
        )
        # Returns: [
        #   (song1_dict, 4.98, "Genre match: pop (+2.0). Mood match: happy (+1.0). ..."),
        #   (song2_dict, 3.45, "Energy similarity (target: 0.8, song: 0.75) (+0.75). ..."),
        #   ...
        # ]
    """
    # Step 1: Score every song
    # Create a list of tuples: (song, score, reasons_list)
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored_songs.append((song, score, reasons))
    
    # Step 2: Sort by score (highest first) using sorted() - returns new list
    # sorted() is preferred over .sort() because:
    # - It returns a NEW sorted list (non-destructive)
    # - We can chain operations: sorted(..., key=..., reverse=True)
    # - It works on any iterable, not just lists
    # - .sort() modifies the list in-place, which can be dangerous
    ranked_songs = sorted(scored_songs, key=lambda x: x[1], reverse=True)
    
    # Step 3: Take top k and format with explanations
    recommendations = []
    for song, score, reasons in ranked_songs[:k]:
        # Join all reasons into a single readable explanation
        explanation = " | ".join(reasons)
        recommendations.append((song, score, explanation))
    
    return recommendations
