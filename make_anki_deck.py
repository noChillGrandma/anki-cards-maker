# pip install genanki
import genanki
import csv
import hashlib

INPUT_FILE = 'finnish_english_translations_google.csv'   # your translated CSV file
BATCH_SIZE = 200  # Number of words per batch
OUTPUT_FILE = 'finnish_words_master.apkg'  # Single output file with all batches

def generate_note_id(finnish_word):
    """Generate a stable note ID based on the Finnish word"""
    # Create a hash of the Finnish word to ensure consistent note IDs
    # This means the same word will always have the same ID, preserving progress
    hash_object = hashlib.md5(finnish_word.encode('utf-8'))
    # Convert to integer and ensure it's positive and within Anki's range
    return int(hash_object.hexdigest()[:8], 16)

# 1. Define a two-field note model for Finnish-English cards
import genanki

# Define minimalist Finnish-English Anki model
model = genanki.Model(
    1607392319,
    'Finnish-English Model',
    fields=[
        {'name': 'Finnish'},
        {'name': 'English'},
        {'name': 'Rank'}
    ],
    templates=[
        {
            'name': 'Finnish → English',
            'qfmt': '<div class="card front">🇫🇮 {{Finnish}}</div>',          # Front: show Finnish
            'afmt': '{{FrontSide}}<hr><div class="card back">🇬🇧 {{English}}</div>'  # Back: show English
        },
    ],
    css="""
        .card {
        background: #00000;                       /* dark background */
        color: #fff;                            /* white text */
        font-family: 'Helvetica Neue', sans-serif;
        text-align: center;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .front {
        font-size: 32px;
        font-weight: 600;
        }
        .back {
        font-size: 24px;
        font-weight: 400;
        }
        hr {
        margin: 20px 0;
        border: none;
        border-top: 1px solid #eee;
        }
        """
)


# 2. Read CSV file and create batched decks
current_batch = 1
current_deck = None
card_count = 0
all_decks = []

def create_new_deck(batch_num):
    return genanki.Deck(
        2059400110 + batch_num,  # Unique deck ID for each batch
        f'Finnish Words::Batch {batch_num} (Words {(batch_num-1)*BATCH_SIZE + 1}-{batch_num*BATCH_SIZE})'
    )

with open(INPUT_FILE, 'r', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    
    # Skip header row
    next(csv_reader, None)
    
    # Create first deck
    current_deck = create_new_deck(current_batch)
    
    for row in csv_reader:
        if len(row) >= 3:  # Ensure we have Number, Finnish, English columns
            number = row[0]
            finnish_word = row[1]
            english_translation = row[2]
            
            # Skip failed translations
            if english_translation.startswith('[') and english_translation.endswith(']'):
                print(f"Skipping failed translation: {finnish_word}")
                continue
            
            # Check if we need to start a new batch
            if card_count >= BATCH_SIZE:
                # Save current deck
                all_decks.append(current_deck)
                print(f"\nCompleted Batch {current_batch} with {card_count} cards")
                
                # Start new batch
                current_batch += 1
                current_deck = create_new_deck(current_batch)
                card_count = 0
                print(f"\nStarting Batch {current_batch}...")
            
            note = genanki.Note(
                model=model, 
                fields=[finnish_word, english_translation, number],
                guid=generate_note_id(finnish_word)  # Stable ID based on Finnish word
            )
            current_deck.add_note(note)
            card_count += 1
            print(f"Added to Batch {current_batch}: {number}: {finnish_word} -> {english_translation}")
    
    # Add the last deck if it has cards
    if card_count > 0:
        all_decks.append(current_deck)
        print(f"\nCompleted Batch {current_batch} with {card_count} cards")

# 3. Export all batches to a single .apkg file
package = genanki.Package(all_decks)
package.write_to_file(OUTPUT_FILE)

print(f"\nCreated master deck: {OUTPUT_FILE}")
print(f"Contains {len(all_decks)} sub-decks with {BATCH_SIZE} words each (except possibly the last batch)")
print("\nIn Anki, you'll see:")
for i, deck in enumerate(all_decks, 1):
    start_word = (i-1) * BATCH_SIZE + 1
    end_word = min(i * BATCH_SIZE, start_word + len(deck.notes) - 1)
    print(f"  Finnish Words::Batch {i} (Words {start_word}-{end_word}) - {len(deck.notes)} cards")
