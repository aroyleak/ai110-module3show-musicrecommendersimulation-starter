# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

### System Overview

This is a **content-based recommender system** (not collaborative filtering). Users provide their music preferences via a form, which are compared against songs in the dataset using a transparent scoring algorithm.

### Song Features

Each song in `data/songs.csv` contains:
- **Genre** - Musical category (pop, lofi, rock, ambient, synthwave, jazz, country, grime, disco, reggae, orchestral, breakbeat)
- **Mood** - Emotional tone (happy, chill, intense, relaxed, focused, moody)
- **Energy** - Intensity level (0.0–1.0 scale)
- **Tempo (BPM)** - Beats per minute (60–152 BPM range)
- **Valence** - Positivity/brightness (0.0–1.0 scale)
- **Danceability** - How suitable for dancing (0.0–1.0 scale)
- **Acousticness** - Proportion of acoustic instruments (0.0–1.0 scale)

### User Profile

The `UserProfile` captures three core preferences:
- `preferred_genre` - The genre the user wants to hear
- `preferred_mood` - The emotional vibe they're seeking
- `target_energy` - How energetic/intense they want the music (0.0–1.0)

### Scoring Algorithm (The Recipe)

For each song in the catalog, the system calculates a **final score** using this formula:

```
FINAL_SCORE = 
    (genre_match × 1.5) +
    (mood_match × 1.5) +
    (energy_similarity × 1.25) +
    (acousticness_bonus × 0.5)

Score Range: 0.0 to 5.25 points (realistic max: ~4.6)
```

**Weight Justification:**

After testing three distinct user profiles, I discovered the original weights (genre: 2.0, mood: 1.0, energy: 1.0) were too heavily biased toward genre. This created a problem:
- Rock fans with only 1 rock song in the catalog faced a 52% score drop to cross-genre alternatives
- Users of niche genres got locked into narrow recommendations
- Great mood/energy matches from other genres were ignored

**Reweighting** to (genre: 1.5, mood: 1.5, energy: 1.25) achieves better balance:
- Genre still matters (primary factor) but doesn't dominate
- Mood and energy are equally important to genre
- Cross-genre alternatives are now viable (36% score gap instead of 52%)
- Better user experience for niche genre preferences

**Point Breakdown:**

| Factor | Points | Logic |
|--------|--------|-------|
| **Genre Match** | +1.5 | Exact match on user's preferred genre (primary) |
| **Mood Match** | +1.5 | Exact match on user's preferred mood (equally important) |
| **Energy Similarity** | Up to +1.25 | Scaled by proximity: `1.25 × (1.0 - abs(song_energy - target_energy))` |
| **Acoustic Bonus** | Up to +0.5 | Optional: bonus if user likes acoustic music |

**Example Calculation:**

User wants: **pop** genre, **happy** mood, **0.90** energy

Song: "Sunrise City" (pop, happy, 0.82 energy)
- Genre match: +1.5 ✓
- Mood match: +1.5 ✓
- Energy similarity: 1.25 × (1.0 - |0.82 - 0.90|) = 1.25 × 0.92 = +1.15 ✓
- **Total: 4.15 points** (Highly recommended!)

### Recommendation Selection

1. Score all 17 songs using the formula above
2. Sort by score (highest first)
3. Return **top 5** recommendations
4. Filter by confidence threshold:
   - **High Confidence** (≥3.5 points): "Highly Recommended"
   - **Medium Confidence** (2.5–3.4 points): "Recommended"
   - **Low Confidence** (<2.5 points): "Alternatives"

### Sample Output

Running the recommender with the "High-Energy Pop" user profile:

