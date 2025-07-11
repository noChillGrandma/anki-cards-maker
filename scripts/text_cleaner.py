#!/usr/bin/env python3
import re
import argparse

def read_cleaning_blacklist(blacklist_file):
    """Read blacklisted words and phrases for cleaning"""
    try:
        with open(blacklist_file, 'r', encoding='utf-8') as file:
            blacklist = []
            for line in file:
                item = line.strip()
                if item:  # Only add non-empty lines
                    blacklist.append(item)
            return blacklist
    except FileNotFoundError:
        print(f"Warning: Cleaning blacklist file '{blacklist_file}' not found. Proceeding without cleaning blacklist.")
        return []

def clean_text(text, cleaning_blacklist=None):
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    
    # Remove URLs (http/https links)
    text = re.sub(r'https?://\S+', ' ', text)
    
    # Remove blacklisted words and phrases if provided
    if cleaning_blacklist:
        for item in cleaning_blacklist:
            # Use word boundaries for whole words, or direct replacement for symbols/phrases
            if re.match(r'^[a-zA-Z]+$', item):  # If it's a word (only letters)
                text = re.sub(r'\b' + re.escape(item) + r'\b', ' ', text, flags=re.IGNORECASE)
            else:  # For symbols, punctuation, or phrases
                text = text.replace(item, ' ')
    
    # Collapse multiple whitespace into single spaces
    text = re.sub(r'\s+', ' ', text)
    # Convert to lowercase and strip leading/trailing spaces
    return text.lower().strip()

def main():
    parser = argparse.ArgumentParser(description='Clean text from input file and append to dataset')
    parser.add_argument('--input', default='text_input.txt', help='Path to input .txt file (default: text_input.txt)')
    parser.add_argument('--output', default='dataset.txt', help='Path to dataset file to append to (default: dataset.txt)')
    parser.add_argument('--cleaning-blacklist', default='cleaning_blacklist.txt', help='Path to cleaning blacklist file (default: cleaning_blacklist.txt)')
    args = parser.parse_args()

    # Read the input file as UTF-8
    with open(args.input, 'r', encoding='utf-8') as infile:
        data = infile.read()

    # Read the cleaning blacklist
    cleaning_blacklist = read_cleaning_blacklist(args.cleaning_blacklist)

    # Clean the text
    cleaned = clean_text(data, cleaning_blacklist)

    # Append the cleaned text to the dataset file
    with open(args.output, 'a', encoding='utf-8') as outfile:
        # Add a space before appending to separate from existing content
        if cleaned:
            outfile.write(' ' + cleaned)
    
    # Clear the input file after successful processing
    with open(args.input, 'w', encoding='utf-8') as infile:
        infile.write('')
    
    print(f"✅ Cleaned text from '{args.input}' has been appended to '{args.output}'")
    print(f"✅ Added {len(cleaned)} characters to the dataset.")
    print(f"✅ '{args.input}' has been cleared and is ready for new content.")

if __name__ == '__main__':
    main()
