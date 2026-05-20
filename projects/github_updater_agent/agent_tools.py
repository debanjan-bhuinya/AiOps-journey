import datetime
import subprocess

def get_current_date():
    """Returns the current system date and time as a string."""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def get_git_status():
    """Runs 'git status' in the current directory and returns the output to the AI."""
    try:
        result = subprocess.check_output(['git', 'status'], text=True, stderr=subprocess.STDOUT)
        return result
    except subprocess.CalledProcessError as e:
        return f"Error running git status: {e.output}"

def get_git_diff():
    """Runs 'git diff' to show the exact lines of code that were changed."""
    try:
        diff = subprocess.check_output(['git', 'diff'], text=True, stderr=subprocess.STDOUT)
        if not diff.strip():
            diff = subprocess.check_output(['git', 'diff', '--staged'], text=True, stderr=subprocess.STDOUT)
        return diff if diff.strip() else "No code changes found."
    except subprocess.CalledProcessError as e:
        return f"Error getting diff: {e.output}"

def stage_changes():
    """Stages all modified and untracked files using 'git add .' so they are ready to be committed."""
    try:
        result = subprocess.check_output(['git', 'add', '.'], text=True, stderr=subprocess.STDOUT)
        return "Successfully staged all files."
    except subprocess.CalledProcessError as e:
        return f"Error staging files: {e.output}"

def commit_changes(commit_message: str):
    """Commits the currently staged files to git with the provided commit message."""
    try:
        result = subprocess.check_output(['git', 'commit', '-m', commit_message], text=True, stderr=subprocess.STDOUT)
        return f"Successfully committed: {result}"
    except subprocess.CalledProcessError as e:
        return f"Error committing: {e.output}"

def pull_changes():
    """Pulls the latest changes from the remote repository to prevent merge conflicts."""
    try:
        result = subprocess.check_output(['git', 'pull', '--rebase', 'origin', 'main'], text=True, stderr=subprocess.STDOUT)
        return f"Successfully pulled: {result}"
    except subprocess.CalledProcessError as e:
        return f"Error pulling from remote: {e.output}"

def push_changes():
    """Pushes the locally committed changes to the remote GitHub repository."""
    try:
        result = subprocess.check_output(['git', 'push', '-u', 'origin', 'main'], text=True, stderr=subprocess.STDOUT)
        return f"Successfully pushed to remote: {result}"
    except subprocess.CalledProcessError as e:
        return f"Error pushing to remote: {e.output}"
