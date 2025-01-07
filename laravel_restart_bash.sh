#!/bin/bash

# Configuration
SERVICE_NAME="laravel-backend"  # Replace with your Laravel backend service name
CPU_THRESHOLD=80               # CPU usage threshold percentage
CHECK_INTERVAL=10              # Check interval in seconds

# Function to get current CPU usage
get_cpu_usage() {
    # This uses the 'top' command to get the average CPU usage in the first line.
    top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}'
}

# Function to restart the Laravel backend service
restart_service() {
    echo "[WARNING] Restarting service: $SERVICE_NAME..."
    sudo systemctl restart "$SERVICE_NAME"
    if [ $? -eq 0 ]; then
        echo "[INFO] Service '$SERVICE_NAME' restarted successfully."
    else
        echo "[ERROR] Failed to restart service '$SERVICE_NAME'. Check systemctl logs for details."
    fi
}

# Main monitoring loop
echo "[INFO] Starting CPU monitoring..."
while true; do
    # Get current CPU usage
    CPU_USAGE=$(get_cpu_usage)
    CPU_USAGE=${CPU_USAGE%.*}  # Convert to integer for comparison

    echo "[INFO] Current CPU usage: ${CPU_USAGE}%"

    # Check if CPU usage exceeds the threshold
    if [ "$CPU_USAGE" -gt "$CPU_THRESHOLD" ]; then
        echo "[WARNING] CPU usage (${CPU_USAGE}%) exceeded threshold (${CPU_THRESHOLD}%)."
        restart_service
    fi

    # Wait for the defined interval before checking again
    sleep "$CHECK_INTERVAL"
done
