"""Hangman: an interactive console game. Guess the word before the gallows is built."""
import os
import random

MAX_MISTAKES = 6
FALLBACK_WORDS = ["python", "gallows", "keyboard", "terminal", "algorithm"]

# One gallows template; slot {n} is filled with a body part after the n-th mistake.
GALLOWS = """
  +---+
  |   |
  {0}   |
 {1}{2}{3}  |
 {4} {5}  |
      |
========="""
BODY = ["O", "/", "|", "\\", "/", "\\"]  # head, arm, torso, arm, leg, leg


# ---------- word handling ----------
def load_words(min_len=4):
    """Read words.txt next to this script; keep clean alphabetic words only."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "words.txt")
    try:
        with open(path) as f:
            words = [w.strip() for w in f if len(w.strip()) >= min_len and w.strip().isalpha()]
    except OSError:
        words = []
    return words or FALLBACK_WORDS  # empty/missing file -> built-in list


def pick_word(words):
    """Choose the secret word at random, in uppercase for easy comparison."""
    return random.choice(words).upper()


def mask_word(word, good):
    """Build the display string: revealed letters stay, the rest become '_'."""
    return " ".join(ch if ch in good else "_" for ch in word)


def is_solved(word, good):
    """The word is solved when all its distinct letters have been guessed."""
    return set(word) <= good


# ---------- display ----------
def draw_gallows(mistakes):
    """Return the gallows showing the first `mistakes` body parts."""
    parts = [p if i < mistakes else " " for i, p in enumerate(BODY)]
    return GALLOWS.format(*parts)


def show_status(word, good, bad):
    """Print the gallows, masked word and wrong letters so far."""
    print(draw_gallows(len(bad)))
    print("\nWord:  ", mask_word(word, good))
    print("Missed:", " ".join(sorted(bad)) or "-", f"({MAX_MISTAKES - len(bad)} left)")


def show_result(word, won):
    """Print the victory or defeat banner."""
    banner = "YOU WIN!" if won else "GAME OVER"
    print(f"\n{'=' * 30}\n{banner:^30}\nThe word was: {word}\n{'=' * 30}")


# ---------- input ----------
def get_guess(tried):
    """Keep asking until the player types a single NEW letter."""
    while True:
        guess = input("\nGuess a letter: ").strip().upper()
        if len(guess) != 1 or not guess.isalpha():
            print("Please type exactly one letter (A-Z).")
        elif guess in tried:
            print(f"You already tried '{guess}' - no penalty, pick another.")
        else:
            return guess


def ask_play_again():
    """Return True if the player answers yes."""
    return input("\nPlay again? (y/n): ").strip().lower().startswith("y")


# ---------- game flow ----------
def play_round(words):
    """Play one game; return True for a win, False for a loss."""
    word = pick_word(words)
    good, bad = set(), set()

    while len(bad) < MAX_MISTAKES and not is_solved(word, good):
        show_status(word, good, bad)
        guess = get_guess(good | bad)
        (good if guess in word else bad).add(guess)

    won = is_solved(word, good)
    print(draw_gallows(len(bad)))
    show_result(word, won)
    return won


def main():
    words = load_words()
    wins = losses = 0
    print("Welcome to HANGMAN! You have", MAX_MISTAKES, "mistakes.")
    while True:
        if play_round(words):
            wins += 1
        else:
            losses += 1
        print(f"Score -> Wins: {wins}  Losses: {losses}")
        if not ask_play_again():
            break
    print("Thanks for playing!")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")