import os
import datetime
import logging
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox, StringVar, ttk, Checkbutton, BooleanVar, Text, Scrollbar, Frame, Menu, Toplevel, END
from copy_files import copy_files_containing_words
from rename_files import batch_rename_files
from replace_text import replace_string_in_files
from backup import create_backup_dir
from utils import update_progress

# Configure logging
logging.basicConfig(filename='file_copier.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def create_ui():
    def browse_src_folder():
        src_folder = filedialog.askdirectory(title="Select the Source Folder")
        if src_folder:
            src_entry.delete(0, 'end')
            src_entry.insert(0, src_folder)

    def browse_dst_folder():
        dst_folder = filedialog.askdirectory(title="Select the Destination Folder")
        if dst_folder:
            dst_entry.delete(0, 'end')
            dst_entry.insert(0, dst_folder)

    def start_copying():
        src_folder = src_entry.get()
        dst_folder = dst_entry.get()
        search_words = words_entry.get()
        file_type = file_type_entry.get()
        recursive = recursive_var.get()
        create_backup_files = backup_var.get()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(dst_folder, f'backups_{timestamp}')
        all_file_types = all_file_types_var.get()

        if not src_folder or not dst_folder or not search_words:
            messagebox.showwarning("Input Error", "Please fill all required fields.")
            return

        if os.listdir(dst_folder):
            proceed = messagebox.askyesno("Destination Folder Not Empty", "The destination folder is not empty. Do you want to proceed?")
            if not proceed:
                return

        search_words_list = [word.strip() for word in search_words.split(',')]
        total_files = sum([len(files) for r, d, files in os.walk(src_folder)])
        progress_bar['maximum'] = total_files
        progress_bar['value'] = 0

        if create_backup_files:
            create_backup_dir(backup_dir)

        copied_files_count = copy_files_containing_words(src_folder, dst_folder, search_words_list, file_type, all_file_types, recursive, backup_dir, create_backup_files)

        if copied_files_count > 0:
            messagebox.showinfo("Success", f"{copied_files_count} files copied successfully.")
        else:
            messagebox.showinfo("No Files Found", "No files containing the specified words were found.")

    def browse_rename_folder():
        rename_folder = filedialog.askdirectory(title="Select the Folder to Rename Files")
        if rename_folder:
            rename_folder_entry.delete(0, 'end')
            rename_folder_entry.insert(0, rename_folder)

    def start_renaming():
        folder = rename_folder_entry.get()
        old_str = old_str_entry.get()
        new_str = new_str_entry.get()
        file_type = rename_file_type_entry.get()
        create_backup_files = backup_var.get()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(folder, f'backups_{timestamp}')
        all_file_types = all_rename_file_types_var.get()

        if not folder or not old_str or not new_str:
            messagebox.showwarning("Input Error", "Please fill all required fields.")
            return

        total_files = sum([len(files) for r, d, files in os.walk(folder)])
        progress_bar['maximum'] = total_files
        progress_bar['value'] = 0

        if create_backup_files:
            create_backup_dir(backup_dir)

        renamed_files_count = batch_rename_files(folder, old_str, new_str, file_type, all_file_types, create_backup_files, backup_dir)

        if renamed_files_count > 0:
            messagebox.showinfo("Success", f"{renamed_files_count} files renamed successfully.")
        else:
            messagebox.showinfo("No Files Renamed", "No files were renamed.")

    def browse_replace_folder():
        replace_folder = filedialog.askdirectory(title="Select the Folder to Replace Text")
        if replace_folder:
            replace_folder_entry.delete(0, 'end')
            replace_folder_entry.insert(0, replace_folder)

    def start_replacing():
        folder = replace_folder_entry.get()
        target_str = target_str_entry.get()
        replacement_str = replacement_str_entry.get()
        file_type = replace_file_type_entry.get()
        create_backup_files = backup_var.get()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(folder, f'backups_{timestamp}')
        all_file_types = all_replace_file_types_var.get()

        if not folder or not target_str or not replacement_str:
            messagebox.showwarning("Input Error", "Please fill all required fields.")
            return

        total_files = sum([len(files) for r, d, files in os.walk(folder)])
        progress_bar['maximum'] = total_files
        progress_bar['value'] = 0

        if create_backup_files:
            create_backup_dir(backup_dir)

        modified_files_count, summary = replace_string_in_files(folder, target_str, replacement_str, file_type, all_file_types, create_backup_files, backup_dir)

        if modified_files_count > 0:
            summary_window = Toplevel(root)
            summary_window.title("Summary of Replaced Files")
            summary_window.geometry("400x300")
            summary_text = Text(summary_window, wrap='word')
            summary_text.pack(expand=True, fill='both')
            for line in summary:
                summary_text.insert(END, line + "\n")
            messagebox.showinfo("Success", f"{modified_files_count} files modified successfully.")
        else:
            messagebox.showinfo("No Files Modified", "No files were modified.")

    # Main window
    root = Tk()
    root.title("File Operations")
    root.geometry("650x500")

    notebook = ttk.Notebook(root)
    copy_tab = Frame(notebook)
    rename_tab = Frame(notebook)
    replace_tab = Frame(notebook)

    notebook.add(copy_tab, text='Copy Files')
    notebook.add(rename_tab, text='Rename Files')
    notebook.add(replace_tab, text='Replace Text')
    notebook.pack(expand=True, fill='both')

    # Copy Files Tab
    Label(copy_tab, text="Source Folder:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
    src_entry = Entry(copy_tab, width=50)
    src_entry.grid(row=0, column=1, padx=10, pady=5)
    Button(copy_tab, text="Browse", command=browse_src_folder).grid(row=0, column=2, padx=10, pady=5)

    Label(copy_tab, text="Destination Folder:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
    dst_entry = Entry(copy_tab, width=50)
    dst_entry.grid(row=1, column=1, padx=10, pady=5)
    Button(copy_tab, text="Browse", command=browse_dst_folder).grid(row=1, column=2, padx=10, pady=5)

    Label(copy_tab, text="Words to Search (comma-separated):").grid(row=2, column=0, padx=10, pady=5, sticky='e')
    words_entry = Entry(copy_tab, width=50)
    words_entry.grid(row=2, column=1, padx=10, pady=5)

    Label(copy_tab, text="File Type (e.g., .txt):").grid(row=3, column=0, padx=10, pady=5, sticky='e')
    file_type_entry = Entry(copy_tab, width=50)
    file_type_entry.grid(row=3, column=1, padx=10, pady=5)

    recursive_var = BooleanVar()
    recursive_check = Checkbutton(copy_tab, text="Include Subfolders", variable=recursive_var)
    recursive_check.grid(row=4, column=1, padx=10, pady=5, sticky='w')

    all_file_types_var = BooleanVar()
    all_file_types_check = Checkbutton(copy_tab, text="All File Types", variable=all_file_types_var)
    all_file_types_check.grid(row=5, column=1, padx=10, pady=5, sticky='w')

    backup_var = BooleanVar()
    backup_check = Checkbutton(copy_tab, text="Create Backup", variable=backup_var)
    backup_check.grid(row=6, column=1, padx=10, pady=5, sticky='w')

    Button(copy_tab, text="Start Copying", command=start_copying).grid(row=7, column=1, padx=10, pady=20)

    # Rename Files Tab
    Label(rename_tab, text="Folder:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
    rename_folder_entry = Entry(rename_tab, width=50)
    rename_folder_entry.grid(row=0, column=1, padx=10, pady=5)
    Button(rename_tab, text="Browse", command=browse_rename_folder).grid(row=0, column=2, padx=10, pady=5)

    Label(rename_tab, text="Old String:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
    old_str_entry = Entry(rename_tab, width=50)
    old_str_entry.grid(row=1, column=1, padx=10, pady=5)

    Label(rename_tab, text="New String:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
    new_str_entry = Entry(rename_tab, width=50)
    new_str_entry.grid(row=2, column=1, padx=10, pady=5)

    Label(rename_tab, text="File Type (e.g., .txt):").grid(row=3, column=0, padx=10, pady=5, sticky='e')
    rename_file_type_entry = Entry(rename_tab, width=50)
    rename_file_type_entry.grid(row=3, column=1, padx=10, pady=5)

    all_rename_file_types_var = BooleanVar()
    all_rename_file_types_check = Checkbutton(rename_tab, text="All File Types", variable=all_rename_file_types_var)
    all_rename_file_types_check.grid(row=4, column=1, padx=10, pady=5, sticky='w')

    backup_check = Checkbutton(rename_tab, text="Create Backup", variable=backup_var)
    backup_check.grid(row=5, column=1, padx=10, pady=5, sticky='w')

    Button(rename_tab, text="Start Renaming", command=start_renaming).grid(row=6, column=1, padx=10, pady=20)

    # Replace Text Tab
    Label(replace_tab, text="Folder:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
    replace_folder_entry = Entry(replace_tab, width=50)
    replace_folder_entry.grid(row=0, column=1, padx=10, pady=5)
    Button(replace_tab, text="Browse", command=browse_replace_folder).grid(row=0, column=2, padx=10, pady=5)

    Label(replace_tab, text="Target String:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
    target_str_entry = Entry(replace_tab, width=50)
    target_str_entry.grid(row=1, column=1, padx=10, pady=5)

    Label(replace_tab, text="Replacement String:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
    replacement_str_entry = Entry(replace_tab, width=50)
    replacement_str_entry.grid(row=2, column=1, padx=10, pady=5)

    Label(replace_tab, text="File Type (e.g., .txt):").grid(row=3, column=0, padx=10, pady=5, sticky='e')
    replace_file_type_entry = Entry(replace_tab, width=50)
    replace_file_type_entry.grid(row=3, column=1, padx=10, pady=5)

    all_replace_file_types_var = BooleanVar()
    all_replace_file_types_check = Checkbutton(replace_tab, text="All File Types", variable=all_replace_file_types_var)
    all_replace_file_types_check.grid(row=4, column=1, padx=10, pady=5, sticky='w')

    backup_check = Checkbutton(replace_tab, text="Create Backup", variable=backup_var)
    backup_check.grid(row=5, column=1, padx=10, pady=5, sticky='w')

    Button(replace_tab, text="Start Replacing", command=start_replacing).grid(row=6, column=1, padx=10, pady=20)

    # Progress Bar
    progress_bar = ttk.Progressbar(root, length=500)
    progress_bar.pack(pady=10)

    # Run the main loop
    root.mainloop()
