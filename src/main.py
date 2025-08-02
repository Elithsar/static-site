import os
import shutil
from textnode import TextType, TextNode

def main():
    copy_and_clean_directory("static", "public")

def copy_and_clean_directory(source_dir, dest_dir):
    """    Recursively copies all contents from source_dir to dest_dir.
    Cleans the destination directory before copying."""
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    else:
        for item in os.listdir(dest_dir):
            item_path = os.path.join(dest_dir, item)
            if os.path.isdir(item_path):
                os.rmdir(item_path)
            else:
                os.remove(item_path)
    
    for item in os.listdir(source_dir):
        source_item_path = os.path.join(source_dir, item)
        dest_item_path = os.path.join(dest_dir, item)

        shutil.copy(source_item_path, dest_item_path)
        print(f"Copied: {source_item_path} to {dest_item_path}")

if __name__ == "__main__":
    main()
