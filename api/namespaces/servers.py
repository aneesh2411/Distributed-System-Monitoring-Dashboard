"""Servers API namespace."""
from flask_restx import Namespace, Resource
from flask import request
from typing import Dict, List
from database import get_db
from models.server import Server
from ..models import server, server_with_metrics
from auth.decorators import login_required, admin_required
from cache.redis_config import (
    cache_response,
    invalidate_cache_prefix,
    CACHE_TIMES
)

# Create namespace
ns = Namespace('servers', description='Server management operations')

# Register models
ns.models[server.name] = server
ns.models[server_with_metrics.name] = server_with_metrics

@ns.route('/')
class ServerList(Resource):
    """Shows a list of all servers, and lets you POST to add new ones"""

    @ns.doc('list_servers')
    @ns.marshal_list_with(server)
    @login_required
    @cache_response('servers:list', CACHE_TIMES['server'])
    def get(self) -> List[Dict]:
        """List all servers"""
        with get_db() as db:
            servers = db.query(Server).all()
            return [s.to_dict() for s in servers]

    @ns.doc('create_server')
    @ns.expect(server)
    @ns.marshal_with(server, code=201)
    @admin_required
    def post(self) -> Dict:
        """Create a new server (admin only)"""
        with get_db() as db:
            new_server = Server(**ns.payload)
            db.add(new_server)
            db.commit()
            
            # Invalidate server list cache
            invalidate_cache_prefix('servers:list')
            
            return new_server.to_dict(), 201

@ns.route('/<string:server_id>')
@ns.response(404, 'Server not found')
@ns.param('server_id', 'The server identifier')
class ServerResource(Resource):
    """Show a single server and lets you delete them"""

    @ns.doc('get_server')
    @ns.marshal_with(server_with_metrics)
    @login_required
    @cache_response('servers:detail', CACHE_TIMES['server'])
    def get(self, server_id: str) -> Dict:
        """Fetch a server given its identifier"""
        with get_db() as db:
            server_obj = db.query(Server).filter(Server.server_id == server_id).first()
            if not server_obj:
                ns.abort(404, f"Server {server_id} doesn't exist")
            return server_obj.to_dict()

    @ns.doc('delete_server')
    @ns.response(204, 'Server deleted')
    @admin_required
    def delete(self, server_id: str) -> None:
        """Delete a server given its identifier (admin only)"""
        with get_db() as db:
            server_obj = db.query(Server).filter(Server.server_id == server_id).first()
            if not server_obj:
                ns.abort(404, f"Server {server_id} doesn't exist")
            db.delete(server_obj)
            
            # Invalidate caches
            invalidate_cache_prefix('servers:list')
            invalidate_cache_prefix(f'servers:detail:{server_id}')
            invalidate_cache_prefix(f'metrics:server:{server_id}')
            
            return '', 204

    @ns.doc('update_server')
    @ns.expect(server)
    @ns.marshal_with(server)
    @admin_required
    def put(self, server_id: str) -> Dict:
        """Update a server given its identifier (admin only)"""
        with get_db() as db:
            server_obj = db.query(Server).filter(Server.server_id == server_id).first()
            if not server_obj:
                ns.abort(404, f"Server {server_id} doesn't exist")
            
            # Update server attributes
            for key, value in ns.payload.items():
                setattr(server_obj, key, value)
            
            db.commit()
            
            # Invalidate caches
            invalidate_cache_prefix('servers:list')
            invalidate_cache_prefix(f'servers:detail:{server_id}')
            
            return server_obj.to_dict() 