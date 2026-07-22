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

Honestly, apps like Spotify and YouTube feel like they read your mind, but they're really just tracking everything you do (what you play, what you skip, what you throw on a playlist) and comparing you to millions of other people to guess what you'll want next. They also look at the actual sound of a song (is it fast, chill, acoustic, hype?) so they can find stuff that *feels* like what you already love. My version keeps it simple: instead of tracking a bunch of behavior, you describe your taste as a set of target values (favorite genre, favorite mood, ideal energy, etc.), and it finds the songs that land closest to that taste. No "people like you also listened to..." magic, just matching a song's vibe to your preferences using its numbers.

### What each `Song` uses

Every song is described by these features from `data/songs.csv`:

- `id`: unique identifier (used to look songs up, not to score)
- `title`, `artist`: display info only
- `genre`: e.g. lofi, pop, rock (categorical)
- `mood`: e.g. chill, intense, happy (categorical)
- `energy`: 0 to 1, how hyped/calm it is
- `valence`: 0 to 1, how happy/moody it sounds
- `danceability`: 0 to 1, how easy it is to move to
- `acousticness`: 0 to 1, acoustic vs electronic
- `tempo_bpm`: beats per minute (normalized to 0 to 1 before scoring)
- `instrumentalness`: 0 to 1, no vocals vs vocal-heavy
- `speechiness`: 0 to 1, spoken/rapped words vs sung

**Scored features:** genre, mood, energy, valence, danceability, acousticness, tempo, instrumentalness, speechiness. (`id`, `title`, `artist` are metadata, not scored.)

### What the `UserProfile` stores

A "taste profile" of target values, one per scored feature:

- `favorite_genre`: preferred genre (categorical)
- `favorite_mood`: preferred mood (categorical)
- `target_energy`, `target_valence`, `target_danceability`, `target_acousticness`: ideal 0 to 1 values
- `target_tempo_bpm`: ideal tempo in BPM (normalized to 0 to 1 at scoring time)
- `target_instrumentalness`, `target_speechiness`: ideal 0 to 1 values

The recommender treats these targets as the "perfect song" and scores how close each real song lands.

### The Algorithm Recipe

Each song earns points against the profile, then the list is ranked.

**Step 0 (prep):** normalize tempo to 0 to 1 with `(bpm - 60) / (160 - 60)`, applied to both the song and the profile target.

**Step 1 (score one song):**

```
score(song) =
    2.0  if genre == favorite_genre  else 0
  + 1.0  if mood  == favorite_mood   else 0
  + 1.0 * (1 - |target_energy           - energy|)
  + 1.0 * (1 - |target_acousticness     - acousticness|)
  + 0.8 * (1 - |target_instrumentalness - instrumentalness|)
  + 0.6 * (1 - |target_valence          - valence|)
  + 0.6 * (1 - |target_danceability     - danceability|)
  + 0.5 * (1 - |target_tempo_norm       - tempo_norm|)
  + 0.4 * (1 - |target_speechiness      - speechiness|)
```

- **Categorical (genre, mood):** exact match earns full points, otherwise 0. Genre is weighted 2x mood because genre is a harder taste boundary and mood cuts across genres.
- **Numeric:** `points * (1 - |target - value|)`, rewarding closeness to the target, not high or low values.
- Max possible is about 7.9 points; divide by 7.9 for a clean 0 to 1 display score (ordering is unchanged).

**Step 2 (choose the list):** score every song, sort descending, return the top K (default 5), breaking ties on genre match.

### Potential biases

- **Genre over-prioritization:** at 2.0 points, a genre match can outweigh several strong audio matches, so a "lofi" profile may bury a jazz track that nails the user's mood, energy, and acousticness just because the label differs. Great near-miss songs get ignored.
- **Exact-match blindness:** genre and mood are all-or-nothing. Sonically adjacent genres (ambient, jazz) score the same zero as the opposite end (metal), so the system can't reward "close but not identical" taste.
- **Correlated-feature double counting:** energy, acousticness, instrumentalness, and tempo tend to move together, so the "calm vs hype" axis is effectively counted several times, quietly outweighing independent signals like valence.
- **Popularity and catalog bias:** with only 18 songs and no play-count data, recommendations reflect whatever the small catalog happens to contain, not real-world listening.

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

## Sample Recommendation Output

`python -m src.main` runs five taste profiles: three "normal" profiles and
two **adversarial** profiles with internally conflicting preferences, used to
stress-test the scoring logic. Output captured below.

