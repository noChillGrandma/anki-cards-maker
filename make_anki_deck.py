# pip install genanki
import genanki
import re

INPUT_FILE = 'top_finnish_words.txt'   # your ranked list
OUTPUT_FILE = 'finnish_words.apkg'     # resulting Anki deck

# 1. Define a simple one-field note model
model = genanki.Model(
    1607392319,
    'Finnish Word Model',
    fields=[{'name': 'Word'}],
    templates=[{
        'name': 'Card 1',
        'qfmt': '{{Word}}',           # front: the Finnish word
        'afmt': '{{FrontSide}}'       # back: same as front (you can customize)
    }]
)

# 2. Create a deck to hold your notes
deck = genanki.Deck(
    2059400110,
    'Top Finnish Words'
)

# 3. Read your file, parse rank lines, and add each word as a note
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        m = re.match(r'\s*\d+:\s*(?:\[.*?\]\s*)?(.*)', line)
        if m:
            word = m.group(1).strip()
            note = genanki.Note(model=model, fields=[word])
            deck.add_note(note)

# 4. Export to .apkg
genanki.Package(deck).write_to_file(OUTPUT_FILE)
