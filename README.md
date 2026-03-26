# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Describe the game's purpose.**
  The game is a number guessing game built with Streamlit. The player selects a difficulty (Easy, Normal, Hard), which sets the number range and attempt limit. The player guesses a number and receives "Too High" or "Too Low" hints until they win or run out of attempts. A score system rewards correct guesses and adjusts based on attempt count.

- [x] **Detail which bugs you found.**
  Three bugs were identified:
  1. **Hard difficulty range was wrong:** `get_range_for_difficulty("Hard")` returned `(1, 50)`, making Hard easier than Normal `(1, 100)`.
  2. **Hints broke on even attempts:** The submit handler cast the secret to `str()` on even attempts and left it as `int` on odd attempts, causing `check_guess()` to enter a TypeError fallback with incorrect string-based comparisons.
  3. **New Game used wrong range:** The "New Game" button used `random.randint(1, 100)` regardless of difficulty, ignoring Easy's `(1, 20)` or Hard's corrected `(1, 200)` range. It also failed to reset score, status, and history.

- [x] **Explain what fixes you applied.**
  1. Changed Hard difficulty range from `(1, 50)` to `(1, 200)` in `logic_utils.py:8`.
  2. Removed the `str`/`int` alternation in `app.py:97-98`, always passing the secret as-is to `check_guess()`.
  3. Updated "New Game" to use `random.randint(low, high)` and added resets for score, status, and history in `app.py:71-75`.
  4. Refactored all logic functions into `logic_utils.py` so `app.py` imports from it, keeping business logic testable.

## 📸 Demo

### All 11 Tests Passing (pytest)
```
tests/test_game_logic.py::test_winning_guess PASSED
tests/test_game_logic.py::test_guess_too_high PASSED
tests/test_game_logic.py::test_guess_too_low PASSED
tests/test_game_logic.py::test_hard_range_larger_than_normal PASSED
tests/test_game_logic.py::test_hard_range_upper_bound PASSED
tests/test_game_logic.py::test_check_guess_int_types_consistent PASSED
tests/test_game_logic.py::test_check_guess_int_types_too_low PASSED
tests/test_game_logic.py::test_check_guess_int_types_win PASSED
tests/test_game_logic.py::test_easy_range PASSED
tests/test_game_logic.py::test_normal_range PASSED
tests/test_game_logic.py::test_hard_range PASSED

============================== 11 passed in 0.01s ==============================
```

### Challenge 1: Advanced Edge-Case Testing
Added 8 new pytest cases targeting the 3 bugs, including range validation for all difficulties, int-type consistency checks for `check_guess`, and a test verifying Hard's range is larger than Normal's. All 11 tests (3 original + 8 new) pass.

## 🚀 Stretch Features

- [ ] Challenge 4: Enhanced Game UI (not completed)
