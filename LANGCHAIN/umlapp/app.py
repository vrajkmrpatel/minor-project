import streamlit as st
from langchain_openai import ChatOpenAI  # OpenAI integration
from langchain_core.prompts import PromptTemplate  # Core prompt handling
from langchain.chains import LLMChain

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

# Set the API key in LangChain/OpenAI
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
os.environ["LANGCHAIN_TRACING_V2"] = "true"


# Streamlit UI
st.title("AI-Powered Use Case Generator 📝")
st.write("Enter a problem statement, choose a prompting technique, and generate a use case!")

problem_statement = st.text_area("Problem Statement", "")
technique = st.radio("Select Prompting Technique", [
                     "Few-Shot Prompting", "Chain-of-Thought (CoT) Prompting"])

# Model and temperature selection
model = st.radio("Select Model", ["gpt-3.5-turbo", "gpt-4"])
temperature = st.slider("Set Temperature", min_value=0.0,
                        max_value=1.0, value=0.7, step=0.1)


# Function to generate use case
def generate_use_case(problem_statement, technique):
    if technique == "Few-Shot Prompting":
        prompt = PromptTemplate(
            input_variables=["problem_statement"],
            template="""
      Assume you are a software engineer developing requirements for a system.
      Generate a structured use case based on the problem statement.

      ### Example Use Case ###
      Use Case: Order Ticket
      Primary Actor: Clerk
      Secondary Actors: Airline System, Payment Gateway
      Preconditions: The Clerk must be logged into the system.
      Steps:
      1. Clerk enters passenger details.
      2. Clerk selects the desired flight.
      3. Clerk proceeds to booking.
      4. System confirms ticket and generates PNR.

      Exceptions:
      - If the payment fails, prompt the user to retry.
      - If the flight is full, suggest alternative flights.

      Now generate three use cases for the following problem statement:
      {problem_statement}
                  """
        )
    else:  # Chain-of-Thought Prompting
        prompt = PromptTemplate(
            input_variables=["problem_statement"],
            template="""
      Assume you are a software engineer developing a system.
      To ensure correctness, follow these steps:

      1️. **Identify all the goals** of the system.  
      Think carefully about what the system is trying to achieve and list all the goals.
      
      2️. For each goal, determine the **primary actor** (who initiates the action).  
      Think about who will trigger the action for each goal. It could be a customer, an admin, or a system.

      3️. Identify any **secondary actors** involved.  
      These are entities that play a supporting role, such as systems or external services.

      4️. Describe the **interaction steps** between actors and the system.  
      Detail the sequence of actions that take place to fulfill the goal.

      5️. Mention **exceptions** and alternative flows.  
      Consider possible exceptions or edge cases where the flow might differ from the norm.

      ### Example Use Case ###
      Use Case: Order Ticket
      Primary Actor: Clerk
      Secondary Actors: Airline System, Payment Gateway
      Preconditions: The Clerk must be logged into the system.

      Steps:
      1. Clerk enters passenger details.
      2. Clerk selects the desired flight.
      3. Airline System checks availability.
      4. Clerk proceeds to booking.
      5. System confirms booking and moves to payment.
      6. Clerk enters payment details.
      7. Payment Gateway processes payment.
      8. Airline System confirms payment.
      9. System generates PNR.
      10. Confirmation message is sent to the Clerk or Customer.

      Exceptions:
      1. If payment fails, prompt the Clerk to retry.
      2. If the flight is full, suggest alternative flights.
      3. If the PNR cannot be generated, notify the Clerk of the issue.

      Now, apply the same reasoning step-by-step to generate three use cases for:
      {problem_statement}
      """
        )

    # Initialize the LLM with selected model and temperature
    llm = ChatOpenAI(model_name=model, temperature=temperature)
    response = llm(prompt.format(problem_statement=problem_statement))
    return response


# Function to generate PlantUML script
def generate_plantuml_script(use_case_output):
    plantuml_prompt = PromptTemplate(
        input_variables=["use_case_output"],
        template="""Convert the textual use case into a valid **PlantUML script**:
        
        Now generate a **PlantUML script** for the following textual use case:
        {use_case_output}
        """
    )
    llm = ChatOpenAI(model_name=model, temperature=temperature)
    plantuml_response = llm(
        plantuml_prompt.format(use_case_output=use_case_output))

    return str(plantuml_response)  # Ensure we return a string


import subprocess  # Ensure this is imported
# Function to generate Use Case Diagram
def generate_uml_diagram(plantuml_script, output_file="use_case_diagram.png"):
    plantuml_script_str = str(plantuml_script)  # Ensure it's a string

    with open("use_case_diagram.txt", "w") as file:
        file.write(plantuml_script_str)  # Write as string

    subprocess.run(
        ["java", "-jar", "plantuml-1.2025.0.jar", "use_case_diagram.txt"])

    if os.path.exists("use_case_diagram.png"):
        os.rename("use_case_diagram.png", output_file)
        return output_file
    else:
        raise FileNotFoundError(
            "PlantUML did not generate 'use_case_diagram.png'. Check for errors.")


if st.button("Generate Use Case & Diagram"):
    if problem_statement.strip() == "":
        st.warning("Please enter a problem statement.")
    else:
        with st.spinner("Generating use case..."):
            use_case_output = generate_use_case(problem_statement, technique)
            st.subheader("Generated Use Case")
            st.write(use_case_output)

            with st.spinner("Generating PlantUML script..."):
                plantuml_script = generate_plantuml_script(use_case_output)
                st.subheader("Generated PlantUML Script")
                st.code(plantuml_script, language="plantuml")

                with st.spinner("Generating Use Case Diagram..."):
                    diagram_path = generate_uml_diagram(plantuml_script)
                    st.image(diagram_path, caption="Generated Use Case Diagram")
