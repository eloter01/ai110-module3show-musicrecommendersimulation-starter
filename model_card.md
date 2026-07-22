# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

It matches songs to your taste. The name says what it does.

---

## 2. Intended Use  

**Goal.** You describe your taste. The app guesses which songs you would like.
It ranks a small list of songs from best fit to worst fit.

**What it assumes.** It assumes you can describe your taste as settings. A
favorite genre, a favorite mood, and a few sliders like energy and tempo. It
does not watch what you actually play.

**Made for.** Learning and class demos. It is a simple example of how a
recommender turns preferences into picks.

**Not made for.** Real users or real products. Do not use it to pick music for a
store, an event, or an app. It only knows 18 songs and cannot learn over time.

---

## 3. How the Model Works  

You set your taste as targets. A favorite genre, a favorite mood, and sliders
for things like energy, tempo, and how acoustic you want it.

Then every song gets a score.

- A song gets 2 points if its genre matches yours.
- It gets 1 point if its mood matches.
- It gets partial points for each slider, based on how close the song is to your target.
- Closer to your target means more points.

We add up all the points. The songs with the highest scores go to the top.

**What we changed from the starter.** The starter just handed back the first few
songs in the list. We wrote the real scoring. We added more sliders (like tempo
and valence). We also made it print the reasons for each pick.

---

## 4. Data  

The app uses one file, `data/songs.csv`. It has 18 songs.

Each song has a title, an artist, a genre, and a mood. It also has numbers from
0 to 1 for energy, valence, danceability, acousticness, instrumentalness, and
speechiness, plus a tempo in beats per minute.

The 18 songs cover 15 different genres. So almost every genre has just one song.
Moods are spread out too, with only a few repeats.

We did not add or remove any songs.

**What is missing.** The list is tiny. There is no real listening history. It
does not know lyrics or language. Most genres and moods barely show up, and there
are very few songs in the middle of the energy range.

---

## 5. Strengths  

It works best for people with a clear, strong taste. If you want loud pop or
calm lofi, it finds good matches fast.

It handles opposite tastes well. A calm listener and a hyped listener get very
different lists, which is what we want.

The genre and mood bonuses feel right. A pop fan gets pop songs first.

It also explains itself. Every pick comes with reasons, so you can see why it
was chosen.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

**Weakness found during experiments: a "calm vs. hype" filter bubble.** Four of
the song features (energy, acousticness, instrumentalness, and tempo) really all
describe the same thing, which is how calm or how hyped a song is. Because the
score adds up all four, that one idea gets counted about four times and ends up
steering the whole ranking, while things like happiness or danceability barely
move the needle. The songs themselves make this worse: out of 18 songs, 8 are
high energy and 7 are low, and only 3 sit somewhere in the middle. So if you
like calm music or hyped music, the app has plenty to give you, but if your
taste sits in the middle or jumps around, there is almost nothing that fits, and
the results start to feel random. We saw this in two tests. Doubling the weight
on energy shuffled the lower spots around just based on how loud a song was, and
the "No-Match Neutral" test scored its whole top five within a fifth of a point
of each other, so the order was basically a coin flip. In plain terms, the app
quietly sorts people into "calm person" or "hype person" and treats those two
groups well while leaving everyone in between with weak picks. (Worth noting: pop
is not over-represented in our data. The 18 songs cover 15 different genres, so
this problem comes from how we score, not from one genre taking over.)

---

## 7. Evaluation  

How we checked whether the recommender behaved as expected.

**Profiles we tested.** We ran five made-up listeners through the app:

1. **High-Energy Pop:** loud, upbeat pop.
2. **Chill Lofi:** quiet, mellow, acoustic study music.
3. **Deep Intense Rock:** heavy, high-energy rock.
4. **Sad but Hype (trick profile):** asks for sad, gloomy music but also cranks the energy and speed way up, which is a contradiction on purpose.
5. **No-Match Neutral (trick profile):** asks for a genre that isn't in our library and sets every slider to the exact middle.

