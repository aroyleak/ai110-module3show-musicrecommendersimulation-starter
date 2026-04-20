# Music Recommender - Scoring Logic Design

## Algorithm Recipe Overview
This document defines the specific rules and point-weighting strategy used to recommend songs based on user preferences.

---

## Point-Weighting Strategy

### 1. **Genre Match** - 2.0 points
- **Rationale**: Genre is a primary categorization that reflects fundamental musical style. Songs in the same genre share instrumental characteristics, production style, and audience expectations.
- **Implementation**: If user's preferred genre matches song's genre exactly → +2.0 points
- **Data Insight**: Our catalog has diverse genres (pop, lofi, rock, ambient, synthwave, jazz, country, grime, disco, reggae, orchestral, breakbeat) with varying audio characteristics.

### 2. **Mood Match** - 1.0 point
- **Rationale**: Mood is a secondary but important factor that captures the emotional resonance. Multiple genres can share moods (e.g., "chill" appears in lofi, ambient, and jazz).
- **Implementation**: If user's mood preference matches song's mood exactly → +1.0 point
- **Data Insight**: Moods in catalog: happy, chill, intense, relaxed, focused, moody
- **Note**: A song can have both genre AND mood match simultaneously.

### 3. **Energy Level Similarity** - Up to 1.0 point (scaled by proximity)
- **Rationale**: Energy level (0.0-1.0 scale) is a continuous variable that directly impacts how the song "feels" during listening. Closer energy matches provide better recommendations.
- **Implementation**: 
  - Calculate absolute difference: |user_energy_target - song_energy|
  - Score = 1.0 - (energy_difference / 1.0)
  - If difference ≤ 0.15 → Full 1.0 point (high similarity)
  - If difference = 0.5 → 0.5 points (moderate similarity)
  - If difference > 0.8 → Near 0 points (poor similarity)
- **Data Insight**: Energy ranges from 0.28 (Spacewalk Thoughts - ambient) to 0.93 (Gym Hero - pop/intense)
- **Example**: If user wants energy=0.75, Neon Echo's "Night Drive Loop" (0.75 energy) scores 1.0, while Spacewalk Thoughts (0.28) scores ~0.0

### 4. **Bonus Factors** (Optional enhancements)
- **Tempo Alignment** - 0.5 points (if within 10% of user preference)
  - Data range: 60-152 BPM
  - Helps refine recommendations when primary factors are equal

- **Audio Feature Alignment** (Danceability, Acousticness, Valence)
  - Can be used as tiebreakers
  - 0.25 points per feature if user specifies preference
  - Example: User wants "upbeat and danceable" → prioritize high danceability (0.79-0.94 range)

---

## Recommendation Score Formula

```
FINAL_SCORE = 
    (genre_match × 2.0) +
    (mood_match × 1.0) +
    (energy_similarity × 1.0) +
    (tempo_bonus × 0.5) +
    (audio_features_bonus × 0.25)

Max possible score: 5.0 points (rarely achieved, realistic max ~4.0)
```

---

## Scoring Logic Examples from Dataset

### Example 1: User Profile
- Preferred Genre: **pop**
- Preferred Mood: **happy**
- Target Energy: **0.80**

**Top Recommendations:**
1. "Sunrise City" (ID: 1) - Neon Echo
   - Genre match: +2.0 ✓
   - Mood match (happy): +1.0 ✓
   - Energy (0.82): +0.98 ✓
   - **TOTAL: 4.98**

2. "Rooftop Lights" (ID: 10) - Indigo Parade
   - Genre match (indie pop): +2.0 ✓
   - Mood match (happy): +1.0 ✓
   - Energy (0.76): +0.96 ✓
   - **TOTAL: 4.96**

3. "Disco Fever" (ID: 14) - Vinyl Legends
   - Genre match (pop-adjacent): +2.0 ✓
   - Mood match (happy): +1.0 ✓
   - Energy (0.89): +0.90 ✓
   - **TOTAL: 4.90**

### Example 2: User Profile
- Preferred Genre: **lofi**
- Preferred Mood: **chill**
- Target Energy: **0.40**

**Top Recommendations:**
1. "Midnight Coding" (ID: 2) - LoRoom
   - Genre match: +2.0 ✓
   - Mood match (chill): +1.0 ✓
   - Energy (0.42): +0.98 ✓
   - **TOTAL: 4.98**

2. "Library Rain" (ID: 4) - Paper Lanterns
   - Genre match: +2.0 ✓
   - Mood match (chill): +1.0 ✓
   - Energy (0.35): +0.95 ✓
   - **TOTAL: 4.95**

3. "Focus Flow" (ID: 9) - LoRoom
   - Genre match: +2.0 ✓
   - Mood match (focused): +0.0 ✗
   - Energy (0.40): +1.0 ✓
   - **TOTAL: 3.0**

---

## Threshold for Recommendations

- **High Confidence** (≥ 3.5 points): Highly recommended
- **Medium Confidence** (2.5-3.4 points): Recommended if no high-confidence options
- **Low Confidence** (< 2.5 points): Show as alternatives only

---

## Implementation Considerations

