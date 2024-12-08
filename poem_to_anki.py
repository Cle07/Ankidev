import genanki

def create_recto_verso(poem):
    recto = []
    verso = []
    recto.append(f'[START]\n{"...\n" * len(poem)}')
    verso.append(poem)
    for i in range(len(poem)):
        if i == 0:
            recto.append("[START]")
            verso.append(poem[i])
        elif i == 1:
            recto.append(f"[START]\n{poem[0]}")
            verso.append(poem[1])
        else:
            recto.append(poem[i-2:i])
            verso.append(poem[i])
    return (recto,verso)

def generate_deck(recto_verso, title):
    recto = recto_verso[0]
    verso = recto_verso[1]
    my_deck = genanki.Deck(
        2059400110,
        title
    )

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

    for i in range(len(recto)):
        my_deck.add_note(
            genanki.Note(
                model=my_model,
                fields=[str(recto[i]), str(verso[i])]
            )
        )

    genanki.Package(my_deck).write_to_file(f'{title}.apkg')

if __name__ == "__main__":
    title = input("Enter the title of the deck: ")
    print("Enter a poem (press Ctrl+D on Unix/Linux or Ctrl+Z on Windows when done):")
    poem_lines = []
    try:
        while True:
            line = input()
            poem_lines.append(line)
    except EOFError:
        poem = "\n".join(poem_lines)
        poem = poem.split("\n")

    recto_verso = create_recto_verso(poem)
    generate_deck(recto_verso, title)
