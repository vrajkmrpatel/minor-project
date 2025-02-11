from extract_info import extract_info
from generate_diagram import generate_use_case_diagram
from use_case_description import generate_use_case_descriptions

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ensure the key is loaded
if OPENAI_API_KEY is None:
    raise ValueError("OpenAI API Key not found. Please set it in the .env file.")

print("OpenAI API Key loaded successfully!")

def process_problem_statement(problem_statement):
    # Extract goals, actors, and interactions
    response = extract_info(problem_statement)
    print("Extracted Data:\n", response)

    # Convert response to structured format (Modify as needed)
    actors = {
        "primary": ["User"],
        "secondary": ["Doctor", "Appointment System", "Payment Gateway"]
    }
    interactions = [
        {"actor": "User", "use_case": "Book Appointment", "description": "User selects doctor and time slot"},
        {"actor": "Appointment System", "use_case": "Confirm Appointment", "description": "System confirms booking"},
        {"actor": "Payment Gateway", "use_case": "Process Payment", "description": "User completes payment"},
        {"actor": "Doctor", "use_case": "Provide Consultation", "description": "Doctor consults patient"}
    ]

    # Generate and display use case diagram
    diagram = generate_use_case_diagram(actors, interactions)
    diagram.render("use_case_diagram", format="png", cleanup=False)
    
    # Generate descriptions
    use_case_descriptions = generate_use_case_descriptions(
        ["Book Appointment", "Confirm Appointment", "Process Payment", "Provide Consultation"]
    )

    return {
        "actors": actors,
        "interactions": interactions,
        "diagram": diagram,
        "descriptions": use_case_descriptions
    }

if __name__ == "__main__":
    problem_statement = "A user wants to schedule an online doctor appointment."
    result = process_problem_statement(problem_statement)
