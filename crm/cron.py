import datetime
import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    # Write to the heartbeat log file
    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(message)

    # Optional: Verify GraphQL hello field
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=False,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        query = gql("""
        query {
            hello
        }
        """)

        result = client.execute(query)
        with open("/tmp/crm_heartbeat_log.txt", "a") as f:
            f.write(f"{timestamp} GraphQL hello response: {result['hello']}\n")

    except Exception as e:
        with open("/tmp/crm_heartbeat_log.txt", "a") as f:
            f.write(f"{timestamp} Failed to query GraphQL hello: {e}\n")
            
def update_low_stock():
    """Runs GraphQL mutation to restock low stock products and logs results"""
    mutation = """
    mutation {
      updateLowStockProducts {
        success
        updatedProducts {
          name
          stock
        }
      }
    }
    """
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": mutation}
        )
        result = response.json()

        now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
        log_entry = f"{now} Low stock update:\n{result}\n"

        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            f.write(log_entry)

        print("Low stock update processed!")

    except Exception as e:
        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            f.write(f"Error: {e}\n")
