import ollama
import sys
# Import both tools now
from k8s_tools import get_cluster_status, get_failed_pod_logs

print("\n🤖 Local K8s Agent: Auditing infrastructure...")

# 1. Gather all the context pre-emptively
print("📡 Fetching cluster status...")
cluster_data = get_cluster_status()

print("📂 Scanning for crash logs...")
crash_logs = get_failed_pod_logs()

# 2. The Advanced SRE Prompt
prompt = f"""
You are an elite Senior Site Reliability Engineer (SRE).
I am giving you the current status of my Kubernetes cluster, along with the raw crash logs for any failing pods.

Task:
1. Identify exactly which pods are failing based on the logs.
2. Read the logs and explain the ROOT CAUSE of the crash in plain English.
3. Provide the exact 'kubectl' command or code fix I need to run to resolve the issue.

--- CLUSTER STATUS ---
{cluster_data}

--- CRASH LOGS ---
{crash_logs}
"""

print("🧠 AI is analyzing logs and formulating a fix...\n")

# 3. Generate the response using your local Llama 3.2 model
try:
    response = ollama.chat(model='llama3.2', messages=[
        {'role': 'user', 'content': prompt}
    ])
    
    print("="*60)
    print("🩺 AIOps Diagnostic Report & Remediation Plan")
    print("="*60)
    print(response['message']['content'].strip())
    print("="*60 + "\n")
    
except Exception as e:
    print(f"Error communicating with local AI: {e}")
    sys.exit(1)
