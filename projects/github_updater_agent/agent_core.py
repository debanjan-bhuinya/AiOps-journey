import google.generativeai as genai
import os
# Import all 5 tools now
from agent_tools import get_git_status, get_git_diff, stage_changes, commit_changes, pull_changes, push_changes

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY environment variable not found.")
    exit()

genai.configure(api_key=api_key)

# Bind ALL tools to the model
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    tools=[get_git_status, get_git_diff, stage_changes, commit_changes, pull_changes, push_changes]  
)

print("Agent is performing a resilient sync...")

chat = model.start_chat(enable_automatic_function_calling=True)

# The Advanced, Self-Correcting Prompt
user_prompt = """
You are a senior DevOps automation agent. Execute the following sequence to safely sync this repository:

1. READ: Use the status tool to see what files changed. If there are changes, use the diff tool to read the EXACT lines of code that were modified.
2. STAGE: Use the stage tool to add all changes.
3. SYNC: Use the pull tool to fetch any remote changes and prevent merge conflicts BEFORE you commit.
4. COMMIT: Using the context you learned from the diff tool, write a highly descriptive, conventional commit message and commit the files. (If there are no changes, skip this).
5. PUSH: Push the changes to the remote repository.
6. REPORT: Give me a final summary of the code you analyzed and the actions you took.
"""

response = chat.send_message(user_prompt)

print("\n--- Agent's Resilient Report ---")
print(response.text)
