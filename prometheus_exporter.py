import os
import time
import requests
from prometheus_client import start_http_server, Gauge

# Environment variables
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')
SCRAPE_INTERVAL = int(os.getenv('SCRAPE_INTERVAL', '15'))  # Default scrape interval: 15 seconds

# Metrics
metrics = {
    "messages": Gauge(
        'rabbitmq_individual_queue_messages',
        'Total count of messages in RabbitMQ queue',
        ['host', 'vhost', 'name']
    ),
    "messages_ready": Gauge(
        'rabbitmq_individual_queue_messages_ready',
        'Ready messages in RabbitMQ queue',
        ['host', 'vhost', 'name']
    ),
    "messages_unacknowledged": Gauge(
        'rabbitmq_individual_queue_messages_unacknowledged',
        'Unacknowledged messages in RabbitMQ queue',
        ['host', 'vhost', 'name']
    ),
}

def fetch_rabbitmq_data():
    """Fetch queue data from RabbitMQ management HTTP API."""
    url = f"http://{RABBITMQ_HOST}:15672/api/queues"
    try:
        response = requests.get(url, auth=(RABBITMQ_USER, RABBITMQ_PASSWORD), timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching RabbitMQ data: {e}")
        return []

def update_metrics():
    """Update Prometheus metrics with RabbitMQ queue data."""
    queue_data = fetch_rabbitmq_data()
    for queue in queue_data:
        vhost = queue.get('vhost', '')
        name = queue.get('name', '')
        host = RABBITMQ_HOST
        metrics["messages"].labels(host=host, vhost=vhost, name=name).set(queue.get('messages', 0))
        metrics["messages_ready"].labels(host=host, vhost=vhost, name=name).set(queue.get('messages_ready', 0))
        metrics["messages_unacknowledged"].labels(host=host, vhost=vhost, name=name).set(queue.get('messages_unacknowledged', 0))

def main():
    """Main function to start the Prometheus exporter."""
    print(f"Starting RabbitMQ Prometheus exporter on {RABBITMQ_HOST}")
    start_http_server(8000)  # Default Prometheus metrics endpoint port
    while True:
        update_metrics()
        time.sleep(SCRAPE_INTERVAL)

if __name__ == "__main__":
    main()
