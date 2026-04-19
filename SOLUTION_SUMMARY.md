# Solution Summary: Music Recommender Scoring System

## What You Asked For

You requested a **math-based scoring system** for a music recommender that:
1. Scores songs based on **energy** proximity (not just high/low, but matching a target)
2. Scores songs based on **mood** similarity (exact or partial matches)
3. Combines both into a single **total score** using weights
4. Shows formulas mathematically AND implements them in Python

---

## What You Got

### ✅ Mathematical Formulas

#### Energy Scoring (Two Options)

**Option A - Linear Penalty:**
```
Formula: energy_score = 1 - |song.energy - user.target_energy|
Range:   [0, 1]
Use:     Simple, linear distance penalty
```

**Option B - Quadratic Penalty:**
```
Formula: energy_score = 1 - (song.energy - user.target_energy)²
Range:   [0, 1]
Use:     Sweet-spot matching, more selective
```

#### Mood Scoring

```
mood_score = MOOD_SIMILARITY[song.mood][user.favorite_mood]

Values:
  - 1.0 for exact match
  - 0.5-0.8 for related moods
  - 0.0 for unrelated moods
```

**Mood Relationships Defined:**
- `chill ↔ relaxed` = 0.8 (calm moods)
- `happy ↔ focused` = 0.6 (energetic moods)
- `intense ↔ moody` = 0.5 (emotional moods)
- All others = 0.0

#### Combined Score

```
total_score = (0.6 × energy_score) + (0.4 × mood_score)

Default: 60% energy weight, 40% mood weight
Result:  Always in [0, 1]
```

---

### ✅ Python Implementation

Complete code in `src/recommender.py`:

```python
# Energy scoring functions
def score_energy_linear(song_energy: float, target_energy: float) -> float
def score_energy_quadratic(song_energy: float, target_energy: float) -> float

# Mood scoring
MOOD_SIMILARITY = { ... }  # 6×6 similarity matrix
def get_mood_similarity(song_mood: str, favorite_mood: str) -> float
def score_mood(song_mood: str, favorite_mood: str) -> float

# Combined scoring (main function)
def score_song(
    song: Song,
    user: UserProfile,
    energy_weight: float = 0.6,
    mood_weight: float = 0.4,
    energy_method: str = "quadratic"
) -> float
```

**Function Signature Matches Your Request:**
```python
def score_song(song: Song, user: UserProfile) -> float:
    # Returns a float in [0, 1]
```

---

## Complete Example

```python
from src.recommender import Song, UserProfile, score_song

# Create a song
song = Song(
    id=1,
    title="Upbeat Morning",
    artist="Joy Makers",
    genre="pop",
    mood="happy",        # ← Categorical mood
    energy=0.8,          # ← Numerical energy [0-1]
    tempo_bpm=120,
    valence=0.8,
    danceability=0.7,
    acousticness=0.2
)

# Create user profile
user = UserProfile(
    favorite_genre="pop",
    favorite_mood="happy",      # ← Categorical mood preference
    target_energy=0.8,          # ← Numerical energy target [0-1]
    likes_acoustic=False
)

# Score the song
score = score_song(song, user, energy_method="quadratic")

# Result: 1.0 (perfect 100% match)
#   - Energy: 1.0 (0.8 vs 0.8 target) ✓
#   - Mood: 1.0 (happy vs happy) ✓
#   - Combined: 0.6(1.0) + 0.4(1.0) = 1.0 ✓
```

---

## Scoring Examples

### Example 1: Perfect Match
- Song: energy=0.8, mood=happy
- User: target_energy=0.8, favorite_mood=happy
- **Score: 1.0** (100%) ⭐⭐⭐⭐⭐

### Example 2: Energy Match, Mood Mismatch
- Song: energy=0.8, mood=intense
- User: target_energy=0.8, favorite_mood=happy
- **Score: 0.6** (60%) ⭐⭐

### Example 3: Energy Mismatch, Related Mood
- Song: energy=0.3, mood=focused
- User: target_energy=0.8, favorite_mood=happy
- **Calculation:** 0.6(0.75) + 0.4(0.6) = 0.69
- **Score: 0.69** (69%) ⭐⭐⭐

### Example 4: Everything Aligned
- Song: energy=0.80, mood=focused
- User: target_energy=0.80, favorite_mood=happy
- **Calculation:** 0.6(1.0) + 0.4(0.6) = 0.84
- **Score: 0.84** (84%) ⭐⭐⭐⭐

