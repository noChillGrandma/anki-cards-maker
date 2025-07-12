# pip install genanki
import genanki
import csv

INPUT_FILE = 'finnish_english_translations_google.csv'   # your translated CSV file
OUTPUT_FILE = 'finnish_english_deck.apkg'     # resulting Anki deck

# 1. Define a two-field note model for Finnish-English cards
import genanki

# Define minimalist Finnish-English Anki model
model = genanki.Model(
    1607392319,
    'Finnish-English Model',
    fields=[
        {'name': 'Finnish'},
        {'name': 'English'}
    ],
    templates=[
        {
            'name': 'Finnish → English',
            'qfmt': '<div class="card front">{{Finnish}}</div>',          # Front: show Finnish
            'afmt': '{{FrontSide}}<hr><div class="card back">{{English}}</div>'  # Back: show English
        },
    ],
    css="""
        .card {
        background: #fff;                       /* White background */
        color: #333;                            /* Dark text */
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


# 2. Create a deck to hold your notes
deck = genanki.Deck(
    2059400110,
    'Top Finnish Words'
)

# 3. Read CSV file and add each word pair as a note
with open(INPUT_FILE, 'r', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    
    # Skip header row
    next(csv_reader, None)
    
    for row in csv_reader:
        if len(row) >= 3:  # Ensure we have Number, Finnish, English columns
            number = row[0]
            finnish_word = row[1]
            english_translation = row[2]
            
            # Skip failed translations
            if english_translation.startswith('[') and english_translation.endswith(']'):
                print(f"Skipping failed translation: {finnish_word}")
                continue
            
            note = genanki.Note(
                model=model, 
                fields=[finnish_word, english_translation]
            )
            deck.add_note(note)
            print(f"Added card {number}: {finnish_word} -> {english_translation}")

# 4. Export to .apkg
genanki.Package(deck).write_to_file(OUTPUT_FILE)
