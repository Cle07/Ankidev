import pandas as pd
import genanki
import os
import random

def load(file):
    """Load a CSV file and return a pandas dataframe"""
    try:
        df = pd.read_csv(file, sep=';')
        return df
    except Exception as e:
        print(f"Error loading file {file}: {e}")
        return None

def create_subdeck(dataframe, main_deck_name, subdeck_name):
    """Create an Anki subdeck from a dataframe"""
    try:
        # Create deck with random ID
        deck_id = random.randrange(1_000_000_000, 9_999_999_999)
        # Format name as "Main Deck::Sub Deck"
        full_deck_name = f"{main_deck_name}::{subdeck_name}"
        my_deck = genanki.Deck(deck_id, full_deck_name)

        # Define card model
        my_model = genanki.Model(
            1091735104,
            'Simple Model',
            fields=[
                {'name': 'Question'},
                {'name': 'Answer'}
            ],
            templates=[{
                'name': 'Card 1',
                'qfmt': '{{Question}}',
                'afmt': '{{Question}}<hr id="answer">{{Answer}}'
            }]
        )

        # Create notes from dataframe
        for index, row in dataframe.iterrows():
            note = genanki.Note(
                model=my_model,
                fields=[str(row['Recto']), str(row['Verso'])]
            )
            my_deck.add_note(note)

        return my_deck
    except Exception as e:
        print(f"Error creating subdeck {subdeck_name}: {e}")
        return None

def create_master_deck(subdecks, master_deck_name):
    """Create a master deck containing all subdecks"""
    try:
        # Ensure results directory exists
        if not os.path.exists('result'):
            os.makedirs('result')

        # Create package with all decks
        output_path = os.path.join('result', f'{master_deck_name}.apkg')
        genanki.Package(subdecks).write_to_file(output_path)
        return True
    except Exception as e:
        print(f"Error creating master deck: {e}")
        return False

if __name__ == "__main__":
    # Ask user for mode
    print("Choose mode:")
    print("1. Create single deck from CSV file")
    print("2. Create master deck from folder of CSV files")
    mode = input("Enter choice (1 or 2): ")

    # Ensure result directory exists
    if not os.path.exists('result'):
        os.makedirs('result')

    # Get the directory containing the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    if mode == "1":
        # Single deck mode
        csv_name = input("Enter the name of the CSV file (including .csv extension): ")
        deck_name = input("Enter the name for your deck: ")

        file_path = os.path.join(script_dir, csv_name)
        if os.path.exists(file_path):
            print(f"Processing {csv_name}...")
            dataframe = load(file_path)

            if dataframe is not None:
                subdeck = create_subdeck(dataframe, deck_name, "")
                if subdeck:
                    if create_master_deck([subdeck], deck_name):
                        print(f"Successfully created deck: {deck_name}")
                    else:
                        print("Failed to create deck")
                else:
                    print("Failed to create deck")
        else:
            print(f"File not found: {file_path}")

    elif mode == "2":
        # Master deck mode
        folder_name = input("Enter the name of the folder containing CSV files: ")
        master_deck_name = input("Enter the name for your master deck: ")

        # List to store all subdecks
        all_decks = []

        # Construct path to source directory
        source_dir = os.path.join(script_dir, folder_name)

        # Process each CSV file in the folder
        if os.path.exists(source_dir):
            for file in os.listdir(source_dir):
                if file.endswith('.csv'):
                    file_path = os.path.join(source_dir, file)
                    subdeck_name = os.path.splitext(file)[0]  # Get filename without extension

                    print(f"Processing {file}...")
                    dataframe = load(file_path)

                    if dataframe is not None:
                        subdeck = create_subdeck(dataframe, master_deck_name, subdeck_name)
                        if subdeck:
                            all_decks.append(subdeck)
                            print(f"Successfully created subdeck: {subdeck_name}")
                        else:
                            print(f"Failed to create subdeck: {subdeck_name}")
        else:
            print(f"Directory not found: {source_dir}")

        # Create master deck containing all subdecks
        if all_decks:
            if create_master_deck(all_decks, master_deck_name):
                print(f"Successfully created master deck '{master_deck_name}' with {len(all_decks)} subdecks")
            else:
                print("Failed to create master deck")
        else:
            print("No subdecks were created. Check your input files.")

    else:
        print("Invalid choice. Please run the script again and select 1 or 2.")
