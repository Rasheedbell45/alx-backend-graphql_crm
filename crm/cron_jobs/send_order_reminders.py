#!/usr/bin/env python3
import sys
import requests
import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/order_reminders_log.txt"
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"

def main():
    try:
        # Setup GraphQL client
        transport = RequestsHTTPTransport(
            url=GRAPHQL_ENDPOINT,
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # Calculate 7 days ago
        seven_days_ago = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()

        # GraphQL query
        query = gql("""
        query GetRecentOrders($date: Date!) {
            orders(orderDate_Gte: $date, status: "PENDING") {
                id
                customer {
                    email
                }
            }
        }
        """)

        # Run query
        result = client.execute(query, variable_values={"date": seven_days_ago})

        # Prepare logging
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a") as f:
            for order in result.get("orders", []):
                line = f"{now} - Reminder: Order {order['id']} for {order['customer']['email']}\n"
                f.write(line)

        print("Order reminders processed!")

    except Exception as e:
        print(f"Error processing reminders: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
