# Music Recommender System - Quick Reference

## Mathematical Formulas Summary

### 1. Energy Scoring

#### Linear Penalty
```
energy_score = 1 - |song.energy - user.target_energy|

Example: song=0.7, target=0.8 → 1 - 0.1 = 0.9
```

#### Quadratic Penalty
```
energy_score = 1 - (song.energy - user.target_energy)²

Example: song=0.7, target=0.8 → 1 - (0.1)² = 0.99
```

### 2. Mood Scoring

```
mood_score = MOOD_SIMILARITY[song.mood][user.favorite_mood]

Exact match:        1.0
Related moods:      0.5 - 0.8
Unrelated moods:    0.0
```

### 3. Combined Score (Default: 60% Energy, 40% Mood)

```
total_score = (0.6 × energy_score) + (0.4 × mood_score)

Result always in [0, 1]
```

---

## Mood Similarity Matrix

| From ↓ / To → | happy | chill | intense | relaxed | moody | focused |
|---|---|---|---|---|---|---|
| **happy** | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.6 |
| **chill** | 0.0 | 1.0 | 0.0 | 0.8 | 0.0 | 0.0 |
| **intense** | 0.0 | 0.0 | 1.0 | 0.0 | 0.5 | 0.0 |
| **relaxed** | 0.0 | 0.8 | 0.0 | 1.0 | 0.0 | 0.0 |
| **moody** | 0.0 | 0.0 | 0.5 | 0.0 | 1.0 | 0.0 |
| **focused** | 0.6 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 |

**Key Relationships:**
- Calm pair: chill ↔ relaxed (0.8)
- Energetic pair: happy ↔ focused (0.6)
- Emotional pair: intense ↔ moody (0.5)
- Unrelated: all others (0.0)

---

## Python Quick Start

```python
from src.recommender import Song, UserProfile, score_song

# Define a song
song = Song(
    id=1, title="Example Song", artist="Artist",
    genre="pop", mood="happy", energy=0.8,
    tempo_bpm=120, valence=0.8, danceability=0.7, acousticness=0.2
)

# Define user profile
user = UserProfile(
    favorite_genre="pop",
    favorite_mood="happy",
    target_energy=0.8,
    likes_acoustic=False
)

# Score the song
score = score_song(
    song=song,
    user=user,
    energy_weight=0.6,      # 60% weight
    mood_weight=0.4,        # 40% weight
    energy_method="quadratic"  # or "linear"
)

print(f"Score: {score:.4f}")  # Output: 1.0000 (perfect match)
print(f"Percentage: {score*100:.1f}%")  # Output: 100.0%
```

---

## Examples: Different Scoring Scenarios

### Scenario 1: Perfect Match
**Song:** energy=0.8, mood=happy  
**User:** target_energy=0.8, favorite_mood=happy  
**Calculation:**
- energy_score = 1 - 0² = 1.0
- mood_score = 1.0 (exact match)
- total = 0.6(1.0) + 0.4(1.0) = **1.0** ✅

### Scenario 2: Energy Match, Mood Mismatch
**Song:** energy=0.8, mood=intense  
**User:** target_energy=0.8, favorite_mood=happy  
**Calculation:**
- energy_score = 1.0
- mood_score = 0.0 (unrelated)
- total = 0.6(1.0) + 0.4(0.0) = **0.60** ⚠️

### Scenario 3: Energy Mismatch, Related Mood
**Song:** energy=0.3, mood=chill  
**User:** target_energy=0.8, favorite_mood=happy  
**Calculation:**
- energy_score = 1 - (0.5)² = 0.75
- mood_score = 0.0 (unrelated)
- total = 0.6(0.75) + 0.4(0.0) = **0.45** ⚠️

### Scenario 4: Everything Aligned
**Song:** energy=0.80, mood=focused  
**User:** target_energy=0.80, favorite_mood=happy  
**Calculation:**
- energy_score = 1.0 (perfect)
- mood_score = 0.6 (related: focused ~ happy)
- total = 0.6(1.0) + 0.4(0.6) = **0.84** ⭐

---

## Implementation Details

### Key Functions in `src/recommender.py`

1. **`score_energy_linear(song_energy, target_energy)`**
   - Returns: float in [0, 1]
   - Use: General recommendations

2. **`score_energy_quadratic(song_energy, target_energy)`**
   - Returns: float in [0, 1]
   - Use: Selective recommendations with sweet-spot preference

3. **`score_mood(song_mood, favorite_mood)`**
   - Returns: float in [0, 1]
   - Lookup from MOOD_SIMILARITY dictionary

