---

## Task 3: Desktop Directory Organizer (Automation)

A Python utility that automatically cleans up cluttered folders (like Downloads or Desktop) by categorizing files into subfolders based on their extensions.

### Features
* **Autonomous Execution:** Takes the target path as a command-line argument (`sys.argv`), defaulting to `~/Downloads` if no argument is provided.
* **Recursive Traversal:** Can optionally scan nested folders (controlled by the `RECURSIVE` flag) while safely avoiding re-sorting files that are already in category folders.
* **Safe Logging:** Simultaneously prints to the console and appends to `organizer.log` without needing external libraries.
* **Collision Handling:** Prevents overwriting by renaming duplicate files (e.g., `photo.jpg` becomes `photo_1.jpg`).
* **Robust Error Handling:** Uses `try-except` blocks to catch `PermissionError`, `FileExistsError` and `OSError` (like if a drive is unmounted mid-run) without crashing the script.
* **Junk Filtering:** Ignores unknown file types and system junk, leaving them untouched rather than sweeping them into an "Others" folder.
* **Self-Protection:** Skips `organizer.py` itself, so the script never moves itself into `Code/`.

### Requirements
* Python 3.6 or newer (uses f-strings and `pathlib`)
* No external packages, only the standard library (`shutil`, `sys`, `pathlib`)

### How to Run
1. Navigate to the Task 3 directory:
   ```bash
   cd Task_3
   ```
2. Run the script on a specific folder:
   ```bash
   python organizer.py "C:/Users/YourName/Downloads"
   ```
   or on Linux/macOS:
   ```bash
   python3 organizer.py ~/Downloads
   ```
3. Run it with no argument to clean your default `~/Downloads` folder:
   ```bash
   python organizer.py
   ```

> **Tip:** Try it on a small test folder first. Moving files is not automatically undone, although every move is recorded in `organizer.log` so you can reverse it by hand.

### Configuration
| Setting | Where | What it does |
|---|---|---|
| `RECURSIVE` | Top of `organizer.py` | `True` sorts files inside sub-folders too. `False` sorts only the top level. |
| `FILE_CATEGORIES` | Top of `organizer.py` | Dictionary mapping an extension to a folder name. Add a line to support a new file type. |

### Categories
| Folder | Extensions |
|---|---|
| Documents | `.pdf` `.docx` `.txt` `.xlsx` |
| Images | `.jpg` `.jpeg` `.png` `.gif` |
| Videos | `.mp4` `.mkv` `.avi` `.mov` |
| Archives | `.zip` `.tar` `.gz` `.rar` |
| Code | `.py` `.js` `.html` `.css` `.c` |

Extensions are matched in lowercase, so `PHOTO.JPG` and `photo.jpg` are treated the same. Any other extension is left where it is.

### Example Output
```text
Scanning: /home/user/Downloads
----------------------------------------
[MOVED] b.JPG -> /Images/
[MOVED] x.zip -> /Archives/
[MOVED] a.pdf -> /Documents/
[MOVED] run.py -> /Code/
[MOVED] a.pdf -> /Documents/
[MOVED] c.png -> /Images/
----------------------------------------
EXECUTION SUMMARY
Total files moved: 6
Errors encountered: 0
```
The second `a.pdf` is saved as `a_1.pdf` because a file with that name was already in `Documents/`.

### How It Works
1. Check that the target path is a real folder. If not, print an error and stop.
2. Build a fixed list of files (`rglob` if `RECURSIVE` is on, otherwise `iterdir`), so moving files doesn't disturb the loop.
3. Skip folders, the script itself, and files already inside a category folder.
4. Look up the lowercase extension in `FILE_CATEGORIES`. Unknown types are skipped.
5. If the destination name already exists, add `_1`, `_2`, and so on until it is free.
6. Create the category folder if needed, then move the file with `shutil.move()`. Any error is logged and counted, and the script carries on with the next file.
7. Print the execution summary.

### Notes and Limitations
* `organizer.log` is created in the folder you run the command from, not in the target folder. Its `.log` extension is not in the category list, so it is never moved.
* With `RECURSIVE = True`, files are pulled out of every sub-folder. Avoid pointing it at a project folder, because it will scatter the project's files. Set the flag to `False` for a safer top-level-only clean-up.
* Files with no entry in `FILE_CATEGORIES` stay exactly where they are.

---