```bash
$ python src/main.py

✓ Loaded 17 songs from data/songs.csv

================================================================================
🎵 MUSIC RECOMMENDER SIMULATION - High-Energy Pop
================================================================================

📋 Your Profile:
   • Favorite Genre: POP
   • Favorite Mood: HAPPY
   • Target Energy: 0.9

🏆 Top 5 Recommendations:

#1 Sunrise City
    Artist: Neon Echo
    Genre: POP
    Score: 4.15/4.5 ⭐
    Why: Genre match: pop (+1.5) | Mood match: happy (+1.5) | Energy similarity (target: 0.9, 
song: 0.82) (+1.15)

#2 Disco Fever
    Artist: Vinyl Legends
    Genre: DISCO
    Score: 2.74/4.5 ⭐
    Why: Mood match: happy (+1.5) | Energy similarity (target: 0.9, song: 0.89) (+1.24)

#3 Gym Hero
    Artist: Max Pulse
    Genre: POP
    Score: 2.71/4.5 ⭐
    Why: Genre match: pop (+1.5) | Energy similarity (target: 0.9, song: 0.93) (+1.21)

#4 Rooftop Lights
    Artist: Indigo Parade
    Genre: INDIE POP
    Score: 2.58/4.5 ⭐
    Why: Mood match: happy (+1.5) | Energy similarity (target: 0.9, song: 0.76) (+1.07)

#5 Summer Vibes
    Artist: Reggae Sunset
    Genre: REGGAE
    Score: 2.42/4.5 ⭐
    Why: Mood match: happy (+1.5) | Energy similarity (target: 0.9, song: 0.64) (+0.93)

================================================================================
```

**Key Observations:**
- **#1 Winner: "Sunrise City"** - Perfect match with all three criteria (genre, mood, energy)
- **#2 "Disco Fever"** - Different genre but excellent mood + energy match (score: 2.74)
- **#3 "Gym Hero"** - Same genre but with energy close to target
- **#2-5 Rankings** - With reweighted scores, cross-genre alternatives (disco, indie pop, reggae) now rank competitively based on mood+energy rather than being locked out by genre mismatch

This demonstrates that the **reweighted algorithm provides better diversity** while still prioritizing genre matches.

---

### Expected Biases & Limitations

⚠️ **Known Issues:**

1. **Genre Over-Prioritization** - Genre gets 1.5 points vs. mood's 1.5 point. This means the system **heavily favors exact genre matches**, potentially ignoring excellent cross-genre recommendations. A song with perfect mood/energy but wrong genre will score poorly.

2. **Limited Genre Diversity** - Only 12 unique genres in catalog, mostly Western music. Users seeking niche genres (metal, k-pop, classical) won't find matches.

3. **Energy Bias** - The algorithm assumes users always want their exact target energy. A user seeking "0.75 energy pop" might miss a great "0.65 energy pop" song with perfect mood/lyrics.

4. **Mood Ceiling** - Only 6 moods in dataset. Real emotion is more nuanced. A user feeling "bittersweet" or "nostalgic" has no exact match.

5. **No Lyrical Understanding** - Ignores lyrics, themes, and cultural context. A song titled "Midnight Rain" might match a mood better than its audio features suggest.

6. **Cold Start Problem** - New/small catalog (17 songs) means first-time users may see limited options, especially for niche preferences.

7. **No User History** - System doesn't learn from what users actually listened to vs. what was recommended. All users treated equally.

**Potential Fairness Issues:**
- Artists/genres with fewer songs in dataset are under-recommended
- Majority genres (pop, lofi) dominate recommendations
- Could reinforce "filter bubbles" if users always pick the same genre 

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Test Results - Three Distinct User Profiles

I tested the recommender with three distinct user preference profiles to evaluate system performance across different music tastes:

### Profile 1: High-Energy Pop 🎉

**User Preferences:** Pop genre, Happy mood, High energy (0.9)

