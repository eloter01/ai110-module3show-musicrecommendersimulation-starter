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

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

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
