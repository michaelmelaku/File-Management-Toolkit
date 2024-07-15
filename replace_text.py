import os
import logging
from backup import create_backup
from utils import update_progress

def replace_string_in_files(folder, target_str, replacement_str, file_type, all_file_types, create_backup_files, backup_dir):
    modified_files_count = 0
    summary = []
    try:
        for root, dirs, files in os.walk(folder):
            for file_name in files:
                if not all_file_types and not file_name.endswith(file_type):
                    continue
                file_path = os.path.join(root, file_name)
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                            file_content = file.read()
                        if target_str in file_content:
                            new_content = file_content.replace(target_str, replacement_str)
                            if create_backup_files:
                                create_backup(file_path, backup_dir)
                            with open(file_path, 'w', encoding='utf-8', errors='ignore') as file:
                                file.write(new_content)
                            modified_files_count += 1
                            summary.append(f"Modified {file_name} in {root}")
                            logging.info(f"Replaced text in {file_name}")
                            update_progress()
                    except Exception as e:
                        logging.error(f"Could not read/write {file_name}: {e}")
    except Exception as e:
        logging.critical(f"Failed to replace text in files: {e}")

    return modified_files_count, summary
