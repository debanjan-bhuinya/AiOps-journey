from kubernetes import client, config

def get_cluster_status():
    """Connects to K8s and returns a list of all pods and their statuses."""
    try:
        # This loads the exact same config file that 'kubectl' uses behind the scenes
        config.load_kube_config()
        v1 = client.CoreV1Api()

        # Fetch all pods across all namespaces
        pods = v1.list_pod_for_all_namespaces(watch=False)
        
        status_report = "Live Kubernetes Pod Statuses:\n"
        for pod in pods.items:
            # We grab the namespace, the pod name, and its current health phase
            status_report += f"Namespace: {pod.metadata.namespace} | Pod: {pod.metadata.name} | Status: {pod.status.phase}\n"
        
        return status_report
    except Exception as e:
        return f"Error connecting to Kubernetes: {str(e)}"

def get_failed_pod_logs():
    """Finds any pod not in a Running/Succeeded state and fetches its recent logs."""
    try:
        config.load_kube_config()
        v1 = client.CoreV1Api()
        pods = v1.list_pod_for_all_namespaces(watch=False)
        
        crash_report = ""
        for pod in pods.items:
            # Check if the pod is in a bad state
            if pod.status.phase not in ["Running", "Succeeded"]:
                crash_report += f"\n🚨 CRASH LOGS FOR: {pod.metadata.name} (Namespace: {pod.metadata.namespace})\n"
                try:
                    # Grab the last 30 lines of the log to avoid overwhelming the AI
                    logs = v1.read_namespaced_pod_log(name=pod.metadata.name, namespace=pod.metadata.namespace, tail_lines=30)
                    crash_report += f"{logs}\n"
                except Exception as e:
                    crash_report += f"[Log retrieval failed: Pod might be stuck in initialization or completely dead. Error: {str(e)}]\n"
        
        return crash_report if crash_report else "No crashing pods detected. Logs are clean."
    except Exception as e:
        return f"Error connecting to Kubernetes: {str(e)}"
