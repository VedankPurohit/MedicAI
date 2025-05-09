from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
import os
from dotenv import load_dotenv

from Modules.Tools import SaveUserInfo_tool, GetUserData_tool, SetReminder_tool, Reminders, psycoProb

load_dotenv()

MemoryArray = [""]

# List of tools to be used by the agent
tools = [SaveUserInfo_tool, GetUserData_tool,SetReminder_tool]#, psycoProb]

# Initialize the language model (you can change model_name to any OpenAI model you have access to)
llm = ChatOpenAI(model_name="gpt-4", temperature=0)

# Set up the memory for conversation history
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
prompt = "System: You are a Medical asistance bot, you provide help with both physical and mentel health acting as a Doctor and tharapist, you are given tools to help get data to help user, make sure you dont go off topic, only answer questions related to physical or mental health, try to ask questions to user to understand the user, also converse about nothing illigal/UnEthical and if user talks about it then guid them away from it \n User: "

# memory.save_context({"input": prompt}, {"output": "Hello this is MedBot how can i help you, i can provide assistance in both mentel and physical problems"})

# Create the agent with the tools, the LLM, and memory
agent = initialize_agent(
    tools=tools,                                # List of tools for the agent
    llm=llm,                                    # LLM that powers the chatbot
    agent_type=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION ,  # Agent type
    verbose=True,                               # Enable verbose to see decision-making
    handle_parsing_errors=True,                 # Handle parsing errors
    memory=memory,                               # Add memory to keep track of conversation history
)

# Start a conversational loop
def Ask(Que):
    user_input = Que # Get user input
    
    if user_input.lower() == 'quit':
        return 0

    # Agent processes the input and decides what to use
    state = prompt + user_input
    # for w in MemoryArray:
    #     state += w +"\n"

    response = agent.invoke(state)#+" For any answer use follow the langchain formate correctly Thought: agent thought here \n Action:")
    print(Reminders)
    # MemoryArray.append("User : "+user_input)
    # MemoryArray.append("Response : "+ response["output"])

    # print(MemoryArray[-1],MemoryArray[-2])
    
    # Display the agent's response
    return response['output']
    
print(Ask("Hii, im feeling low rn"))