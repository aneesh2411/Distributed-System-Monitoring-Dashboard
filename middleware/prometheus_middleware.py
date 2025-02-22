"""Prometheus middleware for request tracking."""
from functools import wraps
from flask import request, Response
from metrics.prometheus_metrics import (
    http_requests_total,
    track_request_duration,
    api_requests_total
)

def track_requests_middleware():
    """Middleware to track HTTP requests using Prometheus metrics."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Track request duration
            with track_request_duration(request.method, request.endpoint):
                response = f(*args, **kwargs)
            
            # Record request metrics
            status = response.status_code if isinstance(response, Response) else 200
            http_requests_total.labels(
                method=request.method,
                endpoint=request.endpoint,
                status=status
            ).inc()
            
            # Track API requests separately
            if request.endpoint and request.endpoint.startswith('api'):
                api_requests_total.labels(
                    endpoint=request.endpoint,
                    method=request.method
                ).inc()
            
            return response
        return decorated
    return decorator 