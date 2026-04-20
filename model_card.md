# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch Mini** — a rule-based recommendation system that ranks songs based on user preferences for genre, mood, and energy.

---

## 2. Goal / Task

The system suggests which songs in a small catalog best fit one user at a time. It scores each song transparently and returns the top results that match the user's genre, mood, and energy settings.

---

## 3. Data Used

The catalog lives in `data/songs.csv`. It has **17 songs** total. Each row has title, artist, genre, mood, energy, tempo (BPM), valence, danceability, and acousticness. 

**Genre Distribution:** lofi (3), pop (2), all others (1 each)
**Mood Options:** happy, chill, intense, relaxed, moody, focused (6 total)

The dataset is small and imbalanced, which amplifies algorithmic biases toward lofi and pop users.

---

## 4. Algorithm Summary

**Current Weights (After Rebalancing):**
- Genre match: **+1.5** points (exact match only)
- Mood match: **+1.5** points (exact match only)  
- Energy similarity: up to **+1.25** points (formula: 1.25 × (1.0 - |song_energy - target_energy|))
- Acoustic bonus: up to **+0.5** points (if user likes acoustic AND song_acousticness ≥ 0.5)

Total possible score: ~4.6 points. Every song is sorted by total score (highest first), and the program returns the top K results (default K=5) with detailed text reasons for each component.

**Why These Weights?** Originally, genre was +2.0 (44% of score), creating a 52% score gap between rock's best and second-best songs. Rebalancing to +1.5 reduced this unfair cliff to 36%, making cross-genre recommendations viable. Mood and energy were boosted to improve multi-criteria diversity.

---

## 5. Observed Behavior / Biases

**Genre Weight Problem (Original vs. Revised):**
The original weighting (genre: +2.0, mood: +1.0, energy: +1.0) created severe "filter bubble" effects. For rock fans with only 1 rock song: #1: 3.99 → #2: 1.97 (52% drop). After reweighting to (genre: +1.5, mood: +1.5, energy: +1.25), the gap improved to 36% (#1: 4.24 → #2: 2.71), making cross-genre alternatives viable and fairer.

**Catalog Imbalance Amplifies Bias:**
- Lofi: 3 songs (18%) → lofi users get abundant options
- Pop: 2 songs (12%) → pop users get good diversity
- All others: 1 song each (6%) → rock, ambient, jazz fans get limited choices

This dataset imbalance compounds the algorithmic bias toward overrepresented genres.

**Strict Label Matching Penalizes Edge Cases:**
"Indie pop" ≠ "pop" in exact matching. Only 6 moods exist. Users feeling "nostalgic" or "bittersweet" get no match.

**Energy Extremes Cannot Be Satisfied:**
Catalog range: 0.28–0.93. Users requesting energy 0.1 or 1.0 cannot be satisfied by any song.

---

## 6. Evaluation Process

**Three User Profiles Tested:**

1. **High-Energy Pop** (genre: pop, mood: happy, energy: 0.9): Mainstream taste. Top match "Sunrise City" (4.15/4.5) was perfect. After reweighting, cross-genre "Disco Fever" improved from 1.99 to 2.74 (+37% improvement).

2. **Chill Lofi** (genre: lofi, mood: chill, energy: 0.4, likes_acoustic: true): Best case scenario. "Library Rain" scored 4.62/4.5 with full multi-criteria alignment. Acoustic bonus (+0.43) was transparent and meaningful.

3. **Deep Intense Rock** (genre: rock, mood: intense, energy: 0.9): Niche genre stress test. Only 1 rock song exists. Before reweight: 3.99 → 1.97 (52% drop). After reweight: 4.24 → 2.71 (36% drop, +0.74 improvement).

**Key Surprise:** The weight shift had disproportionate impact. Reducing genre by just 0.5 points improved rock profile's #2 recommendation by +0.74 points (37% improvement), showing weighting design is critical to fairness.

---

## 7. Intended Use and Non-Intended Use

**Intended Use:** 
- Educational demonstration of content-based recommendation design
- Learning how explicit scoring rules, weights, and catalogs shape outcomes
- Understanding why fairness is hard in ML systems
- Exploring how transparency enables bias detection

**Non-Intended Use:** 
- Real-world music platform (dataset too small)
- Artist auditing (scoring lacks historical data)
- Replacing human curation (17 songs insufficient for personalization)
- Making business decisions about genre representation

---

## 8. Ideas for Improvement

1. **Expand catalog:** Add more songs, especially underrepresented genres (rock, ambient, jazz) to reduce bias
2. **Add diversity rule:** Ensure top K results span multiple genres unless user explicitly requests single genre
3. **Support similarity matching:** Instead of strict mood matching, calculate mood similarity with continuous distance
4. **Support energy ranges:** Allow users to request "around 0.7 energy" instead of exact values
5. **Add recent-artist filter:** Track shown artists and de-prioritize repeats

---

## 9. Personal Reflection

**Biggest Learning:** Clear rules beat mystery. Once I knew the weights, I could predict why a song ranked high. When the list felt "wrong," I could point directly to the rule causing it. 

**Key Surprise:** A tiny set of if-then rules still *feels* like a recommender in the terminal—scores and reasons read like "because you listened to…"

**Fairness Insight:** Weighting is hypersensitive. Reducing genre by 0.5 points produced 37% improvement for niche genres, showing design choices have massive downstream fairness impact. The dataset imbalance (3 lofi, 2 pop, 1 of everything else) compounds the problem.

**What I'd Do Next:** 
- Implement a diversity rule so top 5 don't all cluster in one genre
- Add listening history tracking to avoid showing same artists repeatedly
- Expand the dataset to at least 50+ songs with balanced genre distribution
- Add a "similar mood" continuous metric instead of just exact matching
