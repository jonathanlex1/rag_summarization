from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, YoutubeLoader, UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain

from dotenv import load_dotenv
import os 
import streamlit as st

load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY', st.secrets['GROQ_API_KEY'])

#LLM 
llm = ChatGroq(api_key=GROQ_API_KEY, model='gemma2-9b-it',temperature=0)


#document 
path = 'https://edition.cnn.com/2025/06/16/middleeast/israel-iran-tamra-shelters-latam-hnk-intl'

def stuff_document_summarization(path): 
    if path :   
        if path.endswith('.pdf') : 
            loader = PyPDFLoader(path)
        else : 
            loader = UnstructuredURLLoader(
                urls=[path],
                ssl_verify=False, 
                headers={}  
            )
        docs = loader.load()
        prompt_template = """
        Summarize the following document in a clear, concise, and informative way:

        Document:
        {text}
        
        Summary:
        """
        prompt = PromptTemplate(
            input_variables=['text'],
            template=prompt_template
            )
        
        chain = load_summarize_chain(
            llm=llm,
            chain_type='stuff',
            prompt=prompt,
            verbose=True
        )
        
        return chain.run(docs)
    
    raise FileNotFoundError('there is no path to execute')

def map_reduce_summarization(path) : 
    if path : 
        if path.endswith('.pdf') : 
            loader = PyPDFLoader(path)
        else : 
            loader = UnstructuredURLLoader(
                urls=[path],
                ssl_verify=False, 
                headers={}
            )
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

        splitted_docs = splitter.split_documents(docs)

        map_prompt_template = """
        Summarize each following document in a clear, concise, and informative way:

        Document:
        {text}
        
        Summary:
        """

        map_prompt = PromptTemplate(
            input_variables=['text'],
            template=map_prompt_template
            )
        
        reduce_prompt_template = """
        Provide me the final summary of all the documents in a clear, concise, and informative way:

        Document:
        {text}
        
        Summary:
        """

        reduce_prompt = PromptTemplate(
            input_variables=['text'],
            template=reduce_prompt_template
            )


        chain = load_summarize_chain(
            llm=llm,
            chain_type='map_reduce',
            map_prompt = map_prompt,
            combine_prompt = reduce_prompt,
            verbose=True
        )
        
        return chain.run(splitted_docs)
    
    raise FileNotFoundError('there is no path to execute')


if __name__ == '__main__' : 
    print(stuff_document_summarization(path))




