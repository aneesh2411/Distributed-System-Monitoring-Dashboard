import os
import sys
from collections import defaultdict
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from flask import Flask, request, jsonify, render_template
from analytics.anomaly_detection import detect_anomaly
from alerts.alert_manager import send_alert

app = Flask(__name__)

# Store metrics for multiple servers
# Format: {server_id: [metrics]}
metrics_store = defaultdict(list)
# Store server information
servers_info = {}

@app.route('/metrics', methods=['POST'])
def receive_metrics():
    try:
        data = request.json
        logger.debug(f"Received metrics data: {data}")
        
        server_info = data['server_info']
        server_id = server_info['server_id']
        
        # Store or update server information
        servers_info[server_id] = {
            'hostname': server_info['hostname'],
            'ip': server_info['ip'],
            'os': server_info['os'],
            'last_seen': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Store metrics
        metrics_store[server_id].append(data)
        
        # Keep only last 100 metrics per server
        if len(metrics_store[server_id]) > 100:
            metrics_store[server_id].pop(0)
        
        # Check for anomalies
        anomalies = detect_anomaly(data['metrics'])
        if anomalies:
            # Include server information in alert
            alert_data = {
                'server_info': server_info,
                'anomalies': anomalies,
                'timestamp': data['timestamp']
            }
            send_alert(alert_data)
        
        return jsonify({
            "status": "Metrics received", 
            "server_id": server_id,
            "metrics": data['metrics']
        }), 200
    except Exception as e:
        logger.error(f"Error processing metrics: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def dashboard():
    # Prepare data for the dashboard
    dashboard_data = {
        'servers': servers_info,
        'metrics': {
            server_id: server_metrics[-1] if server_metrics else None
            for server_id, server_metrics in metrics_store.items()
        }
    }
    logger.debug(f"Rendering dashboard with initial data: {dashboard_data}")
    return render_template('dashboard.html', data=dashboard_data)

@app.route('/metrics/<server_id>', methods=['GET'])
def get_server_metrics(server_id):
    try:
        if server_id in metrics_store:
            # Return the last 20 metrics for the chart
            metrics = metrics_store[server_id][-20:] if metrics_store[server_id] else []
            logger.debug(f"Returning metrics for server {server_id}: {metrics}")
            return jsonify(metrics)
        logger.warning(f"Server {server_id} not found in metrics store")
        return jsonify({"error": "Server not found"}), 404
    except Exception as e:
        logger.error(f"Error retrieving metrics for server {server_id}: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/servers', methods=['GET'])
def get_servers():
    try:
        # Add last metrics to server info
        response = {}
        for server_id, info in servers_info.items():
            last_metrics = metrics_store[server_id][-1]['metrics'] if metrics_store[server_id] else None
            response[server_id] = {
                **info,
                'last_metrics': last_metrics
            }
        logger.debug(f"Returning servers info: {response}")
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error retrieving servers: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs(os.path.join(os.path.dirname(__file__), 'templates'), exist_ok=True)
    print("\nMulti-Server Monitoring Dashboard is running!")
    print("Access the dashboard at: http://localhost:5000")
    print("To stop the dashboard, press CTRL+C")
    app.run(debug=True, host='0.0.0.0', port=5000) 