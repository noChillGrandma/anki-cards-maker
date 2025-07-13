#!/usr/bin/env python3
"""
Tatoeba Sentence Examples Extractor for Finnish Words
Gets example sentences with English translations from Tatoeba.org
"""

import requests
import csv
import time
import json
from typing import List, Tuple, Dict

def get_tatoeba_examples(finnish_word: str, max_examples: int = 10) -> str:
    """Get example sentences from Tatoeba for a Finnish word"""
    
    try:
        # Tatoeba API endpoint
        api_url = "https://tatoeba.org/en/api_v0/search"
        
        params = {
            'from': 'fin',  # Finnish
            'to': 'eng',    # English
            'query': finnish_word,
            'limit': max_examples
        }
        
        headers = {
            'User-Agent': 'Finnish-Learning-Tool/1.0 (educational use)'
        }
        
        response = requests.get(api_url, params=params, headers=headers, timeout=15)
        
        if response.status_code != 200:
            return f"[HTTP {response.status_code}]"
        
        data = response.json()
        
        # The API returns a dict with 'results' key
        if not isinstance(data, dict) or 'results' not in data:
            return "[No results in API response]"
        
        results = data['results']
        if not results:
            return "[No examples found]"
        
        examples = []
        for result in results[:max_examples]:
            # Get the Finnish sentence
            finnish_sentence = result.get('text', '').strip()
            
            # Get English translation from the nested translations array
            english_sentence = ""
            translations = result.get('translations', [])
            
            # translations is a nested array: [[...], [...], [...]]
            # Each sub-array contains translation objects
            for translation_group in translations:
                if isinstance(translation_group, list):
                    for translation in translation_group:
                        if isinstance(translation, dict) and translation.get('lang') == 'eng':
                            english_sentence = translation.get('text', '').strip()
                            break
                if english_sentence:  # Break outer loop if found
                    break
            
            # Only add if we have both sentences
            if finnish_sentence and english_sentence:
                # Format: Finnish sentence on one line, English on the next, then empty line
                examples.append(f"{finnish_sentence}\n{english_sentence}")
        
        if not examples:
            return "[No translated examples found]"
        
        # Join examples with double line breaks for clear separation
        return "\n\n".join(examples)
        
    except Exception as e:
        return f"[Error: {str(e)[:50]}]"

def load_existing_examples(csv_file: str) -> List[Tuple[str, str, str, str]]:
    """Load from basic CSV first, then merge in existing examples"""
    basic_file = "finnish_english_translations_google.csv"
    
    # Start with the current basic CSV as the source of truth
    all_words = []
    word_check = []  # Debug: track what words we're loading
    try:
        with open(basic_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if len(row) >= 3:
                    # Start with empty examples for all words
                    all_words.append((row[0], row[1], row[2], ""))
                    word_check.append(f"{row[0]}: {row[1]}")
        
        print(f"Loaded {len(all_words)} words from current basic CSV: {basic_file}")
        
        # Debug: Show first 10 and last 10 words loaded
        print("First 10 words from CSV:", word_check[:10])
        print("Last 10 words from CSV:", word_check[-10:])
        
        # Debug: Check if problematic words are in the CSV
        problem_words = ["vera", "dl", "esim", "veran"]
        found_problems = [word for word in word_check if any(prob in word.lower() for prob in problem_words)]
        if found_problems:
            print(f"WARNING: Found problematic words in CSV: {found_problems}")
        
    except FileNotFoundError:
        print(f"Error: {basic_file} not found!")
        return []
    
    # Now try to load existing examples and merge them in
    existing_examples = {}
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)  # Read header
            
            if header and len(header) >= 4:
                for row in reader:
                    if len(row) >= 4:
                        number = row[0]
                        existing_examples[number] = row[3]  # Just store the examples
                print(f"Loaded {len(existing_examples)} existing examples from {csv_file}")
    except FileNotFoundError:
        print(f"No existing examples file found: {csv_file}")
    
    # Merge existing examples into the current word list
    final_words = []
    preserved_count = 0
    for number, finnish, english, _ in all_words:
        if number in existing_examples and existing_examples[number].strip() and not existing_examples[number].startswith("["):
            # Use existing examples if available and valid
            final_words.append((number, finnish, english, existing_examples[number]))
            preserved_count += 1
            print(f"Preserved examples for word {number}: {finnish}")
        else:
            # Keep empty examples for new/missing words
            final_words.append((number, finnish, english, ""))
            print(f"New word {number}: {finnish} (needs examples)")
    
    print(f"Final result: {len(final_words)} words, {preserved_count} with preserved examples")
    return final_words

