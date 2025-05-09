import os
import bs4
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Securely input the OpenAI API key
os.environ["OPENAI_API_KEY"]

# Initialize the language model
llm = ChatOpenAI(model="gpt-4o-mini")

# Load content from the web page
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)
docs = loader.load()

# Split the content into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# Create a vector store using OpenAI embeddings
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

# Set up the retriever to fetch relevant documents
retriever = vectorstore.as_retriever()

# Define a custom prompt without LangSmith
def custom_prompt(context, question):
    return f"""
You are an AI assistant. Given the context below, please answer the question.

Context:
{context}

Question:
{question}

Answer:
"""

# Formatting function to join the retrieved documents
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Main function to retrieve and generate an answer
def retrieve_and_generate(question):
    # Retrieve relevant context based on the question
    relevant_docs = retriever.get_relevant_documents(question)
    context = format_docs(relevant_docs)
    
    # Format the question with the context
    prompt = custom_prompt(context, question)
    
    # Generate an answer using the language model
    response = llm.generate(prompt)
    
    # Extract and return the response
    return response.generations[0].text.strip()

# Example usage
answer = retrieve_and_generate("What is Task Decomposition?")
print(answer)
