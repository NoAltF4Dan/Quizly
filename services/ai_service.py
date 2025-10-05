from google import genai

quiz_prompt = """

IMPORTANT: Return the result **only as plain JSON text** – do NOT use ```json, ``` or any Markdown formatting. No comments, no extra text. Just raw JSON.

Create a JSON object with the following structure:

{
  "title": "Create a concise quiz title based on the topic of the transcript.",
  "description": "Summarize the transcript in no more than 150 characters. Do not include any quiz questions or answers.",
  "questions": [
    {
      "question_title": "The first question goes here.",
      "question_options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "The correct answer from the above options"
    },
    ... (exactly 10 questions in total)
  ]
}

Requirements:
- Each question must have exactly 4 **distinct** answer options.
- Only one correct answer per question, and it must appear in 'question_options'.
- The output must be valid JSON – it should be parsable directly using e.g. `json.loads()` in Python.
- Do NOT include any explanations, comments, or any text outside the JSON block.
- Language of the quiz: **German**.
- DO NOT start or end the response with ```json or ``` – any such formatting is strictly forbidden.

If the output starts with ``` or contains ```json, the task is considered **not completed correctly**.

Here is the transcript:
"""


def generate_quiz(transcript):
    """Function that generates quiz content from a given transcript using the Gemini 2.5 Flash language model."""
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=quiz_prompt + transcript
    )

    return(response.text)