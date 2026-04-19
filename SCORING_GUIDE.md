# Music Recommender Scoring System - Implementation Guide

## Overview

This document provides a complete mathematical and computational guide for building a music recommender system with energy and mood-based scoring. The system evaluates songs using two key features:

1. **Energy**: A numerical value [0.0, 1.0] representing song intensity
2. **Mood**: A categorical value representing emotional tone

---

## Part 1: Energy Scoring

### Mathematical Formulation

We use two different approaches, both normalizing the score to [0, 1]:

#### Option A: Linear Penalty (Absolute Difference)

**Formula:**
$$\text{energy\_score} = 1 - |\text{song.energy} - \text{user.target\_energy}|$$

**Characteristics:**
- Simple and intuitive
- Linear penalty: doubling the distance doubles the penalty
- Equally penalizes small and large deviations
- Range: [0, 1] (always normalized)

**When to use:**
- General recommendations where all distances matter equally
- Simple linear matching preferred

**Examples:**
- Song energy: 0.8, Target: 0.8 → Score: 1.0 - 0 = **1.0** (perfect)
- Song energy: 0.7, Target: 0.8 → Score: 1.0 - 0.1 = **0.9** (close)
- Song energy: 0.5, Target: 0.8 → Score: 1.0 - 0.3 = **0.7** (moderate)
- Song energy: 0.2, Target: 0.8 → Score: 1.0 - 0.6 = **0.4** (poor)

#### Option B: Quadratic Penalty (Squared Difference)

**Formula:**
$$\text{energy\_score} = 1 - (\text{song.energy} - \text{user.target\_energy})^2$$

**Characteristics:**
- Creates a "sweet spot" around the target
- More forgiving for small differences
- Harsher penalty for large deviations (quadratic growth)
- Range: [0, 1] (always normalized)
- Produces more selective recommendations

**When to use:**
- When you want stricter matching around target energy
- Fitness apps (precise workout intensity matching)
- Mood-sensitive scenarios

**Examples:**
- Song energy: 0.8, Target: 0.8 → Score: 1.0 - (0)² = **1.0** (perfect)
- Song energy: 0.75, Target: 0.8 → Score: 1.0 - (0.05)² = **0.9975** (very close)
- Song energy: 0.7, Target: 0.8 → Score: 1.0 - (0.1)² = **0.99** (close, better than linear)
- Song energy: 0.5, Target: 0.8 → Score: 1.0 - (0.3)² = **0.91** (moderate, better than linear)
- Song energy: 0.2, Target: 0.8 → Score: 1.0 - (0.6)² = **0.64** (poor, worse than linear)

### Python Implementation

```python
def score_energy_linear(song_energy: float, target_energy: float) -> float:
    """Score energy using absolute difference (linear penalty)."""
    return 1.0 - abs(song_energy - target_energy)

def score_energy_quadratic(song_energy: float, target_energy: float) -> float:
    """Score energy using squared difference (quadratic penalty)."""
    diff = song_energy - target_energy
    return 1.0 - (diff * diff)
```

---

## Part 2: Mood Scoring

### Mood Categories

Six mood categories used in the system:
- **happy**: Upbeat, positive, energetic
- **chill**: Relaxed, low-energy, atmospheric
- **intense**: High-energy, aggressive, powerful
- **relaxed**: Calm, soothing, meditative
- **moody**: Emotional, contemplative, introspective
- **focused**: Productive, concentration-enhancing, structured

### Similarity Matrix

**6×6 Mood Similarity Matrix:**

```
         happy  chill  intense  relaxed  moody  focused
happy     1.0    0.0     0.0     0.0     0.0    0.6
chill     0.0    1.0     0.0     0.8     0.0    0.0
intense   0.0    0.0     1.0     0.0     0.5    0.0
relaxed   0.0    0.8     0.0     1.0     0.0    0.0
moody     0.0    0.0     0.5     0.0     1.0    0.0
focused   0.6    0.0     0.0     0.0     0.0    1.0
```

### Scoring Logic

**Formula:**
$$\text{mood\_score} = \text{MOOD\_SIMILARITY}[\text{song.mood}][\text{user.favorite\_mood}]$$

**Score Levels:**

