# Project Title
Generate README.md from Parsed Repository Data

## Description
This project provides a Python script that generates a detailed README.md file for a project based on the parsed repository data. It utilizes the CodeT5 model from Hugging Face to generate the content for the README file.

## Installation
1. Clone the repository to your local machine.
2. Install the necessary libraries by running:
   ```
   pip install transformers
   ```
3. Ensure you have Python 3.x installed on your system.

## Usage
1. Run the `parser.py` script to parse the repository data. Provide the path to the repository when prompted.
   - You can optionally specify the file extensions you want to include in the parsing process.
2. Once the repository data is parsed and saved to `parsed_data.json`, run the `inference.py` script to generate the README.md file.
3. The generated README.md will be saved in the root directory of the project.

### Important Note
-  Make sure you have an internet connection to download the model during the first run.


## License
This project is licensed under the MIT License. Feel free to modify and distribute it as needed.

---

### Additional Information
The repository contains the following scripts for parsing, inference, and generating README.md content:

#### parser.py
- This script parses a repository to collect file paths and their content.
- To use, run the script and provide the path to the repository. You can optionally specify file extensions to include.
- The parsed data is saved to a JSON file named `parsed_data.json`.

#### inference.py
- This script utilizes the ChatGPT 3.5 model to generate README content based on the parsed repository data.
- Run the script after parsing the repository data. It generates the README.md file and saves it in the project's root directory.

---

For detailed instructions on how to use the scripts and generate README content, refer to the Usage section above.