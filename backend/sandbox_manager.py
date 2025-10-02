import os
import shutil

BASE_SANDBOX_DIR = "/sandbox"

# Create isolated directory for user session

def isolate_user_session(user_id: str) -> str:
    user_dir = os.path.join(BASE_SANDBOX_DIR, user_id)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

# Validate that a file belongs to the user

def validate_access(user_id: str, file_path: str) -> bool:
    expected_prefix = os.path.join(BASE_SANDBOX_DIR, user_id)
    return os.path.abspath(file_path).startswith(os.path.abspath(expected_prefix))

# Move file into user's sandbox

def sandbox_file(user_id: str, source_path: str) -> str:
    user_dir = isolate_user_session(user_id)
    filename = os.path.basename(source_path)
    dest_path = os.path.join(user_dir, filename)
    shutil.move(source_path, dest_path)
    return dest_path

# List all files in user's sandbox

def list_user_files(user_id: str) -> list:
    user_dir = os.path.join(BASE_SANDBOX_DIR, user_id)
    if not os.path.exists(user_dir):
        return []
    return [os.path.join(user_dir, f) for f in os.listdir(user_dir)]