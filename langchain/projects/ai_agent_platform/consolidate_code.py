import os

# Files/Folders to ignore
IGNORE_DIRS = {
    "__pycache__",
    ".git",
    "venv",
    ".env",
    "logs",
    ".idea",
    ".vscode",
    ".pytest_cache",
    "node_modules"
}

IGNORE_FILES = {
    ".DS_Store"
}

IGNORE_EXTENSIONS = {
    ".pyc",
    ".log",
    ".md",
    ".txt"
}

OUTPUT_FILE = "codebase_dump.txt"

def should_ignore(file_path: str, is_dir: bool) -> bool:
    """
    Check if the file or directory should be ignored based on ignore lists.
    """
    name = os.path.basename(file_path)

    if is_dir:
        return name in IGNORE_DIRS

    if name in IGNORE_FILES:
        return True

    _, ext = os.path.splitext(name)
    if ext in IGNORE_EXTENSIONS:
        return True

    return False


def consolidate_code(root_dir: str):
    """
    Walks through the directory and consolidates code into a single file.
    """

    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        for dirpath, dirnames, filenames in os.walk(root_dir):

            # Filter ignored directories
            dirnames[:] = [d for d in dirnames if not should_ignore(os.path.join(dirpath, d), is_dir=True)]

            for filename in filenames:
                filepath = os.path.join(dirpath, filename)

                if should_ignore(filepath, is_dir=False):
                    continue

                # Read the file content
                try:
                    with open(filepath, "r", encoding="utf-8") as infile:
                        content = infile.read()

                        outfile.write("\n\n")
                        outfile.write("#" * 80 + "\n")
                        outfile.write(f"# FILE: {filepath}\n")
                        outfile.write("#" * 80 + "\n\n")
                        outfile.write(content)
                        outfile.write("\n\n")
                except Exception as e:
                    print(f"Skipping file {filepath} due to error: {e}")

    print(f"\n✅ Codebase consolidation complete. Output written to '{OUTPUT_FILE}'")


if __name__ == "__main__":
    project_root = "."  # Current directory
    consolidate_code(project_root)