def merge_with_full_csv(existing_examples: dict) -> List[Tuple[str, str, str, str]]:
    """Merge existing examples with full basic CSV - ONLY include words that exist in basic CSV"""
    basic_file = "finnish_english_translations_google.csv"
    all_words = []
    
    try:
        with open(basic_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if len(row) >= 3:
                    number = row[0]
                    if number in existing_examples:
                        # Use existing examples ONLY if the word still exists in basic CSV
                        all_words.append(existing_examples[number])
                        print(f"Preserved examples for word {number}: {row[1]}")
                    else:
                        # Add empty examples field for new words
                        all_words.append((row[0], row[1], row[2], ""))
                        print(f"New word {number}: {row[1]} (needs examples)")
        
        print(f"Merged with current CSV: {len(all_words)} total words")
        
        # Show which old words were removed
        removed_words = set(existing_examples.keys()) - set(word[0] for word in all_words)
        if removed_words:
            print(f"Removed {len(removed_words)} words that are no longer in basic CSV: {sorted(removed_words)}")
        
        return all_words
        
    except FileNotFoundError:
        print(f"Error: {basic_file} not found!")
        return []

def load_basic_csv() -> List[Tuple[str, str, str, str]]:
    """Load words from basic CSV and add empty examples"""
    basic_file = "finnish_english_translations_google.csv"
    words = []
    try:
        with open(basic_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if len(row) >= 3:
                    # Add empty examples field
                    words.append((row[0], row[1], row[2], ""))
        print(f"Loaded {len(words)} words from basic CSV: {basic_file}")
        return words
    except FileNotFoundError:
        print(f"Error: {basic_file} not found!")
        return []

def load_csv(csv_file: str) -> List[Tuple[str, str, str]]:
    """Load words from CSV"""
    words = []
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if len(row) >= 3:
                    words.append((row[0], row[1], row[2]))
        return words
    except FileNotFoundError:
        print(f"Error: {csv_file} not found!")
        return []

def save_csv(enriched_words: List[Tuple[str, str, str, str]], output_file: str):
    """Save enriched data to CSV"""
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Number', 'Finnish', 'English', 'Examples'])
        for row in enriched_words:
            writer.writerow(row)

def main():
    output_file = "finnish_english_with_examples.csv"
    
    print("Loading existing data...")
    # Load existing examples file or fallback to basic CSV
    all_words = load_existing_examples(output_file)
    
    if not all_words:
        return
    
    # Find words that need examples
    words_needing_examples = []
    words_with_examples = []
    
    for number, finnish_word, english_translation, examples in all_words:
        # Check if examples are missing or empty or error placeholders
        if (not examples or 
            examples.strip() == "" or 
            examples.startswith("[") and examples.endswith("]")):
            words_needing_examples.append((number, finnish_word, english_translation, examples))
        else:
            words_with_examples.append((number, finnish_word, english_translation, examples))
    
    print(f"Found {len(words_with_examples)} words with existing examples (will preserve)")
    print(f"Found {len(words_needing_examples)} words needing examples")
    
    if not words_needing_examples:
        print("All words already have examples! Nothing to process.")
        return
    
    print(f"Processing {len(words_needing_examples)} words...")
    
    # Process words that need examples
    processed_words = []
    
    for i, (number, finnish_word, english_translation, old_examples) in enumerate(words_needing_examples, 1):
        print(f"{i}/{len(words_needing_examples)}: {finnish_word}")
        
        examples = get_tatoeba_examples(finnish_word, max_examples=20)  # Increased to 20 examples per word
        processed_words.append((number, finnish_word, english_translation, examples))
        
        # Be respectful to Tatoeba API
        if i < len(words_needing_examples):
            time.sleep(1.5)
    
    # Combine preserved examples with newly processed ones
    final_words = words_with_examples + processed_words
    
    # Sort by number to maintain original order
    final_words.sort(key=lambda x: int(x[0]))
    
    print(f"Saving to {output_file}...")
    save_csv(final_words, output_file)
    
    successful = sum(1 for _, _, _, examples in processed_words if not examples.startswith("["))
    print(f"Done! Processed {successful}/{len(words_needing_examples)} new examples successfully")
    print(f"Preserved {len(words_with_examples)} existing examples")
    print(f"Total words in file: {len(final_words)}")
    
    # Show sample results for newly processed words
    print("\nSample new results:")
    for _, finnish, english, examples in processed_words[:3]:
        print(f"\n{finnish} ({english}):")
        if not examples.startswith("["):
            # Show first 2 example pairs
            example_pairs = examples.split("\n\n")
            for j, pair in enumerate(example_pairs[:2], 1):
                lines = pair.split('\n')
                if len(lines) >= 2:
                    print(f"  {j}. {lines[0]}")
                    print(f"     {lines[1]}")
        else:
            print(f"  {examples}")

if __name__ == "__main__":
    main()