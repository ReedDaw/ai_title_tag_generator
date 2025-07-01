import pandas as pd
import openai
from tqdm import tqdm
import os

# Set your API key securely
openai.api_key = os.getenv("OPENAI_API_KEY") or "your-api-key-here"

# Define prompt template
def build_prompt(row):
    return f"""
You are an expert in SEO and copywriting.

Based on the following information, generate an HTML <title> tag that is:
- Concise and under 60 characters
- Keyword-rich and relevant to the page content
- Optimized for search intent
- Unique and clear

Input:
URL: {row['URL']}
Current Title Tag: {row['Current Title']}
Meta Description: {row['Meta Description']}
H1: {row['H1']}
Content Snippet: {row['Content Snippet']}

Output:
SEO Title Tag:
"""

# Function to get a completion
def generate_title_tag(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        output = response['choices'][0]['message']['content'].strip()
        return output.replace("SEO Title Tag:", "").strip('" ')
    except Exception as e:
        print(f"Error: {e}")
        return ""

# Load input CSV
input_file = "input_pages.csv"
df = pd.read_csv(input_file)

# Add output column
df['AI Title Tag'] = ""

# Process rows
for i, row in tqdm(df.iterrows(), total=len(df)):
    prompt = build_prompt(row)
    ai_title = generate_title_tag(prompt)
    df.at[i, 'AI Title Tag'] = ai_title

# Save output CSV
df.to_csv("output_with_ai_title_tags.csv", index=False)
print("✅ Done! Output saved to 'output_with_ai_title_tags.csv'")
