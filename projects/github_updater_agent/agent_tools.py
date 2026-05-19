import datetime
import subprocess  # <-- NEW: This lets Python run bash commands

def get_current_date():
    """Returns the current system date and time as a string."""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def get_git_status():
    """Runs 'git status' in the current directory and returns the output to the AI."""
    try:
        # Run the bash command and capture the text output
        result = subprocess.check_output(['git', 'status'], text=True, stderr=subprocess.STDOUT)
        return result
    except subprocess.CalledProcessError as e:
        # If git fails, we return the error to the AI so it knows what went wrong!
        return f"Error running git status: {e.output}"

def commit_changes(commit_message: str):
    """Commits the currently staged files to git with the provided commit message."""
    try:
        # Run git commit with the message the AI generates
        result = subprocess.check_output(['git', 'commit', '-m', commit_message], text=True, stderr=subprocess.STDOUT)
        return f"Successfully committed: {result}"
    except subprocess.CalledProcessError as e:
        return f"Error committing: {e.output}"
