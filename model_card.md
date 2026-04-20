# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch Mini** — a tiny rule-based helper that ranks songs for a made-up listener.

---

## 2. Goal / Task

The system suggests which songs in a small catalog best fit one user at a time. It does not predict streams or revenue. It scores each song and returns the top few titles that match the user’s genre, mood, and energy settings.

---

## 3. Data Used

The catalog lives in `data/songs.csv`. It has **10** songs right now. Each row has title, artist, genre, mood, energy, tempo (BPM), valence, danceability, and acousticness. Genres include pop, lofi, rock, ambient, jazz, synthwave, and indie pop. Moods include happy, chill, intense, relaxed, moody, and focused. The list is fake and small, so it cannot stand for all music or all listeners.

---

## 4. Algorithm Summary

Each song gets points from simple rules. If the song’s genre matches the user’s favorite genre, it gets **+2** points. If the mood matches, it gets **+1** point. Energy adds up to **+1** more: the closer the song’s energy is to the user’s target energy, the bigger that slice of the score (far away gives little or nothing). Then every song is sorted by total score, highest first, and the program returns the top **K** results. It also keeps short text reasons for each score, like “genre match” or “energy close.”

---

## 5. Observed Behavior / Biases

Genre counts a lot because it is worth the most points. That can bury good “vibe matches” in other genres. Energy can lift songs high even when genre or mood does not match, so the top list can look same-y in a tiny catalog. Some labels are strict (for example, “indie pop” is not treated as plain “pop”), which can feel unfair even if the math is consistent. The data skews toward a few moods and genres, so users who love underrepresented styles get weaker or odd picks.

---

## 6. Evaluation Process

I tried a few pretend users: **High-Energy Pop** (pop, happy, high energy), **Chill Lofi** (lofi, chill, lower energy), and **Deep Intense Rock** (rock, intense, high energy). I ran the CLI, read the top five, and checked if the order matched my gut. Pop and lofi profiles usually looked sensible. Rock only had one clear rock song, so the rest of the list was mostly “whatever scored next,” which was a good warning about small data. I also imagined changing the rules (for example, caring less about genre) and noticed how much that would change the leaderboard without any fancy math.

---

## 7. Intended Use and Non-Intended Use

**Intended use:** Learning and demos. Running the program locally to see how hand-written rules turn preferences into a ranked list and explanations.

**Non-intended use:** Do not use this as a real music product, a fairness audit for artists, or advice for mental health or identity. Do not use it to judge people or to make business or legal choices. It is not trained on real listener behavior and should not be sold or deployed as if it were.

---

## 8. Ideas for Improvement

1. Add more songs and more genres so niche tastes are not empty.  
2. Add a diversity rule so the top **K** are not all the same genre unless the user asked for that.  
3. Fold in extra fields (tempo bands, valence, or acoustic taste) with small weights and clearer explanations.

---

## 9. Personal Reflection

My biggest learning moment was seeing that **clear rules beat mystery**: once I knew the weights, I could predict why a song was on top, and when the list felt “wrong,” I could point to the rule that caused it. AI tools helped me scaffold the CSV loader and boilerplate fast, but I still had to **run the program and read the output** to catch things like import paths and edge cases the tools did not know about. What surprised me is how **a few if-then style pieces still feel like a “recommender”** in the terminal—scores and reasons read like a tiny version of Spotify’s “because you listened to…” line. If I extended the project, I would try **listening history** (skip recently shown artists) and a **second metric for variety** so the top list feels less repetitive.
