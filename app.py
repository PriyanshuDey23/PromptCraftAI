from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import os
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
import fitz
from prompt import *
from utils import *

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Function to generate README using LLM
def generate_human_text(user_input):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b", temperature=1, api_key=GOOGLE_API_KEY)
    PROMPT_TEMPLATE =PROMPT
    prompt = PromptTemplate(
        input_variables=["user_input"], # From prompt
        template=PROMPT_TEMPLATE,
    )
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    response=llm_chain.run({"user_input":user_input})
    return response


# Streamlit App Configuration
st.set_page_config(page_title="Prompt Gen AI", layout="wide")
st.header("Prompt Gen AI")

#  text input
user_input = st.text_area("Enter your text", height=200)


# Generate Plagarism check
if st.button("Generate Prompt"):
    response=generate_human_text(user_input=user_input)
    st.subheader("Generated Prompt:")
    st.write(response)
    # Download options
    st.download_button(
            label="Download as TXT",
            data=convert_to_txt(response),
            file_name="prompt.txt",
            mime="text/plain",
        )
    st.download_button(
            label="Download as DOCX",
            data=convert_to_docx(response),
            file_name="prompt.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )    
    