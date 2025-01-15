import json
from datetime import datetime
import os

class LocalDatasetSaver:
    def __init__(self, save_directory="datasets"):
        """
        Initialize the LocalDatasetSaver.

        Args:
            save_directory (str): Directory where datasets will be saved.
        """
        self.save_directory = save_directory
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)

    def run(self, state):
        """
        Save the given QA list locally as a JSON file.

        Args:
            state: The state object containing q_and_as and qa_subject.

        Returns:
            None
        """
        qa_list = state.q_and_as
        dataset_name = f"{state.qa_subject}_RAG_Web_Search_QA_Dataset_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        file_path = f"{self.save_directory}/{dataset_name}.json"

        # Prepare data for saving
        data = {
            "dataset_name": dataset_name,
            "description": f"RAG Web Search QA Dataset saved locally at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "examples": [
                {"question": qa.question, "expected_answer": qa.answer} for qa in qa_list
            ]
        }

        # Save to JSON file
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return {"output_message": f"Dataset '{dataset_name}' saved locally at {file_path}."}