| Similarity | Score | Meaning | Example |
|-----------|-------|---------|----------|\n| Exact match | 1.0 | Full credit | "happy" user → "happy" song |
| Related moods | 0.8 | High partial credit | "chill" user → "relaxed" song |
| Similar moods | 0.6 | Medium partial credit | "happy" user → "focused" song |
| Somewhat related | 0.5 | Low partial credit | "intense" user → "moody" song |
| Unrelated moods | 0.0 | No credit | "happy" user → "intense" song |

### Python Implementation

```python
MOOD_SIMILARITY = {
    # Exact matches
    ("happy", "happy"): 1.0,
    ("chill", "chill"): 1.0,
    ("intense", "intense"): 1.0,
    ("relaxed", "relaxed"): 1.0,
    ("moody", "moody"): 1.0,
    ("focused", "focused"): 1.0,
    
    # Related moods
    ("chill", "relaxed"): 0.8,
    ("relaxed", "chill"): 0.8,
    ("happy", "focused"): 0.6,
    ("focused", "happy"): 0.6,
    ("intense", "moody"): 0.5,
    ("moody", "intense"): 0.5,
}

def score_mood(song_mood: str, favorite_mood: str) -> float:
    """Score mood based on similarity matrix."""
    return MOOD_SIMILARITY.get((song_mood, favorite_mood), 0.0)
```

---

## Part 3: Combined Scoring

### Mathematical Formulation

**Weighted Addition Formula:**
$$\text{total\_score} = (w_e \times \text{energy\_score}) + (w_m \times \text{mood\_score})$$

**Default (60/40 split):**
$$\text{total\_score} = (0.6 \times \text{energy\_score}) + (0.4 \times \text{mood\_score})$$

### Normalization Proof

Since:
- 0 ≤ energy_score ≤ 1
- 0 ≤ mood_score ≤ 1
- weights sum to 1.0

Therefore: **0 ≤ total_score ≤ 1** ✓

### Python Implementation

```python
def score_song(
    song: Song,
    user: UserProfile,
    energy_weight: float = 0.6,
    mood_weight: float = 0.4,
    energy_method: str = "quadratic"
) -> float:
    """Calculate comprehensive recommendation score."""
    
    # Validate weights
    assert abs(energy_weight + mood_weight - 1.0) < 1e-6
    
    # Calculate component scores
    if energy_method == "linear":
        energy_score = score_energy_linear(song.energy, user.target_energy)
    else:
        energy_score = score_energy_quadratic(song.energy, user.target_energy)
    
    mood_score = score_mood(song.mood, user.favorite_mood)
    
    # Weighted combination
    total_score = (energy_weight * energy_score) + (mood_weight * mood_score)
    
    return total_score
```

---

## Quick Start Example

```python
from src.recommender import Song, UserProfile, score_song

# Create a song
song = Song(
    id=1,
    title="Upbeat Morning",
    artist="Joy Makers",
    genre="pop",
    mood="happy",
    energy=0.8,
    tempo_bpm=120,
    valence=0.8,
    danceability=0.7,
    acousticness=0.2
)

# Create user profile
user = UserProfile(
    favorite_genre="pop",
    favorite_mood="happy",
    target_energy=0.8,
    likes_acoustic=False
)

# Score the song
score = score_song(song, user, energy_method="quadratic")
print(f"Recommendation Score: {score:.2%}")  # 100.00%
```

---

## Score Interpretation

| Score Range | Interpretation | Level |
|-------------|-----------------|-------|
| 0.85 - 1.0 | Excellent match | ⭐⭐⭐⭐⭐ |
| 0.70 - 0.85 | Good match | ⭐⭐⭐⭐ |
| 0.50 - 0.70 | Fair match | ⭐⭐⭐ |
| 0.30 - 0.50 | Poor match | ⭐⭐ |
| 0.0 - 0.30 | Very poor match | ⭐ |

---

## Files in This Project

- **`src/recommender.py`** - Complete implementation with all scoring functions
- **`Music_Recommender_Scoring.ipynb`** - Interactive notebook with examples and visualizations
- **`SCORING_GUIDE.md`** - This comprehensive guide (mathematical + implementation)
