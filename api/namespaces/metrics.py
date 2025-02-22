"""Metrics API namespace."""
from flask_restx import Namespace, Resource
from flask import request
from typing import Dict, List
from database import get_db
from models.metric import Metric
from models.server import Server
from ..models import metric, metric_submission
from auth.decorators import login_required, admin_required, api_key_required
from cache.redis_config import (
    cache_response,
    invalidate_cache_prefix,
    CACHE_TIMES
)

# Create namespace
ns = Namespace('metrics', description='Metrics management operations')

# Register models
ns.models[metric.name] = metric
ns.models[metric_submission.name] = metric_submission

@ns.route('/')
class MetricList(Resource):
    """Shows a list of all metrics, and lets you POST to add new ones"""

    @ns.doc('list_metrics')
    @ns.marshal_list_with(metric)
    @login_required
    @cache_response('metrics:list', CACHE_TIMES['metrics'])
    def get(self) -> List[Dict]:
        """List all metrics"""
        with get_db() as db:
            metrics = db.query(Metric).all()
            return [m.to_dict() for m in metrics]

    @ns.doc('submit_metrics')
    @ns.expect(metric_submission)
    @ns.marshal_with(metric, code=201)
    @api_key_required
    def post(self) -> Dict:
        """Submit new metrics (requires API key)"""
        with get_db() as db:
            # Get or create server
            server_info = ns.payload['server_info']
            server = db.query(Server).filter(Server.server_id == server_info['server_id']).first()
            if not server:
                server = Server(**server_info)
                db.add(server)
            
            # Create metric
            new_metric = Metric.from_dict(ns.payload)
            db.add(new_metric)
            db.commit()
            
            # Invalidate caches
            server_id = server_info['server_id']
            invalidate_cache_prefix('metrics:list')
            invalidate_cache_prefix(f'metrics:server:{server_id}')
            invalidate_cache_prefix(f'servers:detail:{server_id}')
            
            return new_metric.to_dict(), 201

@ns.route('/server/<string:server_id>')
@ns.response(404, 'Server not found')
@ns.param('server_id', 'The server identifier')
class ServerMetrics(Resource):
    """Show metrics for a specific server"""

    @ns.doc('get_server_metrics')
    @ns.marshal_list_with(metric)
    @login_required
    @cache_response('metrics:server', CACHE_TIMES['server_metrics'])
    def get(self, server_id: str) -> List[Dict]:
        """Fetch metrics for a given server"""
        with get_db() as db:
            server = db.query(Server).filter(Server.server_id == server_id).first()
            if not server:
                ns.abort(404, f"Server {server_id} doesn't exist")
            return [m.to_dict() for m in server.metrics]

@ns.route('/<int:id>')
@ns.response(404, 'Metric not found')
@ns.param('id', 'The metric identifier')
class MetricResource(Resource):
    """Show a single metric"""

    @ns.doc('get_metric')
    @ns.marshal_with(metric)
    @login_required
    @cache_response('metrics:detail', CACHE_TIMES['metrics'])
    def get(self, id: int) -> Dict:
        """Fetch a metric given its identifier"""
        with get_db() as db:
            metric_obj = db.query(Metric).filter(Metric.id == id).first()
            if not metric_obj:
                ns.abort(404, f"Metric {id} doesn't exist")
            return metric_obj.to_dict()

    @ns.doc('delete_metric')
    @ns.response(204, 'Metric deleted')
    @admin_required
    def delete(self, id: int) -> None:
        """Delete a metric given its identifier (admin only)"""
        with get_db() as db:
            metric_obj = db.query(Metric).filter(Metric.id == id).first()
            if not metric_obj:
                ns.abort(404, f"Metric {id} doesn't exist")
                
            server_id = metric_obj.server_id
            db.delete(metric_obj)
            
            # Invalidate caches
            invalidate_cache_prefix('metrics:list')
            invalidate_cache_prefix(f'metrics:detail:{id}')
            invalidate_cache_prefix(f'metrics:server:{server_id}')
            invalidate_cache_prefix(f'servers:detail:{server_id}')
            
            return '', 204 