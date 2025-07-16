import json
import re

def extract_sentence_pairs(examples_text):
    """
    Extract Finnish-English sentence pairs from the examples field.
    The format is: Finnish sentence\nEnglish translation\n\n (repeat)
    """
    sentence_pairs = {}
    
    # Split by double newlines to get individual examples
    examples = examples_text.strip().split('\n\n')
    
    for example in examples:
        if not example.strip():
            continue
            
        # Split each example by single newline to separate Finnish and English
        lines = example.strip().split('\n')
        
        # We expect pairs: Finnish line followed by English line
        if len(lines) >= 2:
            finnish = lines[0].strip()
            english = lines[1].strip()
            
            # Only add if both sentences are non-empty
            if finnish and english:
                sentence_pairs[finnish] = english
    
    return sentence_pairs

def extract_all_examples(input_file, output_file):
    """
    Extract all examples from the vocabulary JSON file and save as a new JSON file.
    
    Args:
        input_file (str): Path to the input vocabulary JSON file
        output_file (str): Path to the output examples JSON file
    """
    try:
        # Read the vocabulary file
        with open(input_file, 'r', encoding='utf-8') as f:
            vocabulary_data = json.load(f)
        
        all_sentences = {}
        processed_count = 0
        
        # Process each word entry
        for word, word_data in vocabulary_data.items():
            if 'examples' in word_data and word_data['examples']:
                examples = word_data['examples']
                sentences = extract_sentence_pairs(examples)
                
                # Add to the master dictionary
                all_sentences.update(sentences)
                
                if sentences:
                    processed_count += 1
                    print(f"Processed '{word}': found {len(sentences)} sentence pairs")
        
        # Save the extracted sentences
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_sentences, f, ensure_ascii=False, indent=2)
        
        print(f"\nExtraction complete!")
        print(f"Processed {processed_count} words with examples")
        print(f"Total sentence pairs extracted: {len(all_sentences)}")
        print(f"Results saved to: {output_file}")
        
    except FileNotFoundError:
        print(f"Error: Could not find input file '{input_file}'")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{input_file}'")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Default file paths - you can modify these as needed
    input_file = "new_system/data/top_words_database.json"  # Change this to your vocabulary file path
    output_file = "finnish_sentences_for_deck.json"
    
    print("Extracting Finnish sentences and English translations...")
    extract_all_examples(input_file, output_file)