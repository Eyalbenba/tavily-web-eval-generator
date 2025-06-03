import dotenv
dotenv.load_dotenv()
import os
import asyncio
from web_eval_generator.graph import graph
from web_eval_generator.state import GeneratorState

async def main():
    # Initialize ResearchState with user inputs
    qa_subjects = \
        [
        "Basketball",
        "Baseball"
        ]
    state = GeneratorState(num_qa=5,qa_subjects=qa_subjects)

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