**Terminal Output:**
```
📋 Your Profile:
   • Favorite Genre: POP
   • Favorite Mood: HAPPY
   • Target Energy: 0.9

🏆 Top 5 Recommendations:

#1 Sunrise City - Neon Echo (POP)
    Score: 3.92/4.5 ⭐
    Why: Genre match: pop (+1.5) | Mood match: happy (+1.5) | Energy similarity (target: 0.9, song: 0.82) (+0.92)

#2 Gym Hero - Max Pulse (POP)
    Score: 2.97/4.5 ⭐
    Why: Genre match: pop (+1.5) | Energy similarity (target: 0.9, song: 0.93) (+0.97)

#3 Disco Fever - Vinyl Legends (DISCO)
    Score: 1.99/4.5 ⭐
    Why: Mood match: happy (+1.5) | Energy similarity (target: 0.9, song: 0.89) (+0.99)

#4 Rooftop Lights - Indigo Parade (INDIE POP)
    Score: 1.86/4.5 ⭐
    Why: Mood match: happy (+1.5) | Energy similarity (target: 0.9, song: 0.76) (+0.86)

#5 Summer Vibes - Reggae Sunset (REGGAE)
    Score: 1.74/4.5 ⭐
    Why: Mood match: happy (+1.5) | Energy similarity (target: 0.9, song: 0.64) (+0.74)
```

**Observation:** Perfect match for #1 with all three criteria (genre, mood, energy). System performs well for mainstream preferences.

---

### Profile 2: Chill Lofi 🎧

**User Preferences:** Lofi genre, Chill mood, Low energy (0.4), Acoustic bonus enabled

**Terminal Output:**
```
📋 Your Profile:
   • Favorite Genre: LOFI
   • Favorite Mood: CHILL
   • Target Energy: 0.4
   • Likes Acoustic: YES

🏆 Top 5 Recommendations:

#1 Library Rain - Paper Lanterns (LOFI)
    Score: 4.38/4.5 ⭐
    Why: Genre match: lofi (+1.5) | Mood match: chill (+1.5) | Energy similarity (target: 0.4, song: 0.35) (+0.95) | Acoustic bonus (acousticness: 0.86) (+0.43)

#2 Midnight Coding - LoRoom (LOFI)
    Score: 4.33/4.5 ⭐
    Why: Genre match: lofi (+1.5) | Mood match: chill (+1.5) | Energy similarity (target: 0.4, song: 0.42) (+0.98) | Acoustic bonus (acousticness: 0.71) (+0.35)

#3 Focus Flow - LoRoom (LOFI)
    Score: 3.39/4.5 ⭐
    Why: Genre match: lofi (+1.5) | Energy similarity (target: 0.4, song: 0.4) (+1.00) | Acoustic bonus (acousticness: 0.78) (+0.39)

#4 Spacewalk Thoughts - Orbit Bloom (AMBIENT)
    Score: 2.34/4.5 ⭐
    Why: Mood match: chill (+1.5) | Energy similarity (target: 0.4, song: 0.28) (+0.88) | Acoustic bonus (acousticness: 0.92) (+0.46)

#5 Coffee Shop Stories - Slow Stereo (JAZZ)
    Score: 1.42/4.5 ⭐
    Why: Energy similarity (target: 0.4, song: 0.37) (+0.97) | Acoustic bonus (acousticness: 0.89) (+0.45)
```

**Observation:** Highest confidence scores (4.38 and 4.33)! Perfect multi-criteria alignment produces excellent results. Acoustic bonus adds significant value.

---

### Profile 3: Deep Intense Rock 🎸

**User Preferences:** Rock genre, Intense mood, High energy (0.9)

**Terminal Output:**
```
📋 Your Profile:
   • Favorite Genre: ROCK
   • Favorite Mood: INTENSE
   • Target Energy: 0.9

🏆 Top 5 Recommendations:

#1 Storm Runner - Voltline (ROCK)
    Score: 3.99/4.5 ⭐
    Why: Genre match: rock (+1.5) | Mood match: intense (+1.0) | Energy similarity (target: 0.9, song: 0.91) (+0.99)

#2 Gym Hero - Max Pulse (POP)
    Score: 1.97/4.5 ⭐
    Why: Mood match: intense (+1.0) | Energy similarity (target: 0.9, song: 0.93) (+0.97)

#3 Breakbeat Bounce - Rhythm Masters (BREAKBEAT)
    Score: 1.97/4.5 ⭐
    Why: Mood match: intense (+1.0) | Energy similarity (target: 0.9, song: 0.87) (+0.97)

#4 Grime City - Urban Warriors (GRIME)
    Score: 1.94/4.5 ⭐
    Why: Mood match: intense (+1.0) | Energy similarity (target: 0.9, song: 0.84) (+0.94)

#5 Disco Fever - Vinyl Legends (DISCO)
    Score: 0.99/4.5 ⭐
    Why: Energy similarity (target: 0.9, song: 0.89) (+0.99)
```

