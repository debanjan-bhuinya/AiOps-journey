import subprocess
import sys
import ollama
from agent_tools import commit_changes, push_changes

print("\n🤖 Local AI: Analyzing your repository offline...")

# 1. Force Git to acknowledge all files (even new ones) BEFORE taking the diff
try:
    subprocess.run(['git', 'add', '.'], check=True)
    diff = subprocess.check_output(['git', 'diff', '--staged'], text=True, stderr=subprocess.STDOUT)
except subprocess.CalledProcessError:
    diff = ""

if not diff.strip():
    print("No changes found to commit! Make sure you edited a file.")
    sys.exit()

# 2. Ask your Local Llama model to write the message
prompt = f"""
Analyze this git diff and write a single, professional conventional commit message.
Do not explain the changes, just output the commit message string itself.

Diff:
{diff}
"""

print("Thinking...\n")
response = ollama.chat(model='llama3.2', messages=[
    {'role': 'user', 'content': prompt}
])

suggested_msg = response['message']['content'].strip()

# 3. The Human-in-the-Loop Interface
print("="*40)
print(f"Suggested Message: {suggested_msg}")
print("="*40 + "\n")

print("Would you like to commit these changes?")
print("1. Use the AI's suggested message.")
print("2. Write my own custom message.")
print("3. Cancel.")

choice = input("\nEnter your choice (1/2/3): ")

if choice == '3':
    print("Action canceled. Nothing committed.")
    sys.exit()

final_msg = suggested_msg if choice == '1' else input("\nEnter your custom commit message: ")

# 4. Execute standard tools (We already staged in Step 1, so we just commit and push!)
print(f"\n🚀 Committing with message: '{final_msg}'")
print(commit_changes(final_msg))
print(push_changes())
print("\n✅ Local Sync Complete!")
