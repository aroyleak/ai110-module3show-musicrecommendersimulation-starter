# Reflection: Profile Comparison & Learning

## Profile Pair Comparisons

### High-Energy Pop vs. Chill Lofi

**Key Difference:** Mood and energy drive opposite scoring patterns.

**High-Energy Pop** prioritizes **genre + mood exact match** (happy, pop). "Sunrise City" dominates at 4.15/4.5 because it hits all three criteria simultaneously. The acoustic bonus doesn't apply, so the score plateaus.

**Chill Lofi** exemplifies the **multi-criteria sweet spot**. "Library Rain" achieves 4.62/4.5—higher than High-Energy Pop's best—because:
- Genre match: +1.5 (lofi = lofi)
- Mood match: +1.5 (chill = chill)
- Energy similarity: +1.25 (0.4 target vs. 0.3 actual energy = near perfect)
- Acoustic bonus: +0.43 (extra points for acoustic quality)

**Insight:** When all criteria align *and* acoustic bonus applies, the system produces the highest confidence. Chill preferences have an advantage because lofi songs tend to be acoustic.

---

### High-Energy Pop vs. Deep Intense Rock

**Key Difference:** Genre scarcity reveals algorithmic fairness problems.

**High-Energy Pop** has **2 pop songs** in the catalog:
- #1: Sunrise City (4.15/4.5) - perfect match
- #2: Disco Fever (2.74/4.5 after reweight) - same genre, different mood
- Cross-genre options fill positions #3-5 with scores around 2.0-2.5

**Deep Intense Rock** has **only 1 rock song**:
- #1: Gym Hero (4.24/4.5) - only possible rock match
- #2: originally 1.97/4.5 (52% drop) → now 2.71/4.5 (36% drop after reweight)
- Forced to rely on energy or mood matches from unrelated genres

**Before Reweighting:** Rock fans faced a 52% cliff between best and second-best. This made rock fans' experience feel **unfair and incomplete**.

**After Reweighting:** The cliff dropped to 36%, making alternatives like "Electric Surge" (2.71 points) viable without abandoning primary preference.

---

### Chill Lofi vs. Deep Intense Rock

**Key Difference:** Catalog representation vs. preference match quality.

**Chill Lofi** has **3 songs** in its genre:
- All 3 lofi songs score high (4.0+ range) because they match genre, mood, and energy simultaneously
- Acoustic bonus applies to most, adding +0.43
- Top recommendations are consistently excellent

**Deep Intense Rock** has **only 1 song**:
- Cannot get second-best rock song; forced into cross-genre fallbacks
- "Intense" mood matches other genres, but cross-genre energy similarity is unpredictable
- Acoustic bonus doesn't apply to rock songs in catalog

**Insight:** **Dataset imbalance creates systematic unfairness**. Lofi users benefit from abundant, well-matched options. Rock fans are constrained by scarcity. This is a data problem, not just an algorithm problem.

---

## Key Learning: Weight Sensitivity Discovery

When I reweighted genre from **+2.0 → +1.5**, I expected a small improvement. Instead, rock profile's #2 recommendation improved by **+0.74 points (37%)**.

This revealed: **Fairness is hypersensitive to design choices.**

- Original: Genre = 44% of total score → dominated rankings
- Revised: Genre = 35% of total score → balanced with mood and energy
- Result: Rock fans suddenly had viable alternatives without sacrificing primary-genre matches

**Takeaway:** Small weighting adjustments have disproportionate downstream effects on fairness. This makes recommender design a **moral decision**, not just a technical one.

---

## What Surprised Me

1. **Acoustic bonus was invisible until I ran it.** I added +0.5 points for acoustic songs, expecting it to be minor. Turns out, for Chill Lofi, the acoustic bonus (+0.43) is the difference between "very confident" (4.62) and "less confident" (4.19). It's more impactful than I predicted.

2. **Clear rules beat black-box mystery.** I could see *why* each recommendation appeared. When "Disco Fever" jumped from #2 to #1 contender after reweighting, I could trace it: genre dropped by 0.5, so its edge disappeared, making other songs competitive. No mystery, just math.

3. **A small dataset makes fairness failures concrete.** With only 1 rock song, the unfairness is *obvious*. Rock fans get a sharp 52% cliff. In larger catalogs, this problem would hide—recommendations might seem reasonable, but the bias persists invisibly.

---

## Reflection: Clear Rules > Mystery

The biggest insight: **Explainability is fairness infrastructure.**

I built this system with transparent scoring (each song gets reasons). This transparency let me:
- Spot the genre-weight bias
- Measure the unfairness (52% cliff)
- Test a fix (reweight to 1.5)
- Verify the improvement (36% cliff)

If the algorithm were a black box, I'd never notice the problem. The system would just output rankings, and rock fans would think, "I guess the algorithm doesn't like rock." But it's not that—it's a *design choice* embedded in weights.

**This suggests a principle:** Recommendation systems should show their work. Not for performance, but for *accountability*.

---

## What Would Improve the System

### Priority 1: Expand & Balance the Catalog
- Current: 3 lofi, 2 pop, 1 of everything else
- Target: 50+ songs with at least 3-5 per genre
- Impact: Would eliminate scarcity bias and give all users comparable options

### Priority 2: Add a Diversity Rule
- Current: Top 5 can all be lofi (if they score highest)
- Proposed: Reserve 40% of top K for secondary genres
- Impact: Forces algorithms to serve variety without sacrificing quality

### Priority 3: Support Continuous Mood Similarity
- Current: Mood is strict (happy ≠ relaxed, even though they're close)
- Proposed: Calculate mood distance (0-1 scale) instead of binary matching
- Impact: "Nostalgic" users could match "relaxed" songs with bonus points

### Priority 4: Support Energy Ranges
- Current: Users request exact energy (0.7)
- Proposed: Allow "around 0.7 ± 0.2"
- Impact: More forgiving matching, fewer unsatisfied users

---

## Personal Reaction

This was satisfying in a way I didn't expect. I built something tiny, ran it, broke it (by finding the bias), and fixed it (by reweighting). The cycle felt like real debugging—not theoretical, but hands-on and measurable.

The hardest part wasn't coding; it was **committing to design decisions** (picking weights). Every choice has tradeoffs:
- High genre weight → favors fans of well-represented genres
- Low genre weight → dilutes identity (pop fans get jazz recommendations)
- Exact mood matching → penalizes edge cases
- Loose mood matching → dilutes relevance

There's no "right" answer—just tradeoffs. Knowing this makes me skeptical of any recommender system that claims objectivity. Under the hood, there are always weighted choices, and those choices are *about values*, not just math.
