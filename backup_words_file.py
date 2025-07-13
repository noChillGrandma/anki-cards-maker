#!/usr/bin/env python3
import os
import shutil
from datetime import datetime

def backup_words_file():
    """Create a backup of the current word analysis file"""
    source_file = "top_finnish_words.txt"
    
    # Create backup filename
    backup_file = "top_finnish_words_old.txt"
    
    try:
        # Check if source file exists
        if os.path.exists(source_file):
            # Copy the file
            shutil.copy2(source_file, backup_file)
            print(f"[OK] Successfully backed up '{source_file}' to '{backup_file}'")
            
            # Show file sizes for verification
            source_size = os.path.getsize(source_file)
            backup_size = os.path.getsize(backup_file)
            print(f"[OK] Source file size: {source_size} bytes")
            print(f"[OK] Backup file size: {backup_size} bytes")
        else:
            print(f"[INFO] Source file '{source_file}' does not exist yet - no backup needed")
            
    except Exception as e:
        print(f"[ERROR] Error creating backup: {e}")
        raise

if __name__ == "__main__":
    backup_words_file()