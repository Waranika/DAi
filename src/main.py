from parser import parse_and_save
from inference import run_inference
import os

def main():
    repo_path = input("📂 Enter the path to your repository: ").strip()
    if not os.path.isdir(repo_path):
        print("❌ Invalid folder path.")
        return

    # Prompt: generate README?
    gen_readme_input = input("📝 Generate README? (y/n): ").strip().lower()
    generate_readme = gen_readme_input in ("y", "yes")

    # Prompt: generate code comments?
    gen_comments_input = input("💬 Add code comments? (y/n): ").strip().lower()
    generate_comments = gen_comments_input in ("y", "yes")

    # Ask for model type
    use_local_input = input("🧠 Use local model instead of OpenAI? (y/n): ").strip().lower()
    use_local_model = use_local_input in ("y", "yes")

    local_model_path = None
    if use_local_model:
        local_model_path = input("📁 Enter the path to your local model folder: ").strip()
        if not os.path.isdir(local_model_path):
            print("❌ Invalid model path.")
            return

    # Parse + Save
    parse_and_save(repo_path)

    # Run inference
    run_inference(repo = repo_path, use_local_model = use_local_model, local_model_path = local_model_path, generate_readme=generate_readme, generate_comments=generate_comments)

if __name__ == "__main__":
    main()
