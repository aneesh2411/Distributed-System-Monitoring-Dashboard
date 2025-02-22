"""Prometheus metrics configuration and collectors."""
from prometheus_client import Counter, Histogram, Gauge, Info
from prometheus_client.core import CollectorRegistry
import time

# Create a custom registry
registry = CollectorRegistry()

# HTTP request metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status'],
    registry=registry
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    registry=registry
)

# System metrics
system_metrics_gauge = Gauge(
    'system_metrics',
    'System metrics collected from servers',
    ['server_id', 'metric_type'],
    registry=registry
)

# Server info
server_info = Info(
    'server_info',
    'Information about monitored servers',
    ['server_id'],
    registry=registry
)

# API metrics
api_requests_total = Counter(
    'api_requests_total',
    'Total number of API requests',
    ['endpoint', 'method'],
    registry=registry
)

# Database metrics
db_operation_duration_seconds = Histogram(
    'db_operation_duration_seconds',
    'Database operation duration in seconds',
    ['operation', 'table'],
    registry=registry
)

# Cache metrics
cache_hits_total = Counter(
    'cache_hits_total',
    'Total number of cache hits',
    ['cache_type'],
    registry=registry
)

cache_misses_total = Counter(
    'cache_misses_total',
    'Total number of cache misses',
    ['cache_type'],
    registry=registry
)

# Active users gauge
active_users = Gauge(
    'active_users',
    'Number of active users',
    registry=registry
)

def track_request_duration(method, endpoint):
    """Context manager to track request duration."""
    start_time = time.time()
    yield
    duration = time.time() - start_time
    http_request_duration_seconds.labels(method=method, endpoint=endpoint).observe(duration)

def update_system_metrics(server_id, metrics):
    """Update system metrics in Prometheus."""
    for metric_type, value in metrics.items():
        if isinstance(value, (int, float)):
            system_metrics_gauge.labels(server_id=server_id, metric_type=metric_type).set(value)

def update_server_info(server_id, info):
    """Update server information in Prometheus."""
    server_info.labels(server_id=server_id).info({
        'hostname': info['hostname'],
        'ip': info['ip'],
        'os': info['os']
    }) 