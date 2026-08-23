#!/usr/bin/env python3
import os
import shutil
import sys
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.bmp', '.tiff'],
    'Documents': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx', '.csv', '.md'],
    'Videos': ['.mp4', '.mov', '.avi', '.mkv', '.wmv'],
    'Music': ['.mp3', '.wav', '.flac', '.aac'],
    'Archives': ['.zip', '.tar', '.gz', '.rar', '.7z'],
    'Scripts': ['.py', '.sh', '.js', '.bat', '.ps1'],
}

def organize_downloads(folder_path):
    if not os.path.exists(folder_path):
        return f"Error: Downloads folder not found: {folder_path}"

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if not files:
        return "No files found in Downloads folder."

    moved_count = 0
    category_counts = {}
    log_lines = []

    for filename in files:
        file_path = os.path.join(folder_path, filename)
        ext = os.path.splitext(filename)[1].lower()
        target_category = None
        for category, extensions in CATEGORIES.items():
            if ext in extensions:
                target_category = category
                break
        if target_category is None:
            continue
        target_dir = os.path.join(folder_path, target_category)
        os.makedirs(target_dir, exist_ok=True)
        dest = os.path.join(target_dir, filename)
        if os.path.exists(dest):
            base, ext_orig = os.path.splitext(filename)
            counter = 1
            while os.path.exists(dest):
                dest = os.path.join(target_dir, f"{base}_{counter}{ext_orig}")
                counter += 1
        shutil.move(file_path, dest)
        moved_count += 1
        category_counts[target_category] = category_counts.get(target_category, 0) + 1
        log_lines.append(f"  ✓ {filename} -> {target_category}/")

    result = f"SUCCESS: {moved_count} file(s) organized!\n\n"
    if category_counts:
        result += "Categories:\n"
        for cat, count in category_counts.items():
            result += f"   - {cat}: {count}\n"
    result += "\n".join(log_lines)
    return result

def show_gui(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("File Organizer", message)
    root.destroy()

if __name__ == '__main__':
    downloads = os.path.expanduser('~/Downloads')
    result = organize_downloads(downloads)
    show_gui(result)
    print(result)
