from logic_utils import check_guess, get_range_for_difficulty


# FIX: Original tests compared result == "Win" but check_guess returns a tuple. AI correctly identified the type mismatch and suggested result[0].
def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result[0] == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result[0] == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result[0] == "Too Low"


# --- Tests for Bug 1: Hard difficulty range must be larger than Normal ---


def test_hard_range_larger_than_normal():
    hard_low, hard_high = get_range_for_difficulty("Hard")
    normal_low, normal_high = get_range_for_difficulty("Normal")
    assert (hard_high - hard_low) > (normal_high - normal_low)


def test_hard_range_upper_bound():
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > 100


# --- Tests for Bug 2: Hints must work correctly with int types (no str mixing) ---


def test_check_guess_int_types_consistent():
    # When both guess and secret are ints, "Too High" should be returned
    outcome, _ = check_guess(75, 50)
    assert outcome == "Too High"


def test_check_guess_int_types_too_low():
    # When both guess and secret are ints, "Too Low" should be returned
    outcome, _ = check_guess(25, 50)
    assert outcome == "Too Low"


def test_check_guess_int_types_win():
    # When both guess and secret are ints, win should work
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


# --- Tests for Bug 3: New Game must use correct difficulty range ---


def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20


def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100


def test_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 200
