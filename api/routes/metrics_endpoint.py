"""Prometheus metrics endpoint."""
from flask import Blueprint, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from metrics.prometheus_metrics import registry

metrics_bp = Blueprint('metrics', __name__)

@metrics_bp.route('/metrics')
def metrics():
    """Expose Prometheus metrics."""
    return Response(generate_latest(registry), mimetype=CONTENT_TYPE_LATEST) 