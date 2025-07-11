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
    parser = argparse.ArgumentParser(description='Clean a .txt file for n-gram analysis')
    parser.add_argument('input', help='Path to input .txt file')
    parser.add_argument('output', help='Path to output cleaned .txt file')
    args = parser.parse_args()

    # Read the input file as UTF-8
    with open(args.input, 'r', encoding='utf-8') as infile:
        data = infile.read()

    # Clean the text
    cleaned = clean_text(data)

    # Write the cleaned text to output
    with open(args.output, 'w', encoding='utf-8') as outfile:
        outfile.write(cleaned)

if __name__ == '__main__':
    main()
