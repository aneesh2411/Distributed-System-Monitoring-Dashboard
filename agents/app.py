"""Agent server application."""
import os
import logging
from flask import Flask, jsonify
from agents.metrics_handler import metrics_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Register metrics endpoint
    app.register_blueprint(metrics_bp)
    
    @app.route('/health')
    def health_check():
        """Health check endpoint."""
        return jsonify({"status": "healthy"})
    
    @app.errorhandler(500)
    def handle_500(error):
        """Handle internal server errors."""
        logger.error(f"Internal server error: {error}")
        return jsonify({"error": "Internal server error"}), 500
    
    logger.info(f"Starting agent server: {os.environ.get('SERVER_NAME', 'unknown')}")
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 