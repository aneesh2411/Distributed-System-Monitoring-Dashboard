import psutil
import time
import requests
import socket
import platform
import uuid
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get server identification
def get_server_info():
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        os_info = f"{platform.system()} {platform.release()}"
        server_id = str(uuid.uuid4())  # Unique ID for this server instance
        
        logger.info(f"Server Info - Hostname: {hostname}, IP: {ip}, OS: {os_info}")
        
        return {
            'hostname': hostname,
            'ip': ip,
            'os': os_info,
            'server_id': server_id
        }
    except Exception as e:
        logger.error(f"Error getting server info: {str(e)}", exc_info=True)
        raise

def get_system_metrics():
    try:
        metrics = {
            'cpu': psutil.cpu_percent(interval=1),
            'memory': psutil.virtual_memory().percent,
            'disk': psutil.disk_usage('/').percent,
            'network': {
                'bytes_sent': psutil.net_io_counters().bytes_sent,
                'bytes_recv': psutil.net_io_counters().bytes_recv
            }
        }
        logger.debug(f"Collected metrics: {metrics}")
        return metrics
    except Exception as e:
        logger.error(f"Error collecting metrics: {str(e)}", exc_info=True)
        raise

def collect_and_send_metrics():
    # Get server information once
    server_info = get_server_info()
    logger.info(f"Starting metrics collection for server: {server_info['hostname']} ({server_info['ip']})")

    # Get the dashboard URL from environment variable or use default
    dashboard_url = os.getenv('DASHBOARD_URL', 'http://localhost:5000')
    metrics_endpoint = f"{dashboard_url}/metrics"
    logger.info(f"Using metrics endpoint: {metrics_endpoint}")

    while True:
        try:
            metrics = get_system_metrics()
            data = {
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'server_info': server_info,
                'metrics': metrics
            }
            
            response = requests.post(metrics_endpoint, json=data)
            if response.status_code == 200:
                logger.info(f"Metrics sent successfully for {server_info['hostname']}")
                logger.debug(f"Response: {response.json()}")
            else:
                logger.error(f"Failed to send metrics. Status code: {response.status_code}")
                logger.error(f"Response: {response.text}")
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Failed to connect to the dashboard at {metrics_endpoint}: {str(e)}")
        except Exception as e:
            logger.error(f"Error sending metrics: {str(e)}", exc_info=True)
        
        time.sleep(5)  # Send metrics every 5 seconds

if __name__ == "__main__":
    try:
        collect_and_send_metrics()
    except KeyboardInterrupt:
        logger.info("Stopping metrics collection...")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True) 