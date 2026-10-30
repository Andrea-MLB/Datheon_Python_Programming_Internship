# Datheon Python Programming Internship

This repository contains the completed tasks for the Datheon Technical Internship program.

## Task 1: Hangman Word Guessing Game (Console)

An interactive, modular console-based Hangman game written in Python.

### Features
* **Randomized Words:** Loads words from an external `words.txt` file and picks one with `random.choice()`.
* **ASCII Art:** Visual gallows that updates with each incorrect guess (6 mistakes allowed).
* **Input Validation:** Accepts one letter at a time and prevents duplicate guesses from penalizing the user.
* **Masked Display:** Shows the word as `_ A _ _ E` to track progress.
* **Win/Lose Screens:** Clear victory and defeat banners that reveal the word.
* **Replay & Score:** Play again right away with a running win/loss tally.

### How to Run
1. Navigate to the Task 1 directory:
   ```bash
   cd Task_1
   ```
2. Run the game (Python 3.6+, no extra packages needed):
   ```bash
   python3 hangman.py
   ```

### How to Play
1. Type a single letter and press Enter.
2. Correct letters are revealed; wrong letters add a part to the gallows.
3. Reveal the whole word to win, or make 6 wrong guesses and lose.
4. Press `y` to play again or `n` to quit (Ctrl+C also exits cleanly).

### Project Structure
```
Task_1/
├── hangman.py   # game logic (modular functions)
└── words.txt    # word list, one word per line
```

### Concepts Demonstrated
* **String manipulation:** `strip()`, `upper()`, `isalpha()`, `join()`, f-strings, `str.format()` templating
* **Control flow:** `while` loops, `if / elif / else`, early `return` / `break`
* **Data structures:** sets for guessed letters, list comprehensions
* **Modular design:** small single-purpose functions and a `__main__` entry point
* **Error handling:** `try/except` for a missing word file, Ctrl+C and EOF