from time import sleep, perf_counter
import openai
import json
import ell
import os

# setting up ell client
client = openai.Client(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://github.com/yourusername/yourrepo",
        "X-Title": "Your Application Name"
    }
)

@ell.simple(model="anthropic/claude-3.5-sonnet", temperature=0.6, client=client)
def flashcreator(title, content):
    system = """You are an advanced language model designed to create high-quality flashcards from provided articles. Your task is to analyze the given article, identify all important information, and generate a set of flashcards that effectively cover key aspects such as important statistics, legal frameworks, legal evolutions, key definitions, insightful concepts, or phenomena. Each flashcard should be structured with a "Recto" containing a question, word to define, or legislation to remember, and a "Verso" with a very concise explanation, number, definition, etc. Ensure that the flashcards adhere to best practices, being atomic, concise, and useful. Generate between 25 and 30 flashcards per article, depending on the content's importance.
    These flashcards will be used to help students for civil servant exams, so ensure that the information is accurate, relevant, and well-structured. Remember to focus on the most critical aspects
    **Instructions:**

    1. **Analyze the Article:**
       - Carefully read the article's content to understand its main themes and key points.
       - Identify important statistics, legal frameworks, legal evolutions, key definitions, insightful concepts, and phenomena.

    2. **Create Flashcards:**
       - For each key point, formulate a clear and concise question or term for the "Recto."
       - Provide a precise and informative answer or definition for the "Verso."
       - Ensure each flashcard is atomic, focusing on a single piece of information.
       - Maintain a lot of conciseness and clarity to enhance the flashcards' effectiveness.

    3. **Output Format:**
       - Present the flashcards in a valid CSV format with the following structure:

         Recto;Verso
         {First question};{First answer}
         {Second question};{Second answer}
         ...

       - Do not include any additional characters, remarks, or code blocks.

    4. **Example:**
Recto;Verso
What is the definition of [Term]?;[Concise Definition]
What year was [Event] established?;[Year]

5. **Final Output:**
- Ensure the final output strictly follows the CSV syntax as described.
- Do not include explanations, comments, or additional text outside the CSV structure.
- Always include between 25 and 30 flashcards per article.

**Remember:** Always perform reasoning and analysis of the article's content before generating the flashcards. The conclusions (flashcards) should appear only after thorough reasoning.

**Input Structure:**
- The input will consist of an article with a "name" and "content."

**Output Requirement:**
- A CSV-formatted list of flashcards covering all important information from the article, adhering to the specified structure and guidelines.
"""
    return [ell.system(system),
            ell.user(f"Title of the article: {title}\n\n{content}")]

with open("essentiels.json", "r") as f:
    data = json.load(f)

# Iterate through all keys in data
for key in data:
    # Create file name from key (replacing invalid characters)
    file_name = "".join(c for c in key if c.isalnum() or c in (' ','-','_')).rstrip()
    file_name = f"{file_name}.csv"
    sleep(0.5)
    # Generate flashcards using flashcreator function
    tstart = perf_counter()
    flashcards = flashcreator(key, data[key])
    tend = perf_counter() - tstart
    if len(flashcards) < 100:
        print(f"Retrying {key}...cuz {len(flashcards)} < 100")
        sleep(0.4)
        tstart = perf_counter()
        flashcards = flashcreator(key, data[key])
        tend = perf_counter() - tstart
    # Write flashcards to CSV file
    with open(f"sonnet/{file_name}", 'w', encoding='utf-8') as f:
        f.write(flashcards)
    print(f"Flashcards generated for {key}\nStatus percentage : {round((list(data.keys()).index(key) + 1) / len(data) * 100, 2)}%\n Token cost : {len(flashcards)/3.5}\n Inference time : {tend} seconds")
