from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)

few_shot_examples = """
Example 1:
Problem: A user wants to book a flight online.
Goals: Book a flight, receive confirmation.
Primary Actor: User.
Secondary Actors: Airline System, Payment Gateway.
Interactions: 
1. User selects flight.
2. User enters details.
3. Payment gateway processes payment.
4. Airline system confirms booking.

Example 2:
Problem: An online food delivery system.
Goals: Order food, track delivery.
Primary Actor: Customer.
Secondary Actors: Restaurant, Delivery Agent, Payment Gateway.
Interactions:
1. Customer selects food.
2. Customer makes payment.
3. Restaurant prepares food.
4. Delivery agent delivers food.
"""

prompt_template = PromptTemplate(
    input_variables=["problem_statement"],
    template="""
Analyze the problem statement and extract the following:
- Goals
- Primary and Secondary Actors
- Interactions between actors

Use the provided examples as reference.

Problem Statement: {problem_statement}
---
Few-shot Examples:
{few_shot_examples}
"""
)

chain = LLMChain(llm=llm, prompt=prompt_template)

def extract_info(problem_statement):
    response = chain.run({"problem_statement": problem_statement, "few_shot_examples": few_shot_examples})
    return response
