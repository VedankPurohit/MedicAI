from langchain.tools import DuckDuckGoSearchRun

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

def demonstrate_search():
    search = DuckDuckGoSearchRun()
    
    # Basic search
    result1 = search.run("top 10 wasy to deel with procrastination")
    print(result1)
    print("Basic Search Result:", result1[:2000], "...\n")
    

# Run the demonstration
if __name__ == "__main__":
    demonstrate_search()