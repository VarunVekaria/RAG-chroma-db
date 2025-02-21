# AI-Powered Coding Assistant and Knowledge Base

This project is an AI-powered coding assistant and knowledge base designed to enhance developer productivity by providing instant coding assistance and summarizing Python code functions. It leverages OpenAI's GPT-4 model and ChromaDB for efficient data storage and retrieval.

## Features

- **Automated Code Summarization**: Extracts and summarizes functions from Python scripts using OpenAI's GPT-4 model.
- **Interactive Query System**: Allows users to input coding questions and receive accurate, context-aware responses.
- **Persistent Storage**: Utilizes ChromaDB to store and manage summarized code snippets and metadata.
- **Environment Management**: Uses dotenv for secure and efficient management of environment variables.

## Technologies Used

- Python
- OpenAI GPT-4
- ChromaDB
- LangChain
- dotenv
- RecursiveCharacterTextSplitter

## Setup

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/ai-coding-assistant.git
    cd ai-coding-assistant
    ```

2. **Create a virtual environment and activate it**:
    ```sh
    python -m venv venv
    venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On macOS/Linux
    ```

3. **Install the required dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    Create a [.env](http://_vscodecontentref_/0) file in the project root directory and add your OpenAI API key:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    ```

## Usage

### Filling the Database

1. **Run the [fill_db.py](http://_vscodecontentref_/1) script** to summarize functions from Python scripts and store them in ChromaDB:
    ```sh
    python fill_db.py
    ```

### Asking Questions

1. **Run the [ask.py](http://_vscodecontentref_/2) script** to interact with the AI-powered coding assistant:
    ```sh
    python ask.py
    ```

2. **Input your coding question** when prompted, and the assistant will provide an answer based on the stored knowledge.

## Project Structure
NOTE : Populate the data folder with relevant files that you want to summarise before running fill_db.py
- [fill_db.py](http://_vscodecontentref_/3): Script to summarize Python code functions and store them in ChromaDB.
- [ask.py](http://_vscodecontentref_/4): Script to interact with the AI-powered coding assistant.
- [data](http://_vscodecontentref_/5): Directory containing Python scripts to be summarized.
- [chroma_db](http://_vscodecontentref_/6): Directory for ChromaDB storage.

## Example

### Summarizing Functions

The [fill_db.py](http://_vscodecontentref_/7) script processes Python scripts in the [data](http://_vscodecontentref_/8) directory, summarizes their functions, and stores the summaries in ChromaDB.

### Asking Questions

The [ask.py](http://_vscodecontentref_/9) script allows users to input coding questions and receive responses based on the stored summaries.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.