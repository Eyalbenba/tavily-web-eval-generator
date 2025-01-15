QA_QUERIES_SYSTEM_PROMPT = """
**Objective:**
Produce {num_queries} clear, effective, and varied queries to gather the most relevant and recent information about the input subject.

**Guidelines:**
1. Ensure clarity, specificity, and relevance to the subject.
2. Prioritize fresh and comprehensive results.
"""

QA_QUERIES_USER_PROMPT = """
**Input:**
- **Subject:** `{subject}`
"""

QA_GENERATION_SYSTEM_PROMPT = """
**Objective:**
Generate 1 highly specific, fact-based question-and-answer pair that reflects real-world, search-oriented queries. The question must be relevant for an online search engine.

**Guidelines for Questions:**
1. Focus on creating questions that people would typically search for online to find specific, verifiable information, targeting globally relevant topics like events, people, places, or data.
2. Ensure the question is concise, direct, and targets a single factual detail, avoiding ambiguity or multi-hop reasoning.
3. Avoid questions tied to personal anecdotes, localized contexts, or content structure (e.g., "Who shared a photo?" or "What is the title of the article?").

**Guidelines for Answers:**
1. Answers must be precise, fact-based, and directly derived from the content, suitable for quick retrieval from a reliable source (e.g., "The Eiffel Tower was completed in 1889.").
2. Answers should be standalone and avoid referencing the context of the content (e.g., do not use phrases like "Based on the article...").
3. Answers must reflect globally recognizable facts and avoid subjective or ambiguous language (e.g., "approximately," "likely," or "some people believe").
"""


QA_GENERATION_USER_PROMPT = """
**Input:**
- **Page Content:** `{page_content}`
"""

