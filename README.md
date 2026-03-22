# Music Recommender Simulation

## Project Summary

This repo is a **CLI-first** music recommender practice project. Songs load from `data/songs.csv`. A small Python program scores each track from a user preference dict (genre, mood, target energy), ranks them, and prints the top **K** with short reasons. The goal is to see how plain rules and transparent scores mimic “recommendations” without a real streaming backend.

---

## How The System Works

Songs are rows in a CSV. The program turns each row into a dictionary with typed fields (energy, tempo, valence, and so on). For each song, **`score_song`** adds points for genre match (+2), mood match (+1), and how close energy is to the user’s target (up to +1). **`recommend_songs`** sorts by total score and returns the top **K** with explanation strings. **`src/main.py`** runs a sample profile and prints titles, final scores, and reasons in the terminal.

**Optional / not in the score yet:** tempo, valence, danceability, and acousticness are loaded but not used in the current formula. The `Recommender` class in `recommender.py` is still starter code for tests.

**Biases to keep in mind:** genre is weighted heavily; small catalogs and exact string genres can make results repetitive or oddly strict.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Mac or Linux
   .venv\Scripts\activate   # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app (from the project root):

   ```bash
   python3 -m src.main
   ```

### Running Tests

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Document things you changed or imagined here, for example:

- Lowering the genre weight versus mood or energy
- Adding tempo or valence into the score
- Trying different fake user profiles and reading the top five out loud

---

## Limitations and Risks

- Tiny, synthetic catalog—not real listener data  
- No lyrics, language, or audio understanding  
- Can over-weight one feature or repeat similar vibes in the top **K**  

See **model_card.md** for a fuller write-up.

---

## Reflection

Full write-up (model name, data, algorithm, evaluation, intended use, improvements, and **personal reflection**): [**model_card.md**](model_card.md).

Building this showed me that recommenders are often **just ranked lists** built from rules or models you can question. Simple scoring still produces output that *feels* personalized because the program names reasons. Bias shows up when one feature dominates or when the catalog skips whole styles—so checking results by hand matters as much as writing the code. Human judgment still picks the weights, the labels, and what “good” means for a playlist.
