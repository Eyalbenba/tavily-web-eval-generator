from collections import defaultdict
import random

class Curator:
    def __init__(self, cfg, utils):
        self.cfg = cfg
        self.utils = utils

    def run(self, state):
        """
        Prepare the final QA list with an even distribution across subjects, capped at num_qa total.

        Note: This can be improved by first selecting the best questions per subject
        before balancing.
        """
        qa_list = state.q_and_a
        subjects = state.qa_subjects
        num_qa = state.num_qa

        if len(qa_list) > num_qa:
            # Step 1: Group QAs by subject
            subject_to_qas = defaultdict(list)
            for qa in qa_list:
                subject_to_qas[qa.subject].append(qa)

            # Step 2: Calculate even distribution
            num_subjects = len(subjects)
            base_per_subject = num_qa // num_subjects
            remainder = num_qa % num_subjects

            # Step 3: Select QAs per subject (distribute remainder)
            selected_qas = []
            selected_set = set()  # To avoid duplicates
            for i, subject in enumerate(subjects):
                qas = subject_to_qas.get(subject, [])
                count = base_per_subject + (1 if i < remainder else 0)
                chosen = qas if len(qas) <= count else random.sample(qas, count)
                selected_qas.extend(chosen)
                selected_set.update(id(q) for q in chosen)

            # Step 4: If still short, fill randomly from remaining QAs
            if len(selected_qas) < num_qa:
                remaining_qas = [q for q in qa_list if id(q) not in selected_set]
                fill_count = num_qa - len(selected_qas)
                if len(remaining_qas) > fill_count:
                    selected_qas.extend(random.sample(remaining_qas, fill_count))
                else:
                    selected_qas.extend(remaining_qas)

            # Step 5: If (in rare cases) overfilled, trim to num_qa
            selected_qas = selected_qas[:num_qa]

            if self.cfg.DEBUG:
                print(f"QA list size - original: {len(qa_list)}, after selection: {len(selected_qas)}")
            return {"dataset": selected_qas}
        else:
            return {"dataset": qa_list}
