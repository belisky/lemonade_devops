import psutil
import time
import subprocess

# Configurable parameters
CPU_THRESHOLD = 80  # CPU usage percentage
CHECK_INTERVAL = 10  # Seconds between each CPU usage check
LARAVEL_SERVICE_NAME = "laravel-backend"  # Replace with your Laravel service name

def check_cpu_usage():
    """Check the current CPU usage percentage."""
    return psutil.cpu_percent(interval=1)

def restart_laravel_service():
    """Restart the Laravel backend service."""
    try:
        print(f"Restarting the Laravel service: {LARAVEL_SERVICE_NAME}")
        subprocess.run(["systemctl", "restart", LARAVEL_SERVICE_NAME], check=True)
        print(f"Service {LARAVEL_SERVICE_NAME} restarted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart the service: {e}")

def monitor_and_restart():
    """Monitor CPU usage and restart Laravel service if necessary."""
    while True:
        cpu_usage = check_cpu_usage()
        print(f"Current CPU usage: {cpu_usage}%")
        if cpu_usage > CPU_THRESHOLD:
            print(f"CPU usage exceeded {CPU_THRESHOLD}%. Restarting service.")
            restart_laravel_service()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    print(f"Monitoring CPU usage... (Threshold: {CPU_THRESHOLD}%)")
    try:
        monitor_and_restart()
    except KeyboardInterrupt:
        print("Monitoring stopped by user.")
