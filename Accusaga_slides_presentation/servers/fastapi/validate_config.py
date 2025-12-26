
import json
import os
import sys
from models.user_config import UserConfig

from utils.get_env import get_user_config_path_env

def validate():
    # Unset env var to test default
    if "USER_CONFIG_PATH" in os.environ:
        del os.environ["USER_CONFIG_PATH"]
        
    user_config_path = get_user_config_path_env()
    print(f"Checking config at: {user_config_path}")
    
    if not os.path.exists(user_config_path):
        print("File does not exist")
        return

    try:
        with open(user_config_path, "r") as f:
            content = f.read()
            print(f"File content: {content[:100]}...")
            data = json.loads(content)
            print("JSON load success")
            config = UserConfig(**data)
            print("Pydantic validation success")
            print(f"LLM Provider: {config.LLM}")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    validate()
