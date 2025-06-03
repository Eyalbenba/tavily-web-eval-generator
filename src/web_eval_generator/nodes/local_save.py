import json
from datetime import datetime
import os
import pandas as pd

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
        qa_list = state.dataset
        dataset_size = len(qa_list)
        max_subjects = 10
        subject_list = list(map(str, state.qa_subjects))
        if len(subject_list) > max_subjects:
            subjects = "_".join(subject_list[:max_subjects]) + "_..."
        else:
            subjects = "_".join(subject_list)
        dataset_name = f"{subjects}_RAG_Web_Search_{dataset_size}_QA_Dataset_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        file_path = f"{self.save_directory}/{dataset_name}"

        # Create DataFrame
        df = pd.DataFrame([
            {
                "question": qa.question,
                "answer": qa.answer,
                "answer_context": qa.answer_context,
                "citations": qa.citations,
                "provider": qa.provider,
                "subject": qa.subject
            }
            for qa in qa_list
        ])
        
        # Save as CSV
        df.to_csv(f"{file_path}.csv", index=False)

        # Also save as JSON for compatibility
        data = {
            "dataset_name": dataset_name,
            "description": f"RAG Web Search QA Dataset on the following subjects: {', '.join(subject_list)}",
            "dataset_size": dataset_size,
            "dataset": [
                {
                    "question": qa.question,
                    "answer": qa.answer,
                    "answer_context": qa.answer_context,
                    "citations": qa.citations,
                    "provider": qa.provider,
                    "subject": qa.subject
                } for qa in qa_list
            ]
        }

        with open(f"{file_path}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return {"output_message": f"Dataset '{dataset_name}' saved locally at {file_path} (CSV and JSON formats)."}