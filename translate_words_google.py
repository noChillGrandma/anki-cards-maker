#!/usr/bin/env python3
"""
Finnish to English Word Translator using Google Translate (unofficial)
Alternative approach when LibreTranslate is not working
"""

import requests
import csv
import time
import re
import urllib.parse
from typing import List, Tuple

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

def translate_with_google_unofficial(text: str) -> str:
    """
    Translate using unofficial Google Translate API
    Note: This is a workaround method and may break if Google changes their API
    """
    try:
        # URL encode the text
        encoded_text = urllib.parse.quote(text)
        
        # Google Translate URL (unofficial method)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=fi&tl=en&dt=t&q={encoded_text}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            # Google's response format: [[[translated_text, original_text, ...], ...], ...]
            if result and len(result) > 0 and len(result[0]) > 0:
                return result[0][0][0]
        
        return f"[FAILED: {text}]"
        
    except Exception as e:
        print(f"  Error translating '{text}': {e}")
        return f"[FAILED: {text}]"

def translate_words_batch(words: List[Tuple[str, str]], delay: float = 1.0) -> List[Tuple[str, str, str]]:
    """Translate a list of words with delay between requests"""
    translated = []
    
    total = len(words)
    for i, (number, finnish_word) in enumerate(words, 1):
        print(f"Translating {i}/{total}: {finnish_word}")
        
        # Try translation with retry logic
        english_translation = None
        for attempt in range(2):
            english_translation = translate_with_google_unofficial(finnish_word)
            if not english_translation.startswith("[FAILED:"):
                break
            print(f"  Retry {attempt + 1}/2 after 3 seconds...")
            time.sleep(3)
        
        translated.append((number, finnish_word, english_translation))
        print(f"  -> {english_translation}")
        
        # Add delay to be respectful
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
    output_file = "finnish_english_translations_google.csv"
    
    print("Reading Finnish words...")
    words = read_finnish_words(input_file)
    print(f"Found {len(words)} words to translate")
    
    print("\nStarting translation using Google Translate (unofficial API)...")
    print("This method is faster but may occasionally fail.")
    translated_words = translate_words_batch(words, delay=1.0)
    
    print(f"\nSaving translations to {output_file}...")
    save_to_csv(translated_words, output_file)
    
    # Count successful translations
    successful = sum(1 for _, _, eng in translated_words if not eng.startswith("[FAILED:"))
    failed = len(translated_words) - successful
    
    print(f"Done! Successfully translated {successful}/{len(translated_words)} words.")
    if failed > 0:
        print(f"Failed translations: {failed}")
    print(f"CSV file saved as: {output_file}")

if __name__ == "__main__":
    main()