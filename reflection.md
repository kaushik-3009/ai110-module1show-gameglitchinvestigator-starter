# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

### 3 Bugs Found

**Bug 1: Hard difficulty range is smaller than Normal.**
In `get_range_for_difficulty()`, "Normal" returns `(1, 100)` but "Hard" returns `(1, 50)`. Hard should be harder, meaning a larger range. This makes Hard easier than Normal.

**Bug 2: Secret number changes randomly on even attempts.**
In the submit handler (lines 158-161), the secret is cast to `str()` on every even attempt and left as `int` on odd attempts. This causes `check_guess()` to fall into the `except TypeError` block on even attempts, where string comparison produces incorrect "Too High"/"Too Low" results.

**Bug 3: "New Game" resets secret with wrong range.**
The `new_game` button (line 136) uses `random.randint(1, 100)` regardless of the selected difficulty. If the player is on Easy (range 1-20) or Hard (range 1-50), the secret number may be generated outside the expected range, making the game unwinnable.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

### AI Tool Used
I used **Copilot (OpenCode)** as my AI teammate throughout the project.

### Correct AI Suggestion
**What the AI suggested:** When I asked the AI to identify bugs in the code, it correctly spotted that in `app.py` lines 158-161, the secret was being cast to `str()` on even attempts and left as `int` on odd attempts. The AI explained that this caused `check_guess()` to enter the `except TypeError` fallback block on even attempts, where string comparison (e.g., `"60" > "50"`) produced wrong "Too High"/"Too Low" hints.

**How I verified:** I wrote the test `test_check_guess_int_types_consistent` which calls `check_guess(75, 50)` with both arguments as ints. Before the fix, if a `str` secret was passed, the TypeError block would compare `"75" > "50"` lexicographically, which works but produces incorrect results for other values. Running `pytest` after the fix confirmed the test passed with correct int-based comparison.

### Incorrect/Misleading AI Suggestion
**What the AI suggested:** When fixing the "New Game" button bug, the AI initially only suggested changing `random.randint(1, 100)` to `random.randint(low, high)`. This was partially correct but misleading because it did not mention that `score`, `status`, and `history` should also be reset when starting a new game. Without resetting those, a player clicking "New Game" would keep their old score and possibly see stale game-over messages.

**How I verified:** I manually tested the game in Streamlit by winning a game, then clicking "New Game". Without the full reset, the score carried over and the status stayed as "won". After I added `st.session_state.score = 0`, `st.session_state.status = "playing"`, and `st.session_state.history = []`, the new game started cleanly with score at 0 and a fresh playing state.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

### How I decided a bug was fixed
I decided a bug was fixed when two things were true: the code change made logical sense when reading it, and a corresponding pytest case passed. For example, after removing the `str`/`int` alternation, I didn't just trust the code looked right, I ran `test_check_guess_int_types_consistent` which calls `check_guess(75, 50)` and asserts the outcome is "Too High". Before the fix, passing a `str` secret would have triggered the TypeError fallback. After the fix, the test passed, confirming both types stay as int throughout.

### A test I ran
`test_hard_range_larger_than_normal` verifies that the Hard difficulty range is actually larger than Normal. It calls `get_range_for_difficulty("Hard")` and `get_range_for_difficulty("Normal")`, then asserts `(hard_high - hard_low) > (normal_high - normal_low)`. This test failed when Hard returned `(1, 50)` and passed after I changed it to `(1, 200)`. It showed me that a bug can exist in plain sight, the range looked like a valid number, but the relationship between difficulty levels was wrong.

### How AI helped with tests
The AI helped me design the edge-case tests by suggesting specific scenarios to cover. When I asked for tests targeting the str/int bug, it suggested testing `check_guess` with both arguments as ints and verifying the correct outcome. It also suggested testing each difficulty range independently. I used these suggestions as a starting point and added the `test_hard_range_larger_than_normal` comparison test myself to catch relational bugs, not just absolute values.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

### Streamlit reruns and session state
I would explain it like this: every time you click a button or interact with a widget, Streamlit reruns the entire Python script from top to bottom. That means any regular variable you set (like `secret = 42`) gets reset to its original value on the next interaction. Session state (`st.session_state`) is Streamlit's way of giving you a "pocket" that survives between reruns, like a backpack you carry through every rerun. If you store `st.session_state.secret = 42`, it stays 42 until you explicitly change it. The bug in this game happened because the secret was being recalculated or cast to a different type on each rerun instead of being kept stable in session state. Understanding this helped me see why the `str`/`int` alternation was so destructive, every even-numbered click literally changed the type of the secret mid-game.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

### Habit to reuse
I want to keep writing tests before trusting a fix. In this project, I didn't just change the code and assume it worked, I wrote a pytest case that would fail on the buggy version and pass on the fixed version. This "test first, verify second" approach caught issues that looked correct in the code but behaved wrong at runtime. I plan to use this in future labs by writing at least one test per bug I fix.

### What I would do differently
Next time I work with AI on a coding task, I would ask the AI to explain its reasoning before accepting a suggestion. In this project, the AI's New Game fix was incomplete because it only addressed the obvious part (the randint range) without thinking about related state like score and status. If I had asked "what else needs to reset when starting a new game?" I would have caught that gap immediately instead of discovering it during manual testing.

### How this project changed my thinking
This project taught me that AI-generated code is a starting point, not a finished product. The AI can spot patterns and suggest fixes quickly, but it doesn't always think about edge cases or side effects. My job as a developer is to verify every suggestion with tests and manual checks before accepting it.
