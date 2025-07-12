#!/usr/bin/env python3
"""
Finnish to English Word Translator for Anki Deck Creation
Uses LibreTranslate API to translate words and create CSV for Anki import
"""

import requests
import csv
import time
import re
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

def translate_text(text: str, source_lang: str = 'fi', target_lang: str = 'en') -> str:
    """Translate text using local LibreTranslate instance"""
    
    url = "http://localhost:5000/translate"
    
    data = {
        'q': text,
        'source': source_lang,
        'target': target_lang,
        'format': 'text'
    }
    
    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        return result['translatedText']
    except requests.exceptions.ConnectionError:
        print(f"  Error: Cannot connect to local LibreTranslate server at {url}")
        print("  Make sure LibreTranslate is running with: libretranslate")
        return f"[CONNECTION ERROR: {text}]"
    except Exception as e:
        print(f"  Error translating '{text}': {e}")
        return f"[ERROR: {text}]"

def translate_words_batch(words: List[Tuple[str, str]], delay: float = 0.1) -> List[Tuple[str, str, str]]:
    """Translate a list of words with minimal delay (local server is fast)"""
    translated = []
    
    total = len(words)
    for i, (number, finnish_word) in enumerate(words, 1):
        print(f"Translating {i}/{total}: {finnish_word}")
        
        english_translation = translate_text(finnish_word)
        translated.append((number, finnish_word, english_translation))
        
        # Show translation result
        if not english_translation.startswith("["):
            print(f"  -> {english_translation}")
        
        # Minimal delay since it's local
        if i < total:
            time.sleep(delay)
    
    return translated

def save_to_csv(translated_words: List[Tuple[str, str, str]], output_file: str):
    """Save translated words to CSV file for Anki import"""
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header (optional, can be removed if Anki doesn't need it)
        writer.writerow(['Number', 'Finnish', 'English'])
        
        # Write translated words
        for number, finnish, english in translated_words:
            writer.writerow([number, finnish, english])

def main():
    input_file = "top_finnish_words.txt"
    output_file = "finnish_english_translations.csv"
    
    print("Reading Finnish words...")
    words = read_finnish_words(input_file)
    print(f"Found {len(words)} words to translate")
    
    print("\nStarting translation (this may take a while)...")
    translated_words = translate_words_batch(words, delay=0.5)
    
    print(f"\nSaving translations to {output_file}...")
    save_to_csv(translated_words, output_file)
    
    print(f"Done! Translated {len(translated_words)} words.")
    print(f"CSV file saved as: {output_file}")
    print("\nYou can now import this CSV file into Anki:")
    print("1. In Anki, go to File > Import")
    print("2. Select the CSV file")
    print("3. Map fields: Finnish -> Front, English -> Back")
    print("4. Choose your deck and import!")

if __name__ == "__main__":
    main()