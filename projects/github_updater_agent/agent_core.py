import google.generativeai as genai
import os
# 1. Import BOTH git tools
from agent_tools import get_git_status, commit_changes 

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY environment variable not found.")
    exit()

genai.configure(api_key=api_key)

# 2. Give the AI an array of multiple tools
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    tools=[get_git_status, commit_changes]  
)

print("Agent is checking status and writing your commit...")

chat = model.start_chat(enable_automatic_function_calling=True)

# 3. A Multi-Step Prompt
user_prompt = """
1. Check my local git status.
2. If there are files ready to be committed, write a professional, concise commit message summarizing the changes.
3. Use the commit tool to actually commit the files with that message.
4. Tell me what you did.
"""

response = chat.send_message(user_prompt)

print("\n--- Agent's Final Report ---")
print(response.text)