### Normal profiles

**High-Energy Pop** — top result nails genre + mood + audio, exactly as intended.

```
=== Profile: High-Energy Pop (pop / intense) ===
#1  Gym Hero - Max Pulse
    Score: 7.84
    Reasons:
      - genre match: pop (+2.0)
      - mood match: intense (+1.0)
      - energy close (+0.98)
      - acousticness close (+1.00)
      - instrumentalness close (+0.80)
      - valence close (+0.58)
      - danceability close (+0.59)
      - tempo close (+0.49)
      - speechiness close (+0.40)
#2  Sunrise City - Neon Echo
    Score: 6.47
    Reasons:
      - genre match: pop (+2.0)
      - energy close (+0.87)
      - acousticness close (+0.87)
      - instrumentalness close (+0.78)
      - valence close (+0.58)
      - danceability close (+0.53)
      - tempo close (+0.44)
      - speechiness close (+0.39)
#3  Storm Runner - Voltline
    Score: 5.30
    Reasons:
      - mood match: intense (+1.0)
      - energy close (+0.96)
      - acousticness close (+0.95)
      - instrumentalness close (+0.74)
      - speechiness close (+0.40)
#4  Block Party - Cardinal Flow
    Score: 4.46
    Reasons:
      - energy close (+0.90)
      - acousticness close (+0.97)
      - instrumentalness close (+0.79)
      - valence close (+0.55)
      - danceability close (+0.60)
#5  Neon Pulse - Voltgrid
    Score: 4.43
    Reasons:
      - energy close (+1.00)
      - acousticness close (+0.98)
      - valence close (+0.60)
      - danceability close (+0.59)
      - tempo close (+0.49)
      - speechiness close (+0.39)
```

**Chill Lofi** — the two genre+mood matches lead cleanly; adjacent ambient/jazz tracks fall below.

```
=== Profile: Chill Lofi (lofi / chill) ===
#1  Library Rain - Paper Lanterns
    Score: 7.79
    Reasons:
      - genre match: lofi (+2.0)
      - mood match: chill (+1.0)
      - energy close (+1.00)
      - acousticness close (+0.99)
      - instrumentalness close (+0.76)
      - valence close (+0.59)
      - danceability close (+0.58)
      - tempo close (+0.47)
      - speechiness close (+0.40)
#2  Midnight Coding - LoRoom
    Score: 7.63
    Reasons:
      - genre match: lofi (+2.0)
      - mood match: chill (+1.0)
      - energy close (+0.93)
      - acousticness close (+0.86)
      - instrumentalness close (+0.80)
      - valence close (+0.59)
      - danceability close (+0.56)
      - tempo close (+0.50)
      - speechiness close (+0.40)
#3  Focus Flow - LoRoom
    Score: 6.71
    Reasons:
      - genre match: lofi (+2.0)
      - energy close (+0.95)
      - acousticness close (+0.93)
      - instrumentalness close (+0.78)
      - valence close (+0.59)
      - danceability close (+0.57)
      - tempo close (+0.49)
      - speechiness close (+0.40)
#4  Spacewalk Thoughts - Orbit Bloom
    Score: 5.46
    Reasons:
      - mood match: chill (+1.0)
      - energy close (+0.93)
      - acousticness close (+0.93)
      - instrumentalness close (+0.72)
      - valence close (+0.56)
      - danceability close (+0.52)
      - tempo close (+0.41)
      - speechiness close (+0.40)
#5  Coffee Shop Stories - Slow Stereo
    Score: 4.57
    Reasons:
      - energy close (+0.98)
      - acousticness close (+0.96)
      - instrumentalness close (+0.68)
      - valence close (+0.52)
      - danceability close (+0.59)
      - tempo close (+0.44)
      - speechiness close (+0.40)
```

**Deep Intense Rock** — one clear rock+intense winner, then the genre pool thins fast in an 18-song catalog.