**What might surprise someone.** The most surprising result is that one song,
"Gym Hero," keeps showing up at or near the top for very different listeners.
Here is why in plain terms: the app cares a lot about two things, whether the
genre matches and how loud/energetic the song is. "Gym Hero" is a pop song that
is very high energy and very electronic, so it scores big on both. If someone
just wants happy pop, "Gym Hero" still wins almost all the points for being pop
and being energetic, and the only thing it misses is the "happy" label (it is
tagged "intense" instead). Missing that one label costs it a single point, which
is not enough to push it down the list, so it keeps popping up even though it is
not really a "happy" song. The second surprise is that the two trick profiles
behaved very differently from each other: the contradictory "Sad but Hype"
listener still got confident picks, while the "everything in the middle"
listener got a nearly random-looking list where the top five were almost tied.

**Comparing the profiles two at a time.** Each row explains what changed between
two listeners and why that makes sense.

| Pair | What changed, and why it makes sense |
|---|---|
| High-Energy Pop vs. Chill Lofi | Complete opposites. Pop pulls loud, electronic songs like "Gym Hero"; Lofi pulls quiet, acoustic songs like "Library Rain." No songs overlap, which is exactly what we'd expect from opposite tastes. |
| High-Energy Pop vs. Deep Intense Rock | Almost the same list, just reordered. Both want loud, high-energy music, so they pull from the same pile of songs. The only real difference is which genre gets the 2-point bonus, so pop puts "Gym Hero" on top and rock puts "Storm Runner" on top. |
| High-Energy Pop vs. Sad but Hype | Surprisingly similar top songs. Even though one asks for happy pop and the other for sad metal, both crank up the energy, and energy dominates, so both end up with the same loud songs. This shows the "sad" request basically gets ignored. |
| High-Energy Pop vs. No-Match Neutral | Pop gets one clear winner with a high score; Neutral gets a flat list of medium songs with tiny score gaps. Asking for the middle of everything gives the app nothing strong to grab onto, so the results turn mushy. |
| Chill Lofi vs. Deep Intense Rock | Total opposites again (calm and acoustic vs. loud and electric), so the lists share nothing. This is the app working correctly. |
| Chill Lofi vs. Sad but Hype | Opposite energy levels (very calm vs. very hyped), so the lists don't overlap. Lofi gets soft study tracks; Sad but Hype gets heavy, fast ones. |
| Chill Lofi vs. No-Match Neutral | These two actually share a couple of songs (like "Midnight Coding" and "Coffee Shop Stories"). That makes sense because calm, mid-level songs sit close to the "everything at 0.5" target, so the neutral listener drifts toward the mellow end. |
| Deep Intense Rock vs. Sad but Hype | Very similar lists because both want loud, aggressive music. Rock is led by "Storm Runner" and the metal-leaning profile is led by "Iron Verdict," but underneath they are pulling from the same loud group of songs. |
| Deep Intense Rock vs. No-Match Neutral | Opposite behavior. Rock confidently grabs the loudest songs; Neutral grabs medium songs and can barely tell them apart. |
| Sad but Hype vs. No-Match Neutral | Both are "broken" requests, but they fail differently. "Sad but Hype" still gets decisive picks because its loud energy setting anchors the score, while "No-Match Neutral" ends in near-ties. Lesson: even a contradictory-but-strong preference ranks better than asking for the middle of everything. |

No numeric accuracy metrics were used; evaluation was based on reading the
ranked lists and checking whether the ordering matched what each profile asked
for.

---

## 8. Future Work  

1. **Add more songs.** 18 is too few. The middle of the taste range is almost
   empty, so eclectic listeners get weak picks.
2. **Stop double-counting energy.** Energy, tempo, acousticness, and
   instrumentalness all measure about the same thing. We would combine them or
   lower their weights so one idea does not count four times.
3. **Reward near-misses.** Right now genre and mood are all-or-nothing. Similar
   genres, like lofi and ambient, should earn partial credit instead of zero.

---

## 9. Personal Reflection  

This project showed me that a recommender is just math, not magic. It only knows
what we tell it to score.

The biggest surprise was how one loud pop song kept winning for very different
users. That happened just because energy counts for so much.

It made me see that real apps like Spotify can have the same kind of hidden bias.
Small choices about weights can quietly shape what everyone hears.
