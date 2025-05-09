from langchain.agents import initialize_agent, AgentType
from langchain.tools import DuckDuckGoSearchRun
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.utilities import DuckDuckGoSearchAPIWrapper
import os
from dotenv import load_dotenv
import time
import requests
from typing import Optional

class EnhancedDuckDuckGoSearch(DuckDuckGoSearchRun):
    """Enhanced DuckDuckGo search with retry logic and better error handling"""
    def __init__(self, max_retries: int = 3, timeout: int = 30):
        super().__init__()
        self.max_retries = max_retries
        self.timeout = timeout
    
    def run(self, query: str) -> str:
        for attempt in range(self.max_retries):
            try:
                wrapper = DuckDuckGoSearchAPIWrapper(timeout=self.timeout)
                self.wrapper = wrapper
                result = super().run(query)
                return result
            except requests.exceptions.Timeout:
                if attempt == self.max_retries - 1:
                    return "Search timed out. Please try again later."
                time.sleep(1)  # Wait before retrying
            except Exception as e:
                if attempt == self.max_retries - 1:
                    return f"Search error: {str(e)}. Please try again."
                time.sleep(1)

class WebSearchAgent:
    """Main agent class for handling web searches and conversations"""
    def __init__(self, openai_api_key: str, max_retries: int = 3):
        self.openai_api_key = openai_api_key
        self.max_retries = max_retries
        self.setup_agent()
    
    def setup_agent(self):
        """Initialize the agent with all necessary components"""
        try:
            # Initialize the language model
            self.llm = ChatOpenAI(
                temperature=0,
                model_name="gpt-3.5-turbo",
                openai_api_key=self.openai_api_key
            )
            
            # Initialize the enhanced search tool
            self.search_tool = EnhancedDuckDuckGoSearch(
                max_retries=self.max_retries
            )
            
            # Initialize conversation memory
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
            
            # Initialize the agent
            self.agent = initialize_agent(
                tools=[self.search_tool],
                llm=self.llm,
                agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                memory=self.memory,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=3,
                early_stopping_method="generate"
            )
        except Exception as e:
            raise Exception(f"Error setting up agent: {str(e)}")
    
    def format_query(self, query: str) -> str:
        """Format the query to be more specific and search-friendly"""
        # Remove multiple spaces and trim
        query = " ".join(query.split()).strip()
        
        # Add time context for certain types of queries
        time_sensitive_keywords = ["current", "latest", "news", "weather", "today"]
        if any(keyword in query.lower() for keyword in time_sensitive_keywords):
            query += " " + time.strftime("%Y %B")
            
        return query
    
    def ask(self, question: str) -> str:
        """
        Ask a question to the agent with error handling and retries
        """
        try:
            # Format the query
            formatted_question = self.format_query(question)
            
            # Get response from agent
            response = self.agent.run(input=formatted_question)
            
            # If response is empty or None, return error message
            if not response:
                return "I couldn't find a good answer to your question. Please try rephrasing it."
                
            return response
            
        except Exception as e:
            error_msg = str(e)
            if "api_key" in error_msg.lower():
                return "There was an issue with the API key. Please check your configuration."
            elif "timeout" in error_msg.lower():
                return "The search took too long to respond. Please try again."
            else:
                return f"An error occurred: {error_msg}. Please try rephrasing your question."

def load_api_key() -> Optional[str]:
    """Load API key from environment with error handling"""
    try:
        load_dotenv()
        api_key = os.getenv("WEBSEARCH_API_KEY")
        if not api_key:
            raise ValueError("WEBSEARCH_API_KEY not found in environment variables")
        return api_key
    except Exception as e:
        print(f"Error loading API key: {str(e)}")
        return None

def main():
    """Main function to run the agent"""
    # Load API key
    api_key = load_api_key()
    if not api_key:
        print("Failed to load API key. Please set OPENAI_API_KEY environment variable.")
        return
    
    try:
        # Initialize the agent
        agent = WebSearchAgent(api_key)
        
        print("\nWeb Search Agent initialized. Type 'quit' to exit.")
        print("Type 'clear' to clear conversation history.")
        
        # Main interaction loop
        while True:
            question = input("\nYour question: ").strip()
            
            if question.lower() == 'quit':
                print("Goodbye!")
                break
                
            if question.lower() == 'clear':
                agent.memory.clear()
                print("Conversation history cleared!")
                continue
                
            if not question:
                print("Please enter a valid question.")
                continue
            
            response = agent.ask(question)
            print("\nAnswer:", response)
            
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()