```
=== Profile: Deep Intense Rock (rock / intense) ===
#1  Storm Runner - Voltline
    Score: 7.79
    Reasons:
      - genre match: rock (+2.0)
      - mood match: intense (+1.0)
      - energy close (+0.99)
      - acousticness close (+1.00)
      - instrumentalness close (+0.76)
      - valence close (+0.58)
      - danceability close (+0.56)
      - tempo close (+0.49)
      - speechiness close (+0.40)
#2  Gym Hero - Max Pulse
    Score: 5.29
    Reasons:
      - mood match: intense (+1.0)
      - energy close (+0.99)
      - acousticness close (+0.95)
      - instrumentalness close (+0.70)
      - tempo close (+0.41)
      - speechiness close (+0.40)
#3  Iron Verdict - Ashfall
    Score: 4.44
    Reasons:
      - energy close (+0.94)
      - acousticness close (+0.94)
      - instrumentalness close (+0.76)
      - danceability close (+0.51)
      - tempo close (+0.45)
      - speechiness close (+0.39)
#4  Sunrise City - Neon Echo
    Score: 4.13
    Reasons:
      - energy close (+0.90)
      - acousticness close (+0.92)
      - instrumentalness close (+0.72)
      - danceability close (+0.49)
      - speechiness close (+0.40)
#5  Block Party - Cardinal Flow
    Score: 4.01
    Reasons:
      - energy close (+0.93)
      - acousticness close (+0.98)
      - instrumentalness close (+0.70)
```

### Adversarial / edge-case profiles

**Sad but Hype** (`metal / melancholic`, but `energy 0.95`, `valence 0.10`, `tempo 160`) — the mood is a contradiction on purpose: nothing in the catalog is both melancholic *and* maximally energetic. **Result:** the mood point is never awarded to the winner, and the genre point (+2.0) alone pins `Iron Verdict` to #1 despite it not matching the requested *melancholic* mood at all. The system silently satisfies the loud numeric preference and drops the emotional one — a clear illustration of the additive score's "any strong signal wins" failure mode.

```
=== Profile: Adversarial: Sad but Hype (metal / melancholic) ===
#1  Iron Verdict - Ashfall
    Score: 6.42
    Reasons:
      - genre match: metal (+2.0)
      - energy close (+0.97)
      - acousticness close (+0.99)
      - instrumentalness close (+0.68)
      - valence close (+0.54)
      - tempo close (+0.50)
      - speechiness close (+0.38)
#2  Storm Runner - Voltline
    Score: 4.38
    Reasons:
      - energy close (+0.96)
      - acousticness close (+0.95)
      - instrumentalness close (+0.76)
      - danceability close (+0.49)
      - tempo close (+0.46)
      - speechiness close (+0.40)
#3  Gym Hero - Max Pulse
    Score: 4.30
    Reasons:
      - energy close (+0.98)
      - acousticness close (+1.00)
      - instrumentalness close (+0.78)
      - danceability close (+0.58)
      - speechiness close (+0.39)
#4  Sunrise City - Neon Echo
    Score: 3.95
    Reasons:
      - energy close (+0.87)
      - acousticness close (+0.87)
      - instrumentalness close (+0.80)
      - danceability close (+0.56)
      - speechiness close (+0.40)
#5  Block Party - Cardinal Flow
    Score: 3.93
    Reasons:
      - energy close (+0.90)
      - acousticness close (+0.97)
      - instrumentalness close (+0.78)
      - danceability close (+0.57)
```

**No-Match Neutral** (genre `polka` / mood `nonexistent`, every numeric target `= 0.5`) — no song can earn categorical points, and asking for the *middle* of every axis means the numeric term barely separates anything. **Result:** the top five sit within 0.20 points of each other (3.99 → 3.79), the ranking is effectively arbitrary, and #4/#5 tie exactly at 3.79 — exposing how weak and tie-prone the score is once the genre/mood anchors are removed.

```
=== Profile: Adversarial: No-Match Neutral (polka / nonexistent) ===
#1  Backroad Sunset - Dusty Boots
    Score: 3.99
    Reasons:
      - energy close (+1.00)
      - acousticness close (+0.82)
      - valence close (+0.53)
      - danceability close (+0.57)
      - tempo close (+0.41)
#2  Midnight Coding - LoRoom
    Score: 3.88
    Reasons:
      - energy close (+0.92)
      - valence close (+0.56)
      - danceability close (+0.53)
#3  Night Drive Loop - Neon Echo
    Score: 3.80
    Reasons:
      - valence close (+0.59)
      - tempo close (+0.50)
#4  Coffee Shop Stories - Slow Stereo
    Score: 3.79
    Reasons:
      - energy close (+0.87)
      - instrumentalness close (+0.64)
      - danceability close (+0.58)
      - tempo close (+0.40)
#5  Paper Boats - Willow Grove
    Score: 3.79
    Reasons:
      - energy close (+0.83)
      - instrumentalness close (+0.68)
      - valence close (+0.57)
      - danceability close (+0.54)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

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

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



