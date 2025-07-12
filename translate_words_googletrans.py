#!/usr/bin/env python3
"""
Finnish to English Word Translator using googletrans library
Easier installation than LibreTranslate
"""

import csv
import time
import re
from typing import List, Tuple

try:
    from googletrans import Translator
except ImportError:
    print("Please install googletrans: pip install googletrans==4.0.0rc1")
    exit(1)

def read_finnish_words(file_path: str) -> List[Tuple[str, str]]:
    """Read Finnish words from the text file and return list of (number, word) tuples"""
    words = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            # Skip header and empty lines
            if line.startswith('-') or not line or line.startswith('//'):
                continue
            
            # Parse lines like "0001: ja"
            match = re.match(r'^(\d{4}):\s*(.+)$', line)
            if match:
                number = match.group(1)
                word = match.group(2)
                words.append((number, word))
    
    return words

def translate_words_batch(words: List[Tuple[str, str]], delay: float = 0.5) -> List[Tuple[str, str, str]]:
    """Translate a list of words using googletrans"""
    translator = Translator()
    translated = []
    
    total = len(words)
    for i, (number, finnish_word) in enumerate(words, 1):
        print(f"Translating {i}/{total}: {finnish_word}")
        
        try:
            result = translator.translate(finnish_word, src='fi', dest='en')
            english_translation = result.text
            print(f"  -> {english_translation}")
        except Exception as e:
            print(f"  Error: {e}")
            english_translation = f"[ERROR: {finnish_word}]"
        
        translated.append((number, finnish_word, english_translation))
        
        # Add delay to avoid rate limiting
        if i < total:
            time.sleep(delay)
    
    return translated

def save_to_csv(translated_words: List[Tuple[str, str, str]], output_file: str):
    """Save translated words to CSV file for Anki import"""
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['Number', 'Finnish', 'English'])
        
        # Write translated words
        for number, finnish, english in translated_words:
            writer.writerow([number, finnish, english])

def main():
    input_file = "top_finnish_words.txt"
    output_file = "finnish_english_translations_googletrans.csv"
    
    print("Reading Finnish words...")
    words = read_finnish_words(input_file)
    print(f"Found {len(words)} words to translate")
    
    print("\nStarting translation using googletrans...")
    translated_words = translate_words_batch(words, delay=0.5)
    
    print(f"\nSaving translations to {output_file}...")
    save_to_csv(translated_words, output_file)
    
    # Count successful translations
    successful = sum(1 for _, _, eng in translated_words if not eng.startswith("[ERROR:"))
    failed = len(translated_words) - successful
    
    print(f"Done! Successfully translated {successful}/{len(translated_words)} words.")
    if failed > 0:
        print(f"Failed translations: {failed}")
    print(f"CSV file saved as: {output_file}")

if __name__ == "__main__":
    main()