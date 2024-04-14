import streamlit as st
import os
from azure.identity import DefaultAzureCredential
from azure.identity import ChainedTokenCredential, ManagedIdentityCredential, AzureCliCredential
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.chains import SequentialChain
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE
from langchain.chains.router.llm_router import LLMRouterChain,RouterOutputParser
from langchain.chains.router import MultiPromptChain
from langchain.chains import TransformChain

# Create an instance of the AzureChatOpenAI model
model = AzureChatOpenAI(
    deployment_name="exq-gpt-35",
    azure_endpoint="https://exquitech-openai-2.openai.azure.com/",
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    temperature=0,
    openai_api_version="2024-02-15-preview"
)

# Define function to generate a funny company name using LLMChain
def generate_company_name(product):
    human_prompt = HumanMessagePromptTemplate.from_template('Make up a funny company name for a company that makes: {product}')
    chat_prompt_template = ChatPromptTemplate.from_messages([human_prompt])
    chain = LLMChain(llm=model, prompt=chat_prompt_template)
    response = chain.run(product=product)
    return response

# Define function for SimpleSequentialChain: Responds with a random joke
def get_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
    ]
    return jokes

# Define function for LLMRouterChain: Responds differently based on input type
def route_response(user_input):
    if "?" in user_input:
        return "That's an interesting question! Let me think about it..."
    else:
        return "Thanks for sharing your thoughts!"

# Define function for TransformChain: Translates input text to uppercase
def transform_text(input_text):
    return input_text.upper()

# Define function for OpenAIChain: Sends user input to Azure Chat OpenAI model and retrieves response
def send_to_azure_chat(input_text):
    response = model.send_message(input_text)
    return response['message']

# Define function for MathChain: Evaluates mathematical expressions
def evaluate_expression(expression):
    try:
        result = eval(expression)
        return f"The result of {expression} is {result}"
    except:
        return "Invalid expression! Please enter a valid mathematical expression."

# Define main function to render Streamlit app
def main():
    st.title("LangChain Showcase")
    st.sidebar.title("Chains")
    selected_chain = st.sidebar.selectbox("Select a chain", ["LLMChain", "SimpleSequentialChain", "LLMRouterChain", "TransformChain", "OpenAIChain", "MathChain"])

    if selected_chain == "LLMChain":
        st.subheader("LLMChain")
        st.write("Functionality: Generates a funny company name based on a given product.")
        product = st.text_input("Enter a product", "Computers")
        generate_button = st.button("Generate")

        if generate_button:
            company_name = generate_company_name(product)
            st.success(f"Here's a funny company name for a {product} company: {company_name}")

    elif selected_chain == "SimpleSequentialChain":
        st.subheader("SimpleSequentialChain")
        st.write("Functionality: Responds with a random joke.")
        joke_button = st.button("Tell me a joke")

        if joke_button:
            joke = get_joke()
            st.success(joke)

    elif selected_chain == "LLMRouterChain":
        st.subheader("LLMRouterChain")
        st.write("Functionality: Responds differently based on input type.")
        user_input = st.text_input("Enter your input")
        route_button = st.button("Route Response")

        if route_button:
            response = route_response(user_input)
            st.success(response)

    elif selected_chain == "TransformChain":
        st.subheader("TransformChain")
        st.write("Functionality: Translates input text to uppercase.")
        input_text = st.text_input("Enter text")
        transform_button = st.button("Transform")

        if transform_button:
            transformed_text = transform_text(input_text)
            st.success(transformed_text)

    elif selected_chain == "OpenAIChain":
        st.subheader("OpenAIChain")
        st.write("Functionality: Interacts with Azure Chat OpenAI model.")
        input_text = st.text_input("You:")
        send_button = st.button("Send")

        if send_button:
            response = send_to_azure_chat(input_text)
            st.text_area("Bot:", response, height=200)

    elif selected_chain == "MathChain":
        st.subheader("MathChain")
        st.write("Functionality: Evaluates mathematical expressions.")
        expression = st.text_input("Enter a mathematical expression")
        evaluate_button = st.button("Evaluate")

        if evaluate_button:
            result = evaluate_expression(expression)
            st.success(result)

if __name__ == "__main__":
    main()