**Observation:** Large score gap (3.99 vs 1.97) reveals limited genre diversity. Only one rock song in catalog, forcing fallback to mood + energy matching for remaining recommendations.

---

## Summary of Test Results

| Profile | Top Score | Key Finding |
|---------|-----------|-------------|
| High-Energy Pop | 3.92/4.5 | Good performance with popular genre |
| Chill Lofi | 4.38/4.5 | Best performance - multi-criteria alignment |
| Deep Intense Rock | 3.99/4.5 | Limited by catalog (only 1 rock song) |

The system excels when user preferences align with available songs in the catalog. Performance degrades for niche genres due to limited catalog diversity (17 songs total).

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

### 🎓 Personal Reflection on the Engineering Process

**Biggest Learning Moment:** My most eye-opening moment was realizing that **weighting design is a fairness decision, not just a technical one**. When I discovered the 52% score cliff for rock fans (genre weight +2.0), I initially thought "oh, I should rebalance this to be more mathematical." But then I realized: every weight I choose embeds a *value*. By making genre worth 44% of the score, I was saying "genre is 4x more important than mood," which happened to hurt underrepresented genres. Reducing genre to 1.5 points (+1.5 instead of +2.0) didn't just improve the algorithm—it changed whose experience was prioritized. This shifted how I think about all recommendation systems: there's no "objective" ranking, just ranked choices.

**How AI Tools Helped (and When I Needed to Double-Check):** AI tools were fantastic for scaffolding—generating the CSV loader boilerplate, suggesting the scoring formula structure, and helping me think through edge cases. But I **absolutely had to run the code myself** to catch critical issues: 
- Import path bugs that the tool glossed over
- The actual 52% fairness cliff that only showed up when I tested real profiles
- The acoustic bonus was (+0.43) more impactful than expected—I needed to see the actual scores to realize

The rule I learned: **AI accelerates ideas; running code validates them.** I trusted the algorithm structure the tool suggested, but I didn't trust the results until I saw the terminal output with real numbers.

**What Surprised Me About Simple Algorithms:** The smallest thing shocked me the most: these simple if-then rules *feel like recommendations* in the terminal. When I see:
```
#1 Sunrise City (4.15/4.5) — Genre match: pop (+1.5) | Mood match: happy (+1.5) | Energy similarity (+1.15)
```
...it reads like "because you like pop and happy vibes, here's an energetic match." It *feels* intelligent, even though it's just point-adding. This made me realize: **perceived fairness matters more than algorithmic complexity**. Users don't care if the recommender is a neural network or hand-written rules—they care if the *explanation* makes sense to them.

**What I'd Try Next:** If I extended this, I'd implement **a diversity rule** first. Right now, if lofi songs score highest, the entire top 5 could be lofi, which feels repetitive even if mathematically correct. Adding logic like "ensure 1 song from a different genre in top 5 unless user explicitly asks for single-genre" would be simple but high-impact. After that, I'd expand the dataset to at least 50 songs with balanced genre distribution—the 3 lofi vs. 1 rock imbalance is a constant reminder that **data shapes fairness as much as algorithms do**. Finally, I'd add a "listening history" filter to avoid recommending the same artists repeatedly, because real recommendation systems have context (what did you just listen to?) that my single-profile approach lacks.

---

### What I Learned About Real AI Systems

This tiny project taught me that recommender systems aren't mysterious black boxes—they're **design choices made visible**. In industry systems like Spotify or Netflix:
- The weights and thresholds are hidden, but they still exist
- The training data is biased, but it shapes what gets recommended
- The evaluation is opaque, but every choice was tested by engineers like me

Building this made me skeptical of "objective" recommendations. When Spotify says "we picked this for you," what they really mean is "we weighted these features in this way, on this data, toward this goal." Knowing *that* changes everything about how I'll evaluate AI systems going forward.


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"
```

