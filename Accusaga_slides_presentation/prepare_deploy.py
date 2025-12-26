import os
import shutil
import pathlib


SOURCE_DIR = os.getcwd()
DEPLOY_DIR = os.path.join(SOURCE_DIR, "deploy_output")

# Ignore patterns
IGNORE_PATTERNS = shutil.ignore_patterns(
    "node_modules", 
    "venv", 
    ".venv", 
    ".next", 
    ".git", 
    "__pycache__", 
    "*.pyc", 
    "tmp",
    ".next-build",
    "test.db",
    "chroma",
    "deploy_output"
)

def prepare_deploy():
    if os.path.exists(DEPLOY_DIR):
        print(f"Cleaning existing deploy folder: {DEPLOY_DIR}")
        shutil.rmtree(DEPLOY_DIR)
    
    print(f"Copying clean files from {SOURCE_DIR} to {DEPLOY_DIR}...")
    
    try:
        shutil.copytree(SOURCE_DIR, DEPLOY_DIR, ignore=IGNORE_PATTERNS)
        
        # Overwrite Dockerfile with Dockerfile.hf for Hugging Face deployment
        hf_dockerfile = os.path.join(SOURCE_DIR, "Dockerfile.hf")
        target_dockerfile = os.path.join(DEPLOY_DIR, "Dockerfile")
        if os.path.exists(hf_dockerfile):
            print("Overwriting Dockerfile with Dockerfile.hf")
            shutil.copy2(hf_dockerfile, target_dockerfile)
            
        print("Success! Deployment folder ready.")
        print(f"Location: {DEPLOY_DIR}")
    except Exception as e:
        print(f"Error during copy: {e}")

if __name__ == "__main__":
    prepare_deploy()
