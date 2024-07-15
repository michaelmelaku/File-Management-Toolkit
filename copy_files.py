import os
import shutil
import logging
from utils import update_progress

def copy_files_containing_words(src_folder, dst_folder, words, file_type, all_file_types, recursive, backup_dir, create_backup):
    copied_files_count = 0
    try:
        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)

        for root, dirs, files in os.walk(src_folder):
            if not recursive:
                dirs.clear()
            for file_name in files:
                if not all_file_types and not file_name.endswith(file_type):
                    continue
                src_file = os.path.join(root, file_name)
                if os.path.isfile(src_file):
                    try:
                        with open(src_file, 'r', encoding='utf-8', errors='ignore') as file:
                            file_content = file.read()
                            if any(word in file_content for word in words):
                                relative_path = os.path.relpath(src_file, src_folder)
                                dst_file = os.path.join(dst_folder, relative_path)
                                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                                shutil.copy(src_file, dst_file)
                                copied_files_count += 1
                                logging.info(f"Copied {file_name} to {dst_file}")
                                update_progress()
                    except Exception as e:
                        logging.error(f"Could not read {file_name}: {e}")
    except Exception as e:
        logging.critical(f"Failed to copy files: {e}")

    return copied_files_count
