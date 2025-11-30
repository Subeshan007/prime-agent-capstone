import shutil
import os

path = "chroma_db"

if os.path.exists(path):
    shutil.rmtree(path)
    print("Deleted chroma_db folder successfully.")
else:
    print("Folder not found.")
