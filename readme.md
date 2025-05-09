# Samadhan Hackathon Project - MedBot & Advanced Health Assistant (Archival)

## Overview

This repository contains the codebase for a project developed during a hackathon. It is being uploaded primarily for **archival purposes**. The project aimed to create an intelligent medical and psychological assistant, leveraging Large Language Models (LLMs) and vector databases for various functionalities.

While the project was a time-constrained endeavor, it explored several innovative features in the realm of AI-powered healthcare assistance.

## Key Features

This project incorporated several modules and functionalities:

1.  **MedBot - AI Powered Therapist and Doctor**:

    - A conversational AI (Chatbot) designed to act as a medical assistant and therapist.
    - Built using LLMs (potentially OpenAI's GPT models and MonsterLLM with Zephyr-7b-beta as seen in `monsterUI.py` and `toolTry.py`).
    - Capable of understanding user queries related to physical and mental health, providing information, and engaging in supportive conversations.
    - Integrated with tools for enhanced functionality (see `Modules/Tools.py` and `toolTry.py`).

2.  **Psychological Problem Identification (`psycoRecal`)**:

    - A feature to analyze user statements and suggest potential psychological issues they might be facing.
    - Utilized text embeddings (e.g., `text-embedding-ada-002`) and vector similarity search in a PostgreSQL database with the `pgvector` extension to match user statements with a pre-existing dataset of psychological problems and their embeddings (see `Modules/Database.py`).

3.  **User Information Management**:

    - `SaveUserInfo_tool`: Allows the system to save important information about the user (e.g., name, preferences, medical notes) for future personalized interactions.
    - `GetUserData_tool`: Retrieves previously saved user information based on query similarity.
    - This also leveraged text embeddings and vector search in the PostgreSQL database.

4.  **Image Vectorization and Search**:

    - `ImgVectorization`: A function to process images from folders, generate embeddings using `imgbeddings`, and store them in the PostgreSQL database (`MedicImgs` table).
    - `ImgSerch`: Enables searching for similar images based on an input image. This was demonstrated with a meme search (`Memes` table) and potentially for medical images.
    - The core idea was to use image embeddings for content-based image retrieval.

5.  **Reminder System (`SetReminder_tool`)**:

    - A tool to set reminders for users (e.g., medication times, appointments).
    - Implemented to send email reminders at scheduled times using `smtplib`.

6.  **Web Search Integration (`WebSearch_tool`)**:

    - Incorporated `DuckDuckGoSearchRun` to allow the bot to search the web for real-time information or to answer factual questions beyond its training data.

7.  **Data Handling and Storage**:

    - Extensive use of a **PostgreSQL database** with the **`pgvector` extension** to store and query text and image embeddings efficiently.
    - Functions in `Modules/Database.py` manage connections, table creation (e.g., `PsycoProb`, `Userinfo`, `UserData`, `MedicImgs`, `Memes`), data insertion with embeddings, and similarity-based retrieval.

8.  **User Interface (Experimental)**:
    - `monsterUI.py`: A Streamlit-based UI for interacting with the MedBot, powered by MonsterLLM.
    - Other UI experiments might have existed (e.g., `SampleUI.py`, `UiApp.py`).

## Technology Stack

- **Backend**: Python
- **Large Language Models (LLMs)**:
  - OpenAI Models (e.g., `gpt-4` for agent logic, `text-embedding-ada-002` for text embeddings)
  - MonsterLLM (`zephyr-7b-beta` via `llama_index`)
- **Database**: PostgreSQL with the `pgvector` extension for efficient vector similarity search.
- **Key Python Libraries**:
  - `langchain`: For building LLM-powered applications and agents.
  - `llama_index`: For data indexing and querying with LLMs.
  - `streamlit`: For creating interactive web UIs.
  - `openai`: Official OpenAI Python client.
  - `psycopg2-binary`: PostgreSQL adapter for Python.
  - `pgvector`: For working with vector types in psycopg2.
  - `imgbeddings`: For generating image embeddings.
  - `Pillow (PIL)`: For image processing.
  - `smtplib`: For sending emails (reminders).
  - `sentence-transformers` (implied by `embed_model="local:BAAI/bge-small-en-v1.5"` in `monsterUI.py`)
  - `pypdf`: For PDF parsing (as noted in `monsterUI.py` comments).
  - `deepface` (commented out in `Modules/Tools.py`): Potentially for emotion analysis from images.

## How It Worked (Conceptual Flow)

1.  **User Interaction**: Users would interact with the system, primarily through a chat interface (e.g., Streamlit app).
2.  **Input Processing**: The Langchain agent (e.g., in `toolTry.py`) would receive user input.
3.  **Tool Selection & Execution**: Based on the input and conversation context, the agent would decide if any specialized tools were needed (e.g., save user info, get user info, set reminder, search web, recall psychological problems).
4.  **Embedding Generation**: For tasks involving semantic understanding or similarity (text or image), embeddings would be generated using models like `text-embedding-ada-002` or `imgbeddings`.
5.  **Database Interaction**: Embeddings and associated data would be stored in or retrieved from the PostgreSQL database using `pgvector` for similarity searches.
6.  **LLM Response Generation**: The LLM would synthesize information from tools, database results, and its own knowledge to generate a response for the user.
7.  **Output**: The response would be displayed to the user.

## Project Structure Highlights

- `Modules/`: Contains core logic for database interactions (`Database.py`), agent tools (`Tools.py`), and potentially audio input (`AudioIn.py`).
- `toolTry.py`: Appears to be a primary script for initializing and running the Langchain agent with various tools.
- `monsterUI.py`: A Streamlit application providing a UI for a LlamaIndex-based query engine using MonsterLLM.
- `data/`: Likely contained documents for RAG (Retrieval Augmented Generation) as used by `SimpleDirectoryReader` in `monsterUI.py`.
- `files/`: Contains image datasets (e.g., `acne`, `bags`, `redness`) used for image vectorization and search experiments.

## Note for Archival

This project represents a snapshot of work done during a hackathon. Some features might be experimental or incomplete. API keys and sensitive credentials (like the email password in `Modules/Tools.py`) are present for hackathon demonstration purposes and should be managed securely in any real-world deployment. The primary goal of this repository is to preserve the ideas and efforts from that event.
