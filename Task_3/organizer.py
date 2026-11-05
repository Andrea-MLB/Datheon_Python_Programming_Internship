# organizer.py - sorts files in a messy folder into category sub-folders
import shutil
import sys
from pathlib import Path

RECURSIVE = True   # True = also sort files inside sub-folders, False = top level only

# Dictionary: file extension -> folder name
FILE_CATEGORIES = {
    '.pdf': 'Documents', '.docx': 'Documents', '.txt': 'Documents', '.xlsx': 'Documents',
    '.jpg': 'Images', '.jpeg': 'Images', '.png': 'Images', '.gif': 'Images',
    '.mp4': 'Videos', '.mkv': 'Videos', '.avi': 'Videos', '.mov': 'Videos',
    '.zip': 'Archives', '.tar': 'Archives', '.gz': 'Archives', '.rar': 'Archives',
    '.py': 'Code', '.js': 'Code', '.html': 'Code', '.css': 'Code', '.c': 'Code',
}
CATEGORY_NAMES = set(FILE_CATEGORIES.values())


def log(message):
    """Print the message and also add it to organizer.log."""
    print(message)
    with open("organizer.log", "a") as f:      # "a" = append, old lines are kept
        f.write(message + "\n")


def organize_folder(target_path):
    target_dir = Path(target_path).expanduser()
    if not target_dir.is_dir():
        log(f"Error: '{target_dir}' is not a folder.")
        return

    log(f"Scanning: {target_dir.resolve()}\n" + "-" * 40)
    moved_count = 0
    error_count = 0

    # list() makes a fixed list first, so moving files can't confuse the loop
    items = list(target_dir.rglob("*") if RECURSIVE else target_dir.iterdir())

    for item in items:
        if not item.is_file() or item.name == Path(__file__).name:
            continue                                   # skip folders and this script
        if item.relative_to(target_dir).parts[0] in CATEGORY_NAMES:
            continue                                   # already sorted, leaves it

        category = FILE_CATEGORIES.get(item.suffix.lower())
        if category is None:
            continue                                   # unknown type: leaves it alone

        dest_folder = target_dir / category
        dest_file = dest_folder / item.name

        # naming collision: photo.jpg -> photo_1.jpg -> photo_2.jpg ...
        counter = 1
        while dest_file.exists():
            dest_file = dest_folder / f"{item.stem}_{counter}{item.suffix}"
            counter += 1

        try:
            dest_folder.mkdir(exist_ok=True)           # inside try, so errors get counted
            shutil.move(str(item), str(dest_file))
            log(f"[MOVED] {item.name} -> /{category}/")
            moved_count += 1
        except PermissionError:
            log(f"[ERROR] Permission denied: {item.name}")
            error_count += 1
        except FileExistsError:
            log(f"[ERROR] Already exists: {item.name}")
            error_count += 1
        except OSError as e:                           # any other file problem
            log(f"[ERROR] Could not move {item.name}: {e}")
            error_count += 1

    log("-" * 40 + "\nEXECUTION SUMMARY")
    log(f"Total files moved: {moved_count}")
    log(f"Errors encountered: {error_count}")


if __name__ == "__main__":
    # Folder from the terminal, otherwise the Downloads folder
    organize_folder(sys.argv[1] if len(sys.argv) > 1 else "~/Downloads")