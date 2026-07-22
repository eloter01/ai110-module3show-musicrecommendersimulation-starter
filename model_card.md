# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

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

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
