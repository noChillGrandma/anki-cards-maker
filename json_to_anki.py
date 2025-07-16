#!/usr/bin/env python3
"""
Script to convert JSON file with Finnish-English sentence pairs to Anki deck.
JSON format: {"finnish_sentence": "english_translation"}
"""

import json
import genanki
import sys
import os
from pathlib import Path

# Define the note model for Finnish-English cards
FINNISH_ENGLISH_MODEL = genanki.Model(
    1607392319,  # Model ID
    'Finnish-English Sentences Styled',
    fields=[
        {'name': 'Finnish'},   # Finnish text field
        {'name': 'English'},   # English text field
    ],
    templates=[
        {
            'name': 'Finnish → English',
            'qfmt': '<div class="card front">🇫🇮 {{Finnish}}</div>',
            'afmt': '''{{FrontSide}}
                        <hr>
                        <div class="card back">
                        <div class="translation">🇬🇧 {{English}}</div>
                        </div>''',
        },
        {
            'name': 'English → Finnish',
            'qfmt': '<div class="card front">🇬🇧 {{English}}</div>',
            'afmt': '''{{FrontSide}}
                        <hr>
                        <div class="card back">
                        <div class="translation">🇫🇮 {{Finnish}}</div>
                        </div>''',
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
        hr {
            margin: 20px 0;
            border: none;
            border-top: 1px solid #333;
        }
        """,
    sort_field_index=0
)

def load_json_data(file_path):
    """Load sentence pairs from JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in '{file_path}': {e}")
        sys.exit(1)

def create_anki_deck(data, deck_name="Finnish-English Sentences"):
    """Create Anki deck from sentence pairs."""
    deck = genanki.Deck(2059400110, deck_name)  # Deck ID
    
    for finnish, english in data.items():
        note = genanki.Note(
            model=FINNISH_ENGLISH_MODEL,
            fields=[finnish, english]
        )
        deck.add_note(note)
    
    return deck

def main():
    if len(sys.argv) != 2:
        print("Usage: python json_to_anki.py <input_json_file>")
        print("Example: python json_to_anki.py sentences.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)
    
    # Load data from JSON file
    print(f"Loading data from '{input_file}'...")
    data = load_json_data(input_file)
    
    if not data:
        print("Error: No data found in the JSON file.")
        sys.exit(1)
    
    print(f"Found {len(data)} sentence pairs.")
    
    # Create deck name from input filename
    deck_name = Path(input_file).stem.replace('_', ' ').replace('-', ' ').title()
    
    # Create Anki deck
    print(f"Creating Anki deck '{deck_name}'...")
    deck = create_anki_deck(data, deck_name)
    
    # Generate output filename
    output_file = f"{Path(input_file).stem}.apkg"
    
    # Create Anki package
    print(f"Generating Anki package '{output_file}'...")
    genanki.Package(deck).write_to_file(output_file)
    
    print(f"Successfully created Anki deck: {output_file}")
    print("Import this file into Anki to use the deck.")

if __name__ == "__main__":
    main()