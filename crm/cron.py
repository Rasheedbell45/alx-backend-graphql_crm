import datetime
import requests

def log_crm_heartbeat():
    """Logs CRM heartbeat every 5 minutes with optional GraphQL health check"""
    now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_entry = f"{now} CRM is alive\n"

    # Write to heartbeat log
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(log_entry)

    # Optional GraphQL health check
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"}
        )
        if response.status_code == 200:
            print("GraphQL endpoint is responsive:", response.json())
        else:
            print("GraphQL health check failed:", response.status_code)
    except Exception as e:
        print("GraphQL health check error:", e)
