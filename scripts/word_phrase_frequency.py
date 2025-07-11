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
    
    # Combine all n-grams into a single list and filter by minimum frequency
    all_ngrams = []
    for ngram_dict in [all_1_grams, all_2_grams, all_3_grams, all_4_grams]:
        for phrase, count in ngram_dict.items():
            if count >= min_frequency:
                all_ngrams.append((phrase, count))
    
    # Sort by frequency (descending) and limit to top 1000
    top_ngrams = sorted(all_ngrams, key=lambda x: x[1], reverse=True)[:1000]

    # Write results to file
    output_file = "top_finnish_words.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("----- Top Words and Phrases -----\n")
        for position, (phrase, count) in enumerate(top_ngrams, 1):
            f.write(f"{position:04d}: {phrase}\n")
    
    print(f"[OK] Results have been written to '{output_file}'")
    print(f"[OK] Total entries: {len(top_ngrams)}")

# Usage
file_path = "dataset.txt"  # Replace with your file path
blacklist_file_path = "blacklist.txt"  # Replace with your blacklist file path if available
min_frequency_threshold = 3  # Minimum frequency threshold (words/phrases with less than this count will be ignored)
analyze_text(file_path, blacklist_file_path, min_frequency_threshold)
