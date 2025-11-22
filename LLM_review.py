from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_llm_review(df):
    """
    Takes a DataFrame with 'review' and 'sentiment' columns
    and generates AI suggestions for positive and negative comments.
    """
    # Combine all comments into a single prompt
    prompt = "Analyze the following YouTube comments.\n\n"
    for idx, row in df.iterrows():
        sentiment = row['sentiment'].capitalize()  # 'Positive' or 'Negative'
        review = row['review']
        prompt += f"Comment: {review}\nSentiment: {sentiment}\n\n"

    prompt += (
        "Summarize all feedback in a readable format. and provide actionable insights.\n"
        "For negative comments, suggest improvements.\n"
    )

    # Call Groq LLM
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
        max_completion_tokens=500,
        top_p=1,
        reasoning_effort="medium",
        stream=False,
        stop=None
    )

    # Collect response
    try:
        summary_text = completion.choices[0].message.content
    except:
        summary_text = "Error: Could not generate review."

    return summary_text
