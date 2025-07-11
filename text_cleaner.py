#!/usr/bin/env python3
import re
import argparse

def clean_text(text):
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Collapse multiple whitespace into single spaces
    text = re.sub(r'\s+', ' ', text)
    # Convert to lowercase and strip leading/trailing spaces
    return text.lower().strip()

def main():
    parser = argparse.ArgumentParser(description='Clean text from input file and append to dataset')
    parser.add_argument('--input', default='text_input.txt', help='Path to input .txt file (default: text_input.txt)')
    parser.add_argument('--output', default='dataset.txt', help='Path to dataset file to append to (default: dataset.txt)')
    args = parser.parse_args()

    # Read the input file as UTF-8
    with open(args.input, 'r', encoding='utf-8') as infile:
        data = infile.read()

    # Clean the text
    cleaned = clean_text(data)

    # Append the cleaned text to the dataset file
    with open(args.output, 'a', encoding='utf-8') as outfile:
        # Add a space before appending to separate from existing content
        if cleaned:
            outfile.write(' ' + cleaned)
    
    # Clear the input file after successful processing
    with open(args.input, 'w', encoding='utf-8') as infile:
        infile.write('')
    
    print(f"Cleaned text from '{args.input}' has been appended to '{args.output}'")
    print(f"Added {len(cleaned)} characters to the dataset.")
    print(f"'{args.input}' has been cleared and is ready for new content.")

if __name__ == '__main__':
    main()
