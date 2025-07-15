import json
import os

def count_words(text):
    """Count the number of words in a phrase"""
    return len(text.strip().split())

def merge_frequency_data():
    """
    Merge frequency data from top_finnish_words_frequency.json 
    with the existing database in new_system/data/top_words_database.json
    """
    
    # File paths
    frequency_file = "top_finnish_words_frequency.json"
    database_file = "new_system/data/top_words_database.json"
    
    try:
        # Load frequency data
        with open(frequency_file, 'r', encoding='utf-8') as f:
            frequency_data = json.load(f)
        print(f"Loaded {len(frequency_data)} words from frequency file")
        
        # Load existing database (if it exists)
        if os.path.exists(database_file):
            with open(database_file, 'r', encoding='utf-8') as f:
                database = json.load(f)
            print(f"Loaded {len(database)} words from existing database")
        else:
            database = {}
            print("No existing database found, creating new one")
            
    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
        return
    
    # Merge logic
    words_updated = 0
    words_added = 0
    
    # Process each word from frequency data
    for finnish_word, freq_info in frequency_data.items():
        frequency_count = freq_info["frequency_count"]
        
        if finnish_word in database:
            # Word exists in database - update frequency_count
            database[finnish_word]["frequency_count"] = frequency_count
            words_updated += 1
        else:
            # Word doesn't exist in database - add it
            database[finnish_word] = {
                "phrase_word_count": count_words(finnish_word),
                "frequency_count": frequency_count,
                "english_translation": "",
                "examples": ""
            }
            words_added += 1
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(database_file), exist_ok=True)
    
    # Save updated database
    try:
        with open(database_file, 'w', encoding='utf-8') as f:
            json.dump(database, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Merge completed successfully!")
        print(f"📊 Words updated: {words_updated}")
        print(f"➕ Words added: {words_added}")
        print(f"📁 Total words in database: {len(database)}")
        print(f"💾 Database saved to: {database_file}")
        
    except Exception as e:
        print(f"Error saving database: {e}")

def main():
    """Main function to run the merge process"""
    print("🔄 Starting frequency data merge...")
    merge_frequency_data()

if __name__ == "__main__":
    main()