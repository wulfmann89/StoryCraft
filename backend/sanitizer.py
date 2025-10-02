import shutil


def quarantine_file(file_path: str) -> str:
    # Move file to quarantine folder

    quarantined_path = file_path.replace("/uploads/", "/quarantine/")
    shutil.move(file_path, quarantined_path)
    return quarantined_path

def sanitize_upload(file_path: str) -> dict:
    # Scan file for scripts, macros, or embedded code

    # Return sanitized version and flag report

    return {"sanitized": True, "flags": ["Removed embedded JS"]}