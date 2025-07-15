import json
import csv
import re
import os

def count_words(phrase):
    """Count the number of words in a Finnish phrase."""
    # Remove punctuation and split by whitespace
    words = re.findall(r'\b\w+\b', phrase.lower())
    return len(words)

def convert_csv_to_json(csv_file):
    """Convert the CSV file to the specified JSON structure."""
    
    finnish_data = {}
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                finnish_word = row['Finnish'].strip()
                english_translation = row['English'].strip()
                examples = row['Examples'].strip()
                
                # Create the structured data
                finnish_data[finnish_word] = {
                    "phrase_word_count": count_words(finnish_word),
                    "frequency_count": 0,  # Set to 0 for now as requested
                    "english_translation": english_translation,
                    "examples": examples
                }
                
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found")
        return {}
    except Exception as e:
        print(f"Error processing CSV file: {e}")
        return {}
    
    return finnish_data

def save_to_json_file(data, filename="data/top_words_database.json"):
    """Save the data to a JSON file."""
    filepath = f"c:\\Users\\JAMK\\Documents\\GitHub\\anki-cards-maker\\{filename}"
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"Finnish words data saved to: {filepath}")
    return filepath

def main():
    """Main function to convert and save the Finnish words data."""
    print("Converting Finnish words CSV to JSON structure...")
    
    # Convert from CSV file
    csv_file = "finnish_english_with_examples.csv"
    finnish_data = convert_csv_to_json(csv_file)
    
    if not finnish_data:
        print("No data to save. Please check your CSV file.")
        return
    
    # Save to file
    save_to_json_file(finnish_data)
    
    # Print sample output
    print(f"\nGenerated {len(finnish_data)} Finnish word entries.")
    print("\nSample entries:")
    for i, (word, data) in enumerate(list(finnish_data.items())[:3]):
        print(f"{word}: {data}")
    
    print("\nData structure for each word:")
    print("- phrase_word_count: Number of words in the phrase")
    print("- frequency_count: Set to 0 (to be updated later)")
    print("- english_translation: Translation from CSV")
    print("- examples: Examples from CSV")

if __name__ == "__main__":
    main()