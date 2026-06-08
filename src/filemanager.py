import os, shutil

def copy_files(sourse: str, destination: str) -> None:
    for item in os.listdir(sourse):
        sourse_path = os.path.join(sourse, item)
        dest_path = os.path.join(destination, item)
        try:
            if os.path.isfile(sourse_path) or os.path.islink(sourse_path):
                print(f"{sourse_path} -> {dest_path}")
                shutil.copy(sourse_path, dest_path)
            elif os.path.isdir(sourse_path):
                print(f"{sourse_path} -> {dest_path}")
                os.mkdir(dest_path)
                copy_files(sourse_path, dest_path)
        except Exception as e:
            print(f"Failed to copy {sourse_path} to {dest_path}. Reason: {e}")

def clean_folder(folder: str) -> None:
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            print(f"deleting {file_path} in {folder}")
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
