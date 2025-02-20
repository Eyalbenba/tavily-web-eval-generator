
# Tavily Real-Time Dataset Generator for RAG Evals

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/eyal-ben-barouch-007-1a2b3c4d5/)




The **Real-Time Dataset Generator** is an advanced agent designed to **automate the creation of datasets** for evaluating **web-augmented AI agents**. By **generating domain-specific queries**, **collecting real-time web data**, and **filtering results**, it streamlines the evaluation process for **LLM-based agents**. 

---
![workflow](https://i.imgur.com/PpJFX0o.png)
---
## 🌟 Key Features

### 1. `generate_qa_search_queries`
This node generates targeted search queries based on the subject and input context. It prepares high-quality search queries to ensure that subsequent retrieval processes focus on the most relevant information.

### 2. `search`
Leverages the Tavily Search API to retrieve web pages or documents related to the generated queries. This node forms the basis of the retrieval process, providing the necessary context for generating meaningful question-answer pairs.

### 3. `generate_qa`
Processes each retrieved web page to generate question-answer pairs. Using a map-reduce paradigm, it extracts key insights from the content and synthesizes comprehensive QA items for each document.

### 4. `save`
Ensures that the generated question-answer pairs are saved in langsmith or locally. (Based on user input)

---

## 🚀 Getting Started with Tavily Real-Time Dataset Generator

### Input

#### Parameters
- **`num_qa`**: Specifies the number of question-answer items to generate. For example, setting this to `100` will produce 100 QA items.
- **`qa_subject`**: Defines the subject focus for QA generation, such as "Sports," "Stocks," or "News." This ensures that the pipeline tailors its output to specific user needs.
- **`save_to_langsmith`**: Bool Parameter to indicate where to save the dataset


### Prerequisites
- **Tavily API Key**: [Sign Up for an API Key](https://www.tavily.com)
- **OpenAI API Key**: [Sign Up for an API Key](https://www.openai.com)
- **Langsmith API Key**: [Sign Up for an API Key](https://www.langchain.com)



### Installation Steps

#### 1. Clone the Repository
```bash
git clone https://github.com/Eyalbenba/tavily-web-eval-generator.git
cd tavily-web-eval-generator
```

#### 2. Create a Virtual Environment
To avoid dependency conflicts, create and activate a virtual environment:
```bash
python -m venv venv  
source venv/bin/activate    # macOS/Linux  
venv\Scripts\activate       # Windows  
```
#### 3. Set Up API Keys
Configure your Tavily, OpenAI, and Langsmith API keys by exporting them as environment variables or placing them in a `.env` file:  
```bash
export TAVILY_API_KEY={Your Tavily API Key here}  
export OPENAI_API_KEY={Your OpenAI API Key here}  
export LANGSMITH_API_KEY={Your Langsmith API Key here}  
```
#### 4. Install Dependencies
Install the required dependencies for the project:  
```bash
pip install -r requirements.txt
```

#### 5. Example Run:
```bash
import dotenv
dotenv.load_dotenv()
import asyncio
from src.web_eval_generator.graph import graph
from src.web_eval_generator.state import GeneratorState

async def main():
    # Initialize ResearchState with user inputs
    state = GeneratorState(num_qa=100,qa_subject="NBA Basketball")

    # Run the graph workflow
    print("Starting the QA Generation workflow...")
    try:
        result = await graph.ainvoke(state)  # Use `ainvoke` for async execution
        print("\nWorkflow completed successfully.")
        print("Final state:", result)
    except Exception as e:
        print(f"An error occurred during the workflow execution: {e}")

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
```
#### 6. Example Output:
![langsmith_saved_example](https://imgur.com/VrgqGUX.png)

---
## 🧠 How It Works

Learn more about the **Real-Time Dataset Generator** in our detailed blog: [Effortless Web-Based RAG Evaluation Using Tavily and LangGraph](https://medium.com/@DataSnake/effortless-web-based-rag-evaluation-using-tavily-and-langgraph-08cac44c8016).

