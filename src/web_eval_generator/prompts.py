QA_QUERIES_SYSTEM_PROMPT = """
**Objective:**
Today's date: {today}
Produce exactly {num_queries} diverse, clear, and well-crafted web search queries to gather the most recent, relevant, and comprehensive information about the input subject from general online sources.

**Guidelines:**
1. Ensure each query is clear, specific, and directly related to the subject.
2. Cover different aspects, perspectives, or subtopics of the subject with varied queries.
3. Prioritize queries likely to yield fresh, up-to-date results (e.g., by using terms like 'latest,' '{year},' 'recent news,' or 'updates').
4. Aim for comprehensive coverage by mixing both broad and focused queries.
"""

QA_QUERIES_USER_PROMPT = """
**Input:**
- **Subject:** `{subject}`
"""

QA_GENERATION_SYSTEM_PROMPT = """
You are a highly precise assistant that generates fact-based question-and-answer (QA) pairs, strictly in JSON, to evaluate AI tools’ ability to retrieve **definite, globally recognized facts** from the web as of {today}.

---

## **Instructions:**

**1. Analyze the document and generate 1 QA pair, following ALL criteria below:**

- **Question MUST be:**  
  - About a real-world entity, event, date, statistic, official decision, or person that has *already happened* (before or on {today}) or is *officially scheduled* as of {today}.  
  - Clear, direct, fully self-contained, and researchable by a global search engine without any additional context.
  - Focused on *definite, verifiable facts* with a single, official answer as of {today}.  
  - If referencing a source (article, paper, report, law, study, etc.), the question MUST include the **full, unique title or name of the source, and if possible, author(s), publication date, or another unique detail**.
  - **The question MUST uniquely identify the fact or event so that searching the question verbatim on Google or another search engine yields a single, precise answer.**
  - Prioritize questions about **recent or newly reported facts** (from within the last 30 days) if present.
  - **For events that have already happened as of {today}, use past-tense ("When did... occur?", "Who won...?", "What was the final score...?"). For future or scheduled events after {today}, use future-tense ("When is... scheduled to take place?"). DO NOT use future-tense for events in the past.**

- **Question MUST NOT be:**  
  - About predictions, expectations, forecasts, projected values, beliefs, opinions, or surveys (e.g., "What do experts believe...", "What is projected...").
  - About ambiguous, speculative, open-ended, or subjective topics, including questions about "recent events" without specific names, or generic phrases like "What caused...", "What led to...".
  - About future or hypothetical events not officially confirmed or completed.
  - About trends, "what will happen if..." scenarios, or any question that could return multiple, conflicting, or editorial answers.
  - Vague or incomplete (must not lack unique details—never ask for "the title of the study" without naming the study).

- **Examples (Allowable):**  
  - "Who won the 2025 Eurovision Song Contest?"  
  - "When did the 2025 Daytona 500 take place?" (if {today} is after the event)
  - "When is the 97th Academy Awards scheduled to take place?" (if {today} is before the event)
  - "According to the 2025 Digital Media Trends report by Deloitte, what percentage of US consumers currently have a cable or satellite TV subscription?"  
  - "What is the year-to-date return for Hims & Hers Health (HIMS) in 2025?"

- **Examples (Not Allowable):**  
  - "What is one prediction for AI in 2025?"  
  - "What percentage of experts expect..."  
  - "Which sector is likely to be most impacted..."  
  - "What is the projected expansion..."  
  - "What is the title of the publication where the pig liver transplantation study was published?" (**must specify study name, author, or unique detail**)
  - "What recent event caused the S&P 500 to erase its 2025 losses?" (**not definite, unique, or searchable**)
  - "What new tournament did the NBA add for the 2023 to 2024 season?" (**must specify the tournament name, must be relevant to {today}**)

**2. Answers:**  
  - Must be a precise, standalone fact directly and unambiguously stated in the content—**suitable for copy-paste**.  
  - The **answer_context** must be an **exact copy** (sentence or phrase) from the content that directly supports the answer (no paraphrasing).

**3. Output Format:**  
Return a JSON array of objects, each containing: `question`, `answer`, and `answer_context`.

If the document does NOT contain suitable, definite, fully testable facts, output the following SKIP template:

```json
{
  "qa_pairs": [
    {
      "question": "SKIP",
      "answer": "SKIP",
      "answer_context": "SKIP"
    }
  ]
}


Example responses:
{
  "qa_pairs": [
    {
      "question": "Which country won the 2025 Eurovision Song Contest?",
      "answer": "Sweden won the 2025 Eurovision Song Contest.",
      "answer_context": "Sweden was announced as the winner of the 2025 Eurovision Song Contest held in Geneva on May 17, 2025."
    },
    {
      "question": "What is the latest inflation rate reported in the United States?",
      "answer": "The latest inflation rate in the United States is 2.3%.",
      "answer_context": "The U.S. Bureau of Labor Statistics reported an inflation rate of 2.3% for April 2025."
    },
    {
      "question": "Who is currently leading the 2025 French Open men's singles tournament?",
      "answer": "Carlos Alcaraz is currently leading the 2025 French Open men's singles tournament.",
      "answer_context": "Carlos Alcaraz advanced to the semifinals, making him the current leader in the 2025 French Open men's singles tournament."
    }
  ]
}
"""

QA_GENERATION_USER_PROMPT = """
**Input:**
- **Document:** `{page_content}`
"""