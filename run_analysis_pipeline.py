#!/usr/bin/env python3
import subprocess
import sys
import os
from datetime import datetime

def run_command(command, description):
    """Run a command and display progress"""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}")
    print(f"Command: {command}")
    print(f"Started at: {datetime.now().strftime('%H:%M:%S')}")
    print("-" * 60)
    
    try:
        # Run the command and capture output
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # Print stdout if there's any
        if result.stdout:
            print("Output:")
            print(result.stdout)
        
        # Print stderr if there's any
        if result.stderr:
            print("Errors/Warnings:")
            print(result.stderr)
        
        # Check return code
        if result.returncode == 0:
            print(f"✅ {description} completed successfully!")
        else:
            print(f"❌ {description} failed with return code {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False
    
    print(f"Finished at: {datetime.now().strftime('%H:%M:%S')}")
    return True

def main():
    print("🚀 Starting Finnish Words Analysis Pipeline")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Define the pipeline steps
    steps = [
        {
            "command": "python scripts\\text_cleaner.py",
            "description": "Step 1: Cleaning and processing text input"
        },
        {
            "command": "python scripts\\backup_words_file.py",
            "description": "Step 2: Backing up previous top words list..."
        },
        {
            "command": "python scripts\\word_phrase_frequency.py",
            "description": "Step 3: Analyzing word and phrase frequencies"
        },
        {
            "command": "python scripts\\compare_ranks.py top_finnish_words_old.txt top_finnish_words.txt -o diff.txt",
            "description": "Step 4: Comparing new to list with old list..."
        },
        {
            "command": "python scripts\\translate_words_google.py",
            "description": "Step 5: Translating new words..."
        },
        {
            "command": "python scripts\\tatoeba_examples.py",
            "description": "Step 6: Extracting examples for new words from Tatoeba..."
        },
        
    ]
    
    # Track success/failure
    successful_steps = 0
    total_steps = len(steps)
    
    # Run each step
    for i, step in enumerate(steps, 1):
        print(f"\n🔢 Pipeline Progress: {i}/{total_steps}")
        
        success = run_command(step["command"], step["description"])
        
        if success:
            successful_steps += 1
        else:
            print(f"\n💥 Pipeline failed at step {i}")
            break
    
    # Final summary
    print(f"\n{'='*60}")
    print("📊 PIPELINE SUMMARY")
    print(f"{'='*60}")
    print(f"Total steps: {total_steps}")
    print(f"Successful steps: {successful_steps}")
    print(f"Failed steps: {total_steps - successful_steps}")
    
    if successful_steps == total_steps:
        print("🎉 All steps completed successfully!")
        print("\n📄 Generated files:")
        files_to_check = ["dataset.txt", "top_finnish_words.txt", "top_finnish_words_old.txt", "diff.txt"]
        for file in files_to_check:
            if os.path.exists(file):
                size = os.path.getsize(file)
                print(f"  ✅ {file} ({size} bytes)")
            else:
                print(f"  ❌ {file} (not found)")
    else:
        print("❌ Pipeline completed with errors")
    
    print(f"\nFinished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()