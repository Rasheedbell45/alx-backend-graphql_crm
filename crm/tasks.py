import requests
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime

@shared_task
def generate_crm_report():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # GraphQL client setup
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Query totals
    query = gql("""
    query {
        totalCustomers
        totalOrders
        totalRevenue
    }
    """)

    try:
        result = client.execute(query)
        customers = result["totalCustomers"]
        orders = result["totalOrders"]
        revenue = result["totalRevenue"]

        log_message = f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue\n"

    except Exception as e:
        log_message = f"{timestamp} - Failed to generate report: {e}\n"

    # Write to log
    with open("/tmp/crm_report_log.txt", "a") as f:
        f.write(log_message)