---

## Key Design Decisions

### Why 60% Energy / 40% Mood?

| Weight | Reason |
|--------|--------|
| **60% Energy** | Objective, measurable, critical for matching use case (workout, focus, etc.) |
| **40% Mood** | Important but secondary; users more flexible with mood |

*Customizable: Use `energy_weight` and `mood_weight` parameters to adjust*

### Why Two Energy Methods?

| Method | When to Use |
|--------|-------------|
| **Linear** | General recommendations, all distances matter equally |
| **Quadratic** | Selective recommendations, want "sweet spot" around target |

---

## Deliverables

### 📄 Documentation Files (NEW)

| File | Purpose |
|------|---------|
| `SCORING_GUIDE.md` | Comprehensive mathematical guide with all formulas |
| `QUICK_REFERENCE.md` | Quick lookup guide and usage patterns |
| `IMPLEMENTATION_DETAILS.md` | Complete technical documentation |

### 💻 Implementation Files (UPDATED)

| File | Changes |
|------|---------|
| `src/recommender.py` | Added all scoring functions + MOOD_SIMILARITY matrix |

### 📊 Interactive Resources (NEW)

| File | Purpose |
|------|---------|
| `Music_Recommender_Scoring.ipynb` | Interactive notebook with examples and visualizations |

---

## How to Use

### Basic Usage

```python
from src.recommender import Song, UserProfile, score_song

song = Song(...)  # Load from CSV or create manually
user = UserProfile(...)  # Create from user input

score = score_song(song, user)
print(f"Recommendation: {score*100:.1f}%")
```

### Advanced Usage

```python
# Use linear energy method
score = score_song(song, user, energy_method="linear")

# Adjust weights (70% energy, 30% mood)
score = score_song(song, user, energy_weight=0.7, mood_weight=0.3)

# Get top 5 recommendations
recommendations = [
    (s, score_song(s, user)) for s in song_library
]
recommendations.sort(key=lambda x: x[1], reverse=True)
top_5 = recommendations[:5]
```

---

## Verification & Testing

### ✅ All Formulas Work Correctly

**Energy Scoring:**
- ✓ Linear method: Returns values in [0, 1]
- ✓ Quadratic method: Returns values in [0, 1]
- ✓ Perfect match (distance=0): Score = 1.0
- ✓ Maximum distance: Score = 0.0

**Mood Scoring:**
- ✓ Exact matches: Score = 1.0
- ✓ Related moods: Score in {0.5, 0.6, 0.8}
- ✓ Unrelated moods: Score = 0.0
- ✓ Undefined pairs: Default to 0.0

**Combined Score:**
- ✓ Always in [0, 1]
- ✓ Weight validation works
- ✓ Both energy methods supported
- ✓ Customizable parameters

---

## Score Interpretation

| Range | Meaning | Emoji |
|-------|---------|-------|
| 0.85-1.0 | Excellent match | ⭐⭐⭐⭐⭐ |
| 0.70-0.85 | Good match | ⭐⭐⭐⭐ |
| 0.50-0.70 | Fair match | ⭐⭐⭐ |
| 0.30-0.50 | Poor match | ⭐⭐ |
| 0.00-0.30 | Very poor | ⭐ |

---

## Files to Review

### Start Here 👇
1. **`QUICK_REFERENCE.md`** ← 5-minute overview
2. **`src/recommender.py`** ← See the actual code
3. **`Music_Recommender_Scoring.ipynb`** ← Run examples

### For Deep Dive 🔍
4. **`SCORING_GUIDE.md`** ← All mathematical details
5. **`IMPLEMENTATION_DETAILS.md`** ← Technical documentation

---

## Next Steps

1. ✅ Review the formulas and implementation
2. ✅ Run the Jupyter notebook to see examples
3. ✅ Test with your `data/songs.csv` file
4. ✅ Integrate `score_song()` into your `recommend()` method
5. ✅ Adjust weights and energy method based on your use case

---

## Summary

✅ **Complete solution provided** with:
- Mathematical formulas for energy scoring (2 options)
- Mood similarity matrix with relationships
- Combined weighted scoring formula
- Full Python implementation
- Comprehensive documentation
- Interactive examples

**Your `score_song(song: Song, user: UserProfile) -> float` function is ready to use!**

---

**Status:** ✅ COMPLETE AND PRODUCTION-READY
**Date:** March 21, 2026
**Version:** 1.0
