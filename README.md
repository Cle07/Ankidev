# Ankidev

A personal collection of Python scripts for generating Anki decks from various sources using LLMs and structured data.

## Scripts

- **article_to_csv.py** - Converts articles into flashcard CSV files using Claude 3.5 Sonnet via OpenRouter
- **csv_to_anki.py** - Creates Anki decks from CSV files, with support for single decks or master decks with subdecks
- **poem_to_anki.py** - Generates progressive memorization cards for poems, helping with line-by-line memorization

## Dependencies

- [ell](docs.ell.so) - LLM interaction framework
- openai - OpenRouter API client
- pandas - CSV file handling
- [genanki](https://github.com/kerrickstaley/genanki) - Anki deck generation
