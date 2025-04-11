import json
import openai
import os

def load_parsed_data(parsed_path="parsed_data.json"):
    """
    Loads the parsed repository data from a JSON file.
    """
    with open(parsed_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_readme_with_chatgpt(files_data, use_openai=True, generator=None):
    # Load your OpenAI API key from environment
    openai.api_key = os.getenv("OPENAI_API_KEY")

    if not openai.api_key:
        print("❌ OPENAI_API_KEY is not set in environment variables.")
        return ""

    # Prepare the prompt
    prompt = (
        "You are an AI assistant. Write a complete README.md for the repository shared. Explain the purpose of the repository\n"
        "Include sections: Project Title, Description, Installation, and Usage. Go into details for installation and usage, including the necessary library and the variables the user need to input.\n\n"
        "Project files:\n"
    )

    for file_data in files_data:
        path = file_data['path']
        snippet = file_data['content'] 
        prompt += f"- Path: {path}\nContent:\n{snippet}\n\n"

    prompt += "\nNow write the full README.md content:\n"

    if(use_openai):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert software documenter."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )

            readme = response['choices'][0]['message']['content']
            return readme.strip()

        except Exception as e:
            print(f"❌ Error calling OpenAI API: {e}")
            return ""


        except Exception as e:
            print(f"❌ Error generating README.md: {e}")
            return ""
    else:
        if generator is None:
            print("❌ Local model pipeline is missing.")
            return ""

        try:
            result = generator(prompt, max_new_tokens=600, do_sample=False)[0]['generated_text']
            return result.strip()

        except Exception as e:
            print(f"❌ Local model generation error: {e}")
            return "" 


def save_readme(readme_content, repo_path):
    """
    Saves the generated README content to a file.
    """
    output_file=repo_path+"\README.md"
    if readme_content:
        with open(output_file, "w", encoding='utf-8') as f:
            f.write(readme_content)
        print(f"✅ README.md generated successfully and saved to {output_file}.")
    else:
        print("❌ Failed to generate README.md.")

def comment_code_with_chatgpt(files_data, use_openai=True, generator=None):
    """
    Adds AI-generated comments directly to original code files,
    without modifying the existing logic.
    Only processes .py, .cpp, .js, and .html files.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        print("❌ OPENAI_API_KEY is not set.")
        return

    valid_extensions = ('.py', '.cpp', '.js', '.html')

    for file in files_data:
        file_path = file["path"]
        filename = os.path.basename(file_path)

        if not filename.endswith(valid_extensions):
            continue

        content = file["content"]

        prompt = (
            f"Rewrite this {filename} file adding inline comments where you deem it necessary.\n"
            "Do not modify the existing code. Just add inline comments or comment blocks above functions, classes, or sections as needed.\n"
            "Return only the updated code with added comments.\n"
            "For a class, only generate a docstring for the whole class, do not add any comments for the class methods. \n"
            "Do not change the code, name or existing comments of the original class, method, or function, only add comments wherever necessary. \n"
            "Do not add any import statements \n"
            "Do not add bacticks to your response (') as it would modify the code \n \n"
            f"{content}"
        )
        if(use_openai):

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a senior developer helping document source code."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=1500
                )

                commented_code = response['choices'][0]['message']['content'].strip()
                #  Backup original
                with open(file_path + ".bak", "w", encoding="utf-8") as backup:
                    backup.write(content)
                    
                # Overwrite the original file
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(commented_code)

                print(f"✅ Updated with comments: {filename}")

            except Exception as e:
                print(f"❌ Failed to comment {filename}: {e}")
        else:
            if generator is None:
                    print("❌ Local model generator not provided.")
                    continue

            result = generator(prompt, max_new_tokens=1500, do_sample=False)
            commented_code = result[0]['generated_text'].strip()

            # Backup original
            with open(file_path + ".bak", "w", encoding="utf-8") as backup:
                backup.write(content)

            # Overwrite with commented version
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(commented_code)

            print(f"✅ Commented: {filename}")



def load_local_model(model_path: str):
    """
    Loads a local Hugging Face model from a user-provided directory.
    Requires model and tokenizer to be saved in that directory.
    Returns a text-generation pipeline.
    """
    print(f"🧠 Loading local model from: {model_path}...")

    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

        tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True)

        generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
        print("✅ Local model loaded successfully.")
        return generator

    except Exception as e:
        print(f"❌ Failed to load model from {model_path}: {e}")
        return None

def run_inference(repo, use_local_model=False, local_model_path=None, generate_readme=True, generate_comments=True):
    """
    Runs the inference to generate README.md from parsed files.
    """
    generator = None
    if(use_local_model):
        if not local_model_path:
            print("❌ No local model path provided.")
            return
        generator = load_local_model(local_model_path)
        parsed_path =  repo +"\parsed_data.json"
        files = load_parsed_data(parsed_path)
        if(generate_readme):
            readme_content = generate_readme_with_chatgpt(files, use_openai=False, generator=generator)
            save_readme(readme_content, repo)
        if(generate_comments):
            comment_code_with_chatgpt(files, use_openai=not use_local_model, generator=generator)
    else:
        parsed_path =  repo +"\parsed_data.json"
        files = load_parsed_data(parsed_path)
        if(generate_readme):
            readme_content = generate_readme_with_chatgpt(files)
            save_readme(readme_content, repo)
        if(generate_comments):
            comment_code_with_chatgpt(files)

