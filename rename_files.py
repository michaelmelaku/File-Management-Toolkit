import os
import logging
from backup import create_backup
from utils import update_progress

def batch_rename_files(folder, old_str, new_str, file_type, all_file_types, create_backup_files, backup_dir):
    renamed_files_count = 0
    try:
        for root, dirs, files in os.walk(folder):
            for file_name in files:
                if not all_file_types and not file_name.endswith(file_type):
                    continue
                if old_str in file_name:
                    new_file_name = file_name.replace(old_str, new_str)
                    src_file = os.path.join(root, file_name)
                    dst_file = os.path.join(root, new_file_name)
                    if create_backup_files:
                        create_backup(src_file, backup_dir)
                    os.rename(src_file, dst_file)
                    renamed_files_count += 1
                    logging.info(f"Renamed {file_name} to {new_file_name}")
                    update_progress()
    except Exception as e:
        logging.critical(f"Failed to rename files: {e}")

    return renamed_files_count
