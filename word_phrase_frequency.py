import re
from collections import Counter
from itertools import islice

def read_blacklist(blacklist_file):
    """Read blacklisted words and phrases from a file"""
    try:
        with open(blacklist_file, 'r', encoding='utf-8') as file:
            blacklist = set()
            for line in file:
                # Strip whitespace and convert to lowercase
                item = line.strip().lower()
                if item:  # Only add non-empty lines
                    blacklist.add(item)
            return blacklist
    except FileNotFoundError:
        print(f"Warning: Blacklist file '{blacklist_file}' not found. Proceeding without blacklist.")
        return set()

def get_ngrams(text, n, blacklist=None):
    words = re.findall(r'\b\w+\b', text.lower())  # Extract words and convert to lowercase
    ngrams = [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]
    if blacklist:
        ngrams = [ngram for ngram in ngrams if ngram not in blacklist]  # Exclude blacklisted n-grams
    return Counter(ngrams)

def analyze_text(file_path, blacklist_file=None, min_frequency=1):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    blacklist = read_blacklist(blacklist_file) if blacklist_file else None

    # Get most common n-grams and filter by minimum frequency
    all_1_grams = get_ngrams(text, 1, blacklist)
    all_2_grams = get_ngrams(text, 2, blacklist)
    all_3_grams = get_ngrams(text, 3, blacklist)
    all_4_grams = get_ngrams(text, 4, blacklist)
    
    # Filter by minimum frequency and get top 10
    most_common_1 = [(phrase, count) for phrase, count in all_1_grams.most_common() if count >= min_frequency][:10]
    most_common_2 = [(phrase, count) for phrase, count in all_2_grams.most_common() if count >= min_frequency][:10]
    most_common_3 = [(phrase, count) for phrase, count in all_3_grams.most_common() if count >= min_frequency][:10]
    most_common_4 = [(phrase, count) for phrase, count in all_4_grams.most_common() if count >= min_frequency][:10]

    # Display results
    print("\nMost Common Words:")
    for word, count in most_common_1:
        print(f"{word}: {count}")

    print("\nMost Common 2-Word Phrases:")
    for phrase, count in most_common_2:
        print(f"{phrase}: {count}")

    print("\nMost Common 3-Word Phrases:")
    for phrase, count in most_common_3:
        print(f"{phrase}: {count}")

    print("\nMost Common 4-Word Phrases:")
    for phrase, count in most_common_4:
        print(f"{phrase}: {count}")

# Usage
file_path = "dataset_clean.txt"  # Replace with your file path
blacklist_file_path = "blacklist.txt"  # Replace with your blacklist file path if available
min_frequency_threshold = 4  # Minimum frequency threshold (words/phrases with less than this count will be ignored)
analyze_text(file_path, blacklist_file_path, min_frequency_threshold)
