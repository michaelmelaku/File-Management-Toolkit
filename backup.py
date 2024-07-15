import os
import shutil
import logging

def create_backup_dir(backup_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        logging.info(f"Created backup directory at {backup_dir}")

def create_backup(file_path, backup_dir):
    backup_path = os.path.join(backup_dir, os.path.basename(file_path))
    shutil.copy(file_path, backup_path)
    logging.info(f"Created backup for {file_path} at {backup_path}")
