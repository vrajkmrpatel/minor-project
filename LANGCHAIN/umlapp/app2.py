import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve API keys
openai_api_key = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

# Set API keys in environment
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# Streamlit UI
st.title("AI-Powered Use Case Generator 📝")
st.write("Enter a problem statement, choose a prompting technique, and generate a use case!")

problem_statement = st.text_area("Problem Statement", "")
technique = st.radio("Select Prompting Technique", ["Few-Shot Prompting", "Chain-of-Thought (CoT) Prompting"])
model = st.radio("Select Model", ["gpt-3.5-turbo", "gpt-4"])
temperature = st.slider("Set Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

# Function to generate use case
def generate_use_case(problem_statement, technique):
    if technique == "Few-Shot Prompting":
        prompt = PromptTemplate(
            input_variables=["problem_statement"],
            template="""
            Generate a structured use case based on the problem statement.
            {problem_statement}
            """
        )
    else:
        prompt = PromptTemplate(
            input_variables=["problem_statement"],
            template="""
            Follow structured steps to generate a detailed use case.
            {problem_statement}
            """
        )
    llm = ChatOpenAI(model_name=model, temperature=temperature)
    response = llm(prompt.format(problem_statement=problem_statement))
    return response

# Function to generate PlantUML script
def generate_plantuml_script(use_case_output):
    plantuml_prompt = PromptTemplate(
        input_variables=["use_case_output"],
        template="""
        Convert the textual use case into a PlantUML script:
        {use_case_output}
        """
    )
    llm = ChatOpenAI(model_name=model, temperature=temperature)
    plantuml_response = llm(plantuml_prompt.format(use_case_output=use_case_output))
    return str(plantuml_response)

# Function to generate Use Case Diagram
def generate_uml_diagram():
    plantuml_jar = "plantuml-1.2025.0.jar"
    plantuml_input_file = "use_case_diagram.txt"
    output_file = "use_case_diagram.png"
    
    if os.path.exists(plantuml_input_file):
        subprocess.run(["java", "-jar", plantuml_jar, plantuml_input_file])
        
        if os.path.exists(output_file):
            return output_file
        else:
            raise FileNotFoundError("PlantUML did not generate 'use_case_diagram.png'. Check for errors.")
    else:
        raise FileNotFoundError("Input file 'use_case_diagram.txt' not found.")

# Streamlit button action
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
                
                with open("use_case_diagram.txt", "w") as file:
                    file.write(plantuml_script)
                
                with st.spinner("Generating Use Case Diagram..."):
                    diagram_path = generate_uml_diagram()
                    st.image(diagram_path, caption="Generated Use Case Diagram")
