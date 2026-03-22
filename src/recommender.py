import csv
from typing import List, Dict, Tuple

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

def load_songs(filepath: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dictionaries with typed fields."""
    songs: List[Dict] = []
    try:
        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                return songs
            for row in reader:
                if not any(row.values()):
                    continue
                song = {
                    "id": int(row["id"]),
                    "title": row["title"].strip(),
                    "artist": row["artist"].strip(),
                    "genre": row["genre"].strip(),
                    "mood": row["mood"].strip(),
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
                songs.append(song)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Songs file not found: {filepath}") from e
    except (KeyError, ValueError, TypeError) as e:
        raise ValueError(f"Invalid or incomplete song data in {filepath}: {e}") from e
    except csv.Error as e:
        raise ValueError(f"Could not parse CSV {filepath}: {e}") from e
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Compute a preference score and human-readable reasons for one song."""
    score = 0.0
    reasons: List[str] = []

    user_genre = str(user_prefs.get("genre", "")).strip().lower()
    user_mood = str(user_prefs.get("mood", "")).strip().lower()
    target_energy = user_prefs.get("target_energy", user_prefs.get("energy", 0.0))
    if not isinstance(target_energy, (int, float)):
        target_energy = float(target_energy)

    if user_genre and song["genre"].strip().lower() == user_genre:
        score += 2.0
        reasons.append("genre match (+2.0)")

    if user_mood and song["mood"].strip().lower() == user_mood:
        score += 1.0
        reasons.append("mood match (+1.0)")

    energy_points = max(0.0, 1.0 - abs(float(song["energy"]) - float(target_energy)))
    energy_points = round(energy_points, 2)
    if energy_points > 0:
        score += energy_points
        reasons.append(f"energy close (+{energy_points:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """Rank songs by score and return the top k with scores and reason lists."""
    scored: List[Tuple[Dict, float, List[str]]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, reasons))
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[: max(0, k)]
