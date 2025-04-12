# DAi
Document your ticket with AI !
This project is open source and will have the MIT license, feel free to fork it and improve

## Description
This repository contains a tool for generating documentation for AI projects. The tool parses the repository files, runs inference to generate README files, and adds AI-generated comments to code files. It provides options to use a local model or the OpenAI API for generating documentation.

## Installation
1. Clone the repository to your local machine.
2. Make sure you have Python installed.
3. Install the necessary libraries by running:
   ```
   pip install PyQt5 openai transformers
   ```
4. Ensure you have an OpenAI API key set in your environment variables if using the OpenAI model. You can do so with: 
```
 setx OPENAI_API_KEY = "Your API Key here"
 ```

5. If you wish to use your own model have it ready in a folder straight from hugginface

## Usage
1. Run the `DAi_GUI.py` file located in the `src` directory.
2. Enter the path to the repository in the provided field.
3. Check the options to generate README and add comments.
4. If using a local model, enable the checkbox and provide the path to the local model folder.
5. Click on the "Run" button to start the documentation generation process.

### Variables
- `repo_path`: Path to the repository directory.
- `use_local_model`: Boolean indicating whether to use a local model or the OpenAI API.
- `model_path`: Path to the local model folder if `use_local_model` is enabled.
- `generate_readme`: Boolean to generate README files.
- `generate_comments`: Boolean to add AI-generated comments to code files.

### Controls in GUI
- Repository Path: Input field to enter the path to the repository.
- Browse: Button to browse and select the repository folder.
- Use local model: Checkbox to select using a local model for inference.
- Path to local model folder: Input field for the path to the local model folder.
- Browse: Button to browse and select the local model folder.
- Generate README: Checkbox to generate README files.
- Generate Comments: Checkbox to add AI-generated comments.
- Run: Button to start the documentation generation process.
- Log Output: Text area to display the processing logs.
  
  ![image](https://github.com/user-attachments/assets/38d715d5-8ac0-4e75-966c-db19b3a82ad5)


### Additional Information
- The `inference.py` file contains functions for generating README files and adding comments using either the OpenAI API or a local model.
- The `main.py` file provides a command-line interface for running the documentation generation process.
- The `parser.py` file handles parsing the repository files and saving the parsed data.
- The `timetest.py` and files in the `test` directory are for testing purposes and example documentation content.

Enjoy automating your AI project documentation with this tool!
