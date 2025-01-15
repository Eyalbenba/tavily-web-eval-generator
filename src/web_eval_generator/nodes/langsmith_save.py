from langsmith import Client
from langsmith.utils import LangSmithNotFoundError
from datetime import datetime

class LangSmithDatasetSaver:
    def __init__(self):
        """
        Initialize the QASaver with a LangSmith client.

        Args:
            dataset_name (str): Name of the dataset to create or retrieve.
            description (str): Description of the dataset.
        """
        self.client = Client()
        self.dataset_name = "RAG Web Search QA Dataset"
        self.description = f"RAG Web Search QA Dataset made by Tavily Web Search QA Generator at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    def run(self, state):
        """
        Save the given QA list to LangSmith as a dataset.

        Args:
            qa_list (List[Dict[str, str]]): List of question-answer pairs to save.

        Returns:
            None
        """
        # Check if the dataset already exists
        qa_list = state.q_and_as
        dataset_name = f"{state.qa_subject} - {self.dataset_name}  - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        try:
            exists_dataset = self.client.read_dataset(dataset_name=dataset_name)
            print(f"Dataset '{self.dataset_name}' already exists.")
            print("You can access the dataset via the URL: ", exists_dataset.url)
            return
        except LangSmithNotFoundError:
            # Create the dataset if it doesn't exist
            pass

        # Create the dataset
        dataset = self.client.create_dataset(
            dataset_name=dataset_name,
            description=self.description,
        )

        # Prepare inputs and outputs for bulk creation
        inputs = [{"question": qa.question} for qa in qa_list]
        outputs = [{"expected_answer": qa.answer} for qa in qa_list]

        # Save the examples
        self.client.create_examples(
            inputs=inputs,
            outputs=outputs,
            dataset_id=dataset.id,
        )

        return {"output_message": f"Dataset '{dataset_name}' saved in langsmith, You can access the dataset via the URL {dataset.url}."}