4. **`score_song(song, user, energy_weight=0.6, mood_weight=0.4, energy_method="quadratic")`**
   - Returns: float in [0, 1]
   - Main scoring function combining all components

### Constants

**`MOOD_SIMILARITY`** - Dictionary mapping (mood1, mood2) pairs to similarity scores

---

## Customization Guide

### Change Energy Weight
```python
# More energy-focused (80/20)
score_song(song, user, energy_weight=0.8, mood_weight=0.2)

# Balanced (50/50)
score_song(song, user, energy_weight=0.5, mood_weight=0.5)

# More mood-focused (40/60)
score_song(song, user, energy_weight=0.4, mood_weight=0.6)
```

### Switch Energy Method
```python
# Use linear instead of quadratic
score_song(song, user, energy_method="linear")
```

### Update Mood Relationships
```python
from src.recommender import MOOD_SIMILARITY

# Add new relationship
MOOD_SIMILARITY[("happy", "relaxed")] = 0.5

# Modify existing relationship
MOOD_SIMILARITY[("chill", "relaxed")] = 0.9  # Increase similarity
```

---

## Score Ranges & Interpretation

| Range | Interpretation | Usage |
|-------|---|---|
| 0.90-1.00 | ⭐⭐⭐⭐⭐ Excellent | Top recommendations |
| 0.70-0.89 | ⭐⭐⭐⭐ Good | Strong recommendations |
| 0.50-0.69 | ⭐⭐⭐ Fair | Include in results |
| 0.30-0.49 | ⭐⭐ Poor | Marginal matches |
| 0.00-0.29 | ⭐ Very Poor | Don't recommend |

---

## Common Use Cases

### Top-K Recommendations
```python
# Get top 5 songs for a user
scores = [(song, score_song(song, user)) for song in song_library]
scores.sort(key=lambda x: x[1], reverse=True)
top_5 = [song for song, _ in scores[:5]]
```

### Threshold Filtering
```python
# Only recommend songs above 70% match
good_songs = [song for song in song_library 
              if score_song(song, user) > 0.7]
```

### Ranked List with Scores
```python
# Return sorted list with scores
recommendations = [(song, score_song(song, user)) 
                   for song in song_library]
recommendations.sort(key=lambda x: x[1], reverse=True)

for song, score in recommendations[:10]:
    print(f"{song.title}: {score*100:.1f}%")
```

---

## Files Reference

| File | Purpose |
|------|---------|
| `src/recommender.py` | Main implementation with all scoring functions |
| `Music_Recommender_Scoring.ipynb` | Interactive notebook with examples & visualizations |
| `SCORING_GUIDE.md` | Comprehensive mathematical guide |
| `QUICK_REFERENCE.md` | This file - quick lookup |

---

## Testing Your Implementation

```python
from src.recommender import Song, UserProfile, score_song

# Test 1: Perfect match
song1 = Song(1, "Perfect", "Artist", "pop", "happy", 0.8, 120, 0.8, 0.7, 0.2)
user1 = UserProfile("pop", "happy", 0.8, False)
assert score_song(song1, user1) == 1.0, "Perfect match should score 1.0"
print("✓ Test 1 passed")

# Test 2: Complete mismatch
song2 = Song(2, "Wrong", "Artist", "metal", "intense", 0.1, 160, 0.2, 0.8, 0.1)
user2 = UserProfile("pop", "happy", 0.9, True)
score2 = score_song(song2, user2)
assert 0.0 <= score2 < 0.5, "Mismatch should score < 0.5"
print("✓ Test 2 passed")

# Test 3: Output range
for i in range(100):
    song = Song(i, f"Song {i}", "Artist", "pop", 
                ["happy", "chill", "intense"][i%3], i/100, 100+i, 0.5, 0.5, 0.5)
    user = UserProfile("pop", "happy", 0.5, False)
    score = score_song(song, user)
    assert 0.0 <= score <= 1.0, f"Score out of range: {score}"
print("✓ Test 3 passed - All 100 scores in valid range")
```

---

## Next Steps

1. ✅ Review the mathematical formulas above
2. ✅ Examine `src/recommender.py` implementation
3. ✅ Run the interactive notebook: `Music_Recommender_Scoring.ipynb`
4. ✅ Test with your data in `data/songs.csv`
5. ✅ Implement `recommend()` in the `Recommender` class
6. ✅ Integrate into your main application

---

**Created:** March 21, 2026  
**System:** Music Recommender v1.0  
**Status:** Ready for production ✅
