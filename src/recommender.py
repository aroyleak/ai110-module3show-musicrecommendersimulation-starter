from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

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

def score_song(
    song: Song,
    user: UserProfile,
    energy_weight: float = 0.6,
    mood_weight: float = 0.4,
    energy_method: str = "quadratic"
) -> float:
    """
    Calculate a comprehensive recommendation score for a song given a user profile.
    
    Formula (default weights):
        total_score = (0.6 × energy_score) + (0.4 × mood_score)
    
    Args:
        song: A Song object with 'energy' (float) and 'mood' (str) fields
        user: A UserProfile object with 'target_energy' (float) and 'favorite_mood' (str) fields
        energy_weight: Weight for energy component (default 0.6)
        mood_weight: Weight for mood component (default 0.4)
        energy_method: "linear" or "quadratic" scoring for energy (default "quadratic")
        
    Returns:
        A score in [0.0, 1.0] where 1.0 is the best possible recommendation
        
    Raises:
        ValueError: If energy_method is not "linear" or "quadratic"
        AssertionError: If weights don't sum to 1.0 (with small tolerance for float precision)
    """
    # Validate inputs
    assert abs(energy_weight + mood_weight - 1.0) < 1e-6, \
        f"Weights must sum to 1.0, got {energy_weight + mood_weight}"
    
    if energy_method not in ("linear", "quadratic"):
        raise ValueError(f"energy_method must be 'linear' or 'quadratic', got '{energy_method}'")
    
    # Calculate component scores
    if energy_method == "linear":
        energy_score = score_energy_linear(song.energy, user.target_energy)
    else:  # quadratic
        energy_score = score_energy_quadratic(song.energy, user.target_energy)
    
    mood_score = score_mood(song.mood, user.favorite_mood)
    
    # Weighted combination
    total_score = (energy_weight * energy_score) + (mood_weight * mood_score)
    
    return total_score


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
    Loads songs from a CSV file.
    Required by src/main.py
    """
    # TODO: Implement CSV loading logic
    print(f"Loading songs from {csv_path}...")
    return []

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    return []
