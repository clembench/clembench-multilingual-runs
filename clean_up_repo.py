import os
import argparse

REPO_DIR = "."

files_to_remove = [".tex", ".DS_Store", "transcript.html"]

def remove_files(repo_dir, remove_by_suffix=files_to_remove):
    i = 0
    for root, dirs, files in os.walk(repo_dir):
        for file in files:
            if any(file.endswith(ext) for ext in remove_by_suffix):
                file_path = os.path.join(root, file)
                # print(f"Removing {file_path}...")
                os.remove(file_path)
                i += 1
                if i % 100 == 0:
                    print(f"Removed {i} files so far...")

    print(f"Removed a total of {i} files with extensions {files_to_remove}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean up the repository by removing specified files.")
    parser.add_argument("--repo_dir", type=str, default=REPO_DIR, help="Path to the repository directory.")
    parser.add_argument("--remove_by_suffix", nargs='+', default=files_to_remove, help="List of file suffixes to remove.")
    
    args = parser.parse_args()
    
    remove_files(args.repo_dir, args.remove_by_suffix)