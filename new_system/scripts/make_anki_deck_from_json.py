#!/usr/bin/env python3
"""
Enhanced Anki Deck Creator from JSON Database
Creates Anki decks from JSON database with Finnish words, translations, and examples
"""

# pip install genanki
import genanki
import json
import hashlib

VERSION = '1.0.5'  # Version for output file naming
INPUT_FILE = 'new_system/data/top_words_database.json'   # JSON database
BATCH_SIZE = 200  # Number of words per batch
OUTPUT_FILE = f'anki_deck/top_1k_finnish_words_v{VERSION}.apkg'  # Enhanced output file

def generate_note_id(finnish_word):
    """Generate a stable note ID based on the Finnish word"""
    hash_object = hashlib.md5(finnish_word.encode('utf-8'))
    return int(hash_object.hexdigest()[:8], 16)

# Enhanced model with examples field
model = genanki.Model(
    1607392321,  # New model ID for examples version
    'Finnish-English-Examples Model',
    fields=[
        {'name': 'Finnish'},
        {'name': 'English'},
        {'name': 'Examples'},
        {'name': 'Rank'}
    ],
    templates=[
        {
            'name': 'Finnish → English + Examples',
            'qfmt': '<div class="card front">🇫🇮 {{Finnish}}</div>',
            'afmt': '''{{FrontSide}}
            <hr>
            <div class="card back">
                <div class="translation">🇬🇧 {{English}}</div>
                <div class="examples">{{Examples}}</div>
            </div>'''
        },
    ],
    css="""
        .card {
            background: #1a1a1a;
            color: #fff;
            font-family: 'Helvetica Neue', sans-serif;
            text-align: center;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        .front {
            font-size: 32px;
            font-weight: 600;
        }
        .translation {
            font-size: 24px;
            font-weight: 500;
            margin-bottom: 15px;
            color: #4CAF50;
        }
        .examples {
            font-size: 16px;
            font-weight: 400;
            color: #81C784;
            background: rgba(129, 199, 132, 0.1);
            padding: 15px;
            border-radius: 8px;
            border-left: 3px solid #81C784;
            text-align: left;
            max-width: 600px;
            margin: 0 auto;
            line-height: 1.6;
            white-space: pre-line;
        }
        hr {
            margin: 20px 0;
            border: none;
            border-top: 1px solid #333;
        }
        """,
    sort_field_index=3  # Sort by Rank field
)

def create_new_deck(batch_num):
    return genanki.Deck(
        2059400110 + batch_num,
        f'Top 1000 Finnish Words::Batch {batch_num} (Words {(batch_num-1)*BATCH_SIZE + 1}-{batch_num*BATCH_SIZE})'
    )

def main():
    # Load JSON database
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            database = json.load(f)
        print(f"Loaded {len(database)} words from JSON database")
    except FileNotFoundError:
        print(f"Database not found: {INPUT_FILE}")
        print("Please run the merge script first to create the database!")
        return
    except json.JSONDecodeError as e:
        print(f"Error reading JSON database: {e}")
        return
    
    # Sort words by frequency_count (descending) to get most frequent first
    sorted_words = sorted(
        database.items(), 
        key=lambda x: x[1]['frequency_count'], 
        reverse=True
    )
    
    current_batch = 1
    current_deck = None
    card_count = 0
    all_decks = []
    
    # Create first deck
    current_deck = create_new_deck(current_batch)
    
    # Process each word in order of frequency
    for rank, (finnish_word, word_data) in enumerate(sorted_words, 1):
        english_translation = word_data.get('english_translation', '')
        examples = word_data.get('examples', '')
        frequency_count = word_data.get('frequency_count', 0)
        
        # Skip words without translation
        if not english_translation.strip():
            print(f"Skipping word without translation: {finnish_word}")
            continue
        
        # Check if we need to start a new batch
        if card_count >= BATCH_SIZE:
            all_decks.append(current_deck)
            print(f"\nCompleted Batch {current_batch} with {card_count} cards")
            
            current_batch += 1
            current_deck = create_new_deck(current_batch)
            card_count = 0
            print(f"\nStarting Batch {current_batch}...")
        
        # Create note with examples
        note = genanki.Note(
            model=model, 
            fields=[finnish_word, english_translation, examples, str(rank)],
            guid=generate_note_id(finnish_word)
        )
        current_deck.add_note(note)
        card_count += 1
        print(f"Added to Batch {current_batch}: #{rank}: {finnish_word} -> {english_translation} (freq: {frequency_count})")
    
    # Add the last deck if it has cards
    if card_count > 0:
        all_decks.append(current_deck)
        print(f"\nCompleted Batch {current_batch} with {card_count} cards")
    
    # Export all batches to a single .apkg file
    package = genanki.Package(all_decks)
    package.write_to_file(OUTPUT_FILE)
    
    print(f"\nCreated enhanced master deck: {OUTPUT_FILE}")
    print(f"Contains {len(all_decks)} sub-decks from JSON database!")
    
    for i, deck in enumerate(all_decks, 1):
        start_word = (i-1) * BATCH_SIZE + 1
        end_word = min(i * BATCH_SIZE, start_word + len(deck.notes) - 1)
        print(f"  Top Finnish Words::Batch {i} (Ranks {start_word}-{end_word}) - {len(deck.notes)} cards")

if __name__ == "__main__":
    main()