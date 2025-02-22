"""API models for request/response serialization."""
from flask_restx import Model, fields

# Network statistics model
network_stats = Model('NetworkStats', {
    'bytes_sent': fields.Integer(required=True, description='Number of bytes sent'),
    'bytes_recv': fields.Integer(required=True, description='Number of bytes received')
})

# Metric model
metric = Model('Metric', {
    'id': fields.Integer(readonly=True, description='The metric identifier'),
    'server_id': fields.String(required=True, description='The server identifier'),
    'cpu_usage': fields.Float(required=True, description='CPU usage percentage'),
    'memory_usage': fields.Float(required=True, description='Memory usage percentage'),
    'disk_usage': fields.Float(required=True, description='Disk usage percentage'),
    'network_stats': fields.Nested(network_stats, required=True),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

# Server model
server = Model('Server', {
    'server_id': fields.String(required=True, description='Unique server identifier'),
    'hostname': fields.String(required=True, description='Server hostname'),
    'ip_address': fields.String(required=True, description='Server IP address'),
    'os_info': fields.String(required=True, description='Operating system information'),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

# Server with metrics
server_with_metrics = Model('ServerWithMetrics', {
    'server_id': fields.String(required=True, description='Unique server identifier'),
    'hostname': fields.String(required=True, description='Server hostname'),
    'ip_address': fields.String(required=True, description='Server IP address'),
    'os_info': fields.String(required=True, description='Operating system information'),
    'metrics': fields.List(fields.Nested(metric)),
    'created_at': fields.DateTime(readonly=True),
    'updated_at': fields.DateTime(readonly=True)
})

# Metric submission
metric_submission = Model('MetricSubmission', {
    'timestamp': fields.DateTime(required=True, description='Timestamp of the metrics'),
    'server_info': fields.Nested(server, required=True),
    'metrics': fields.Nested(metric, required=True)
}) 