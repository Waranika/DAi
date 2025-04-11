import json
import os
import pathlib
from pathlib import Path
from typing import Dict, List


def parse_repository(repo_path: str, extensions: List[str] = None) -> List[Dict]:
    """
    Parses a repository to collect file paths and their content.

    Args:
        repo_path (str): The root directory of the repository to parse.
        extensions (List[str], optional): A list of file extensions to include. 
                                          If None, all files are included.

    Returns:
        List[Dict]: A list of dictionaries with file information.
    """

    files_data = []

    # Walk through the directory tree starting from repo_path
    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = Path(file_path).suffix

            # If extensions are specified, skip files that don't match
            if extensions and file_extension not in extensions:
                continue

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Store the file data in a dictionary
                files_data.append({
                    "path": file_path,
                    "name": file,
                    "content": content  
                })
            except Exception as e:
                print(f"Could not read file {file_path}: {e}")

    return files_data


def save_parsed_data(files_data: List[Dict], repo_path: str ) -> None:
    """
    Saves the parsed data to a JSON file.

    Args:
        files_data (List[Dict]): The parsed file data.
        output_file (str): The path to the JSON file where data will be saved.
    """
    output_file = repo_path + "\parsed_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(files_data, f, indent=4)

def parse_and_save(repo_path: str):
    
    extensions = ['.py', '.cpp', '.h', '.js', '.html', '.css', '.md']

    parsed_files = parse_repository(repo_path, extensions)
    save_parsed_data(parsed_files, repo_path)

    print(f"✅ Parsed {len(parsed_files)} files and saved to 'parsed_data.json'.")


if __name__ == "__main__":
    # Example usage
    repo_path = input("Enter the path to the repository: ")
    
    # Optional: Specify file extensions you want to parse
    extensions = ['.py', '.cpp', '.h', '.js', '.html', '.css', '.md']

    # Parse the repository and save the parsed data
    parsed_files = parse_repository(repo_path, extensions)
    save_parsed_data(parsed_files, repo_path)

    print(f"✅ Parsed {len(parsed_files)} files successfully and saved to 'parsed_data.json'.")