1. **Normalization**: All scores scale 0-5 range for consistency
2. **Tie-Breaking**: When scores are within 0.1 points, use energy similarity as primary tiebreaker
3. **Cold Start**: For new users, recommend songs with highest absolute scores (cross-genre hits)
4. **Diversity**: In top 5 recommendations, limit to 2 songs per genre if possible

---

## Testing Dataset Insights

- **Most Popular Genres**: pop (3 songs), lofi (3 songs)
- **Most Common Mood**: chill (3 songs)
- **Energy Distribution**: Concentrated around 0.40-0.90 range
- **Recommendation Diversity**: Using this algorithm ensures mix of genres while maintaining relevance

---

## Data Flow Visualization

### High-Level Process: Input → Process → Output

```mermaid
flowchart TD
    A["📥 INPUT: User Preferences"] --> B["🎯 User Profile Created"]
    B --> C["preferred_genre: string<br/>preferred_mood: string<br/>target_energy: float"]
    
    C --> D["📂 Load songs.csv"]
    D --> E["🔄 PROCESSING LOOP<br/>For each song in catalog"]
    
    E --> F["🎵 Song Data Extracted"]
    F --> G["genre, mood, energy, tempo, etc."]
    
    G --> H["📊 Calculate Score"]
    H --> I["Genre Match: +2.0?<br/>Mood Match: +1.0?<br/>Energy Similarity: +X?"]
    
    I --> J["✅ Store Score with Song ID"]
    J --> K{"More songs<br/>to process?"}
    
    K -->|Yes| E
    K -->|No| L["📈 Sort All Songs by Score"]
    
    L --> M["🏆 OUTPUT: Ranked List"]
    M --> N["Top K Recommendations<br/>Sorted High → Low Score"]
    
    style A fill:#e1f5ff
    style M fill:#c8e6c9
    style H fill:#fff9c4
```

---

### Detailed Scoring Loop (Single Song Processing)

```mermaid
flowchart TD
    Start["🎵 Load Song from CSV<br/>ID, Title, Artist, Genre, Mood, Energy"] --> Step1{"Genre ==<br/>User Preference?"}
    
    Step1 -->|Yes| G_Add["genre_points = 2.0"]
    Step1 -->|No| G_Skip["genre_points = 0.0"]
    
    G_Add --> Step2
    G_Skip --> Step2
    
    Step2{"Mood ==<br/>User Preference?"}
    
    Step2 -->|Yes| M_Add["mood_points = 1.0"]
    Step2 -->|No| M_Skip["mood_points = 0.0"]
    
    M_Add --> Step3
    M_Skip --> Step3
    
    Step3["Calculate Energy Similarity<br/>diff = |song_energy - target_energy|<br/>energy_points = 1.0 - diff"]
    
    Step3 --> Step4["Calculate Bonus Points<br/>tempo_bonus = 0.5 if within 10%<br/>audio_bonus = 0.25 if specified"]
    
    Step4 --> Final["📊 TOTAL SCORE<br/>score = genre_points +<br/>mood_points +<br/>energy_points +<br/>tempo_bonus +<br/>audio_bonus"]
    
    Final --> Store["💾 Store Result<br/>{song_id, title, score}"]
    
    style Start fill:#e3f2fd
    style Final fill:#fff3e0
    style Store fill:#f3e5f5
```

---

### Complete Pipeline: From CSV to Recommendations

```mermaid
flowchart LR
    CSV["📄 songs.csv<br/>17 songs"]
    
    CSV --> |Load| Memory["🗂️ In-Memory<br/>Song Objects"]
    
    User["👤 User Input<br/>Genre: pop<br/>Mood: happy<br/>Energy: 0.80"] --> |Create Profile| Profile["📋 User Profile"]
    
    Profile --> |Initialize| Scoring["🎯 Scoring Engine"]
    Memory --> |Feed| Scoring
    
    Scoring --> |Process| Scores["📊 Score Array<br/>[{id:1, score:4.98},<br/>{id:10, score:4.96},<br/>{id:14, score:4.90},<br/>...]"]
    
    Scores --> |Sort| Ranked["🏆 Ranked Results<br/>1. Sunrise City (4.98)<br/>2. Rooftop Lights (4.96)<br/>3. Disco Fever (4.90)"]
    
    Ranked --> |Filter| Top5["🎵 Top 5<br/>Recommendations"]
    
    Top5 --> Output["✨ Display to User"]
    
    style CSV fill:#e8f5e9
    style User fill:#e3f2fd
    style Ranked fill:#fff3e0
    style Output fill:#f3e5f5
```

---

## Data Flow Summary

| Stage | Input | Process | Output |
|-------|-------|---------|--------|
| **1. Intake** | User preferences (genre, mood, energy) | Store as Profile object | User profile loaded |
| **2. Load** | CSV file path | Read and parse CSV | 17 song objects in memory |
| **3. Loop** | Each song object | Calculate scoring formula | Score value (0-5 range) |
| **4. Store** | Score + Song ID | Add to results list | Results array |
| **5. Rank** | Results array | Sort by score descending | Sorted list (highest first) |
| **6. Output** | Top N from sorted list | Format & display | Top K recommendations |
```
