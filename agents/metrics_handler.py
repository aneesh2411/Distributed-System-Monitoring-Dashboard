"""Metrics handler for agent servers."""
from flask import Blueprint, Response, current_app
from prometheus_client import (
    generate_latest,
    CONTENT_TYPE_LATEST,
    Gauge,
    CollectorRegistry
)
import psutil
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a custom registry
registry = CollectorRegistry()

# Create metrics
cpu_usage = Gauge('cpu_usage_percent', 'CPU Usage in percent', registry=registry)
memory_usage = Gauge('memory_usage_percent', 'Memory Usage in percent', registry=registry)
disk_usage = Gauge('disk_usage_percent', 'Disk Usage in percent', registry=registry)
network_bytes_sent = Gauge('network_bytes_sent', 'Network bytes sent', registry=registry)
network_bytes_recv = Gauge('network_bytes_recv', 'Network bytes received', registry=registry)

metrics_bp = Blueprint('metrics', __name__)

@metrics_bp.route('/metrics', methods=['GET'])
def metrics():
    """Collect and return current system metrics."""
    try:
        logger.info("Collecting metrics...")
        
        # Update CPU metrics
        cpu_percent = psutil.cpu_percent(interval=None)  # Don't wait for interval
        cpu_usage.set(cpu_percent)
        logger.debug(f"CPU Usage: {cpu_percent}%")
        
        # Update memory metrics
        memory = psutil.virtual_memory()
        memory_usage.set(memory.percent)
        logger.debug(f"Memory Usage: {memory.percent}%")
        
        # Update disk metrics
        disk = psutil.disk_usage('/')
        disk_usage.set(disk.percent)
        logger.debug(f"Disk Usage: {disk.percent}%")
        
        # Update network metrics
        network = psutil.net_io_counters()
        network_bytes_sent.set(network.bytes_sent)
        network_bytes_recv.set(network.bytes_recv)
        logger.debug(f"Network - Sent: {network.bytes_sent}, Received: {network.bytes_recv}")
        
        # Generate and return metrics
        return Response(generate_latest(registry), mimetype=CONTENT_TYPE_LATEST)
    except Exception as e:
        logger.error(f"Error collecting metrics: {str(e)}")
        return Response(f"Error collecting metrics: {str(e)}", status=500) 