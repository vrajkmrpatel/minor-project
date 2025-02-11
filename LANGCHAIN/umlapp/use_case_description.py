from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from extract_info import llm

prompt_template = PromptTemplate(
    input_variables=["use_case"],
    template="Describe the use case '{use_case}' in detail."
)

chain = LLMChain(llm=llm, prompt=prompt_template)

def generate_use_case_descriptions(use_cases):
    return {use_case: chain.run({"use_case": use_case}) for use_case in use_cases}
