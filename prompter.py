import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Dict, Optional
from groq import Groq

# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("API key not found in environment variables.")

client = Groq(api_key=api_key)

# Output schema
class SemanticPromptOut(BaseModel):
    intent: str
    args: Dict[str, str]
    auth_level: Optional[str]
    status: Optional[str]
    timestamp: Optional[str]

def run_prompter(instruction: str) -> SemanticPromptOut:
    prompt = f"""
You are an instruction parser. Extract the user's intent and all relevant arguments from the following instruction.

Instruction:
\"\"\"{instruction}\"\"\"

Return the result as a valid JSON object with:
- `intent`: high-level action (e.g., "transfer", "book", "schedule")
- `args`: dictionary of extracted arguments (like amount, to_account, item, date, location, etc.)
- `auth_level`: authentication level if needed (L1–L5)
- `status`: always "ready for execution"
- `timestamp`: null unless explicitly present

Example:
{{
  "intent": "Transfer",
  "args": {{
    "amount": "75000 USD",
    "to_account": "7395-8845-2291",
    "from_account": "1559-6623-4401"
  }},
  "auth_level": "L4",
  "status": "ready for execution",
  "timestamp": null
}}

Respond with only the JSON.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # or "llama-3-1-8b-instant"
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    model_output = response.choices[0].message.content.strip()

    try:
        parsed = json.loads(model_output)
    except json.JSONDecodeError:
        raise ValueError(f"Model did not return valid JSON:\n{model_output}")

    return SemanticPromptOut(**parsed)

if __name__ == "__main__":
    instruction = "Book a flight from New York to San Francisco on August 12th at 10 AM"
    result = run_prompter(instruction)
    print(result.model_dump_json(indent=2))

    
