import spacy
from spacy.matcher import Matcher

# Load the English language model
nlp = spacy.load("en_core_web_sm")

# Define intents and their corresponding actions
intents = {
    "create_function": "function {function_name}() {{\n  // Code goes here\n}}0000000000",
    "declare_variable": "var {variable_name};",
    "loop_over_array": "for (var i = 0; i < {array_name}.length; i++) {\n  // Code goes here\n}",
    # Add more intents and actions as needed
}

# Process the user's instruction and return the code snippet
def process_instruction(instruction):
    doc = nlp(instruction)
    matcher = Matcher(nlp.vocab)

    # Define patterns for the matcher
    pattern_create_function = [{"LOWER": "create"}, {"LOWER": "a"}, {"LOWER": "function"}, {"POS": "PROPN"}]
    matcher.add("CreateFunction", [pattern_create_function])

    matches = matcher(doc)

    for match_id, start, end in matches:
        # Identify the intent and extract any relevant entities
        intent = nlp.vocab.strings[match_id]
        entities = doc[start:end].text

        # Generate the code snippet based on the intent and entities
        if intent in intents:
            code_snippet = intents[intent].format(**entities)
            return code_snippet

    return None

# Take user input and process the instruction
instruction = input("Enter an instruction: ")
response = process_instruction(instruction)

if response:
    print("Generated code snippet:")
    print(response)
else:
    print("No matching code snippet found.")
