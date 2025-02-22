"""Main application module."""
from flask import Flask
from api import api
from api.namespaces.servers import ns as servers_ns
from api.namespaces.metrics import ns as metrics_ns
from api.namespaces.auth import ns as auth_ns
from api.routes.metrics_endpoint import metrics_bp
from database import init_db

# Initialize Flask app
app = Flask(__name__)

# Register metrics endpoint
app.register_blueprint(metrics_bp)

# Initialize API
api.init_app(app)

# Add namespaces
api.add_namespace(auth_ns)
api.add_namespace(servers_ns)
api.add_namespace(metrics_ns)

# Initialize database
init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 