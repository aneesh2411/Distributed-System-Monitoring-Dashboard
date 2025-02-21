# Distributed System Monitoring Dashboard 🖥️

A comprehensive monitoring solution for distributed systems with real-time metrics, alerts, and predictive analytics.

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-enabled-blue.svg)](https://www.docker.com/)

## 🌟 Features

- 📊 Real-time system metrics collection (CPU, Memory, Disk usage)
- 🔍 Anomaly detection using configurable thresholds
- 📧 Email alerts for system anomalies
- 📈 Interactive web dashboard with real-time updates
- 🤖 Predictive analytics using machine learning
- 🐳 Docker containerization for easy deployment

## 🏗️ Architecture

The system consists of several components:

1. **Metrics Collection** (`agents/system_metrics_agent.py`)
   - Collects system metrics using psutil
   - Sends metrics to the central dashboard
   - Unique server identification

2. **Analytics** (`analytics/`)
   - Real-time anomaly detection
   - Predictive analytics using scikit-learn
   - Configurable thresholds

3. **Alerting** (`alerts/alert_manager.py`)
   - Email notifications for anomalies
   - Configurable alert thresholds
   - Detailed alert messages

4. **Dashboard** (`dashboard/`)
   - Flask web application
   - Real-time metrics visualization
   - Interactive charts using Chart.js
   - Multi-server support

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.9+
- SMTP server credentials (for email alerts)

## 🚀 Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/distributed-system-monitoring.git
   cd distributed-system-monitoring
   ```

2. **Configure environment variables:**
   - Copy `.env.example` to `.env`
   - Update with your SMTP credentials:
     ```bash
     EMAIL_USER=your-email@gmail.com
     EMAIL_PASSWORD=your-app-password
     SMTP_SERVER=smtp.gmail.com
     SMTP_PORT=587
     ```

3. **Run with Docker:**
   ```bash
   docker-compose up --build
   ```

4. **Access the dashboard:**
   - Open http://localhost:5000 in your browser

## 🛠️ Manual Installation

1. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\\Scripts\\activate   # Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the metrics agent:**
   ```bash
   python agents/system_metrics_agent.py
   ```

4. **Start the dashboard:**
   ```bash
   python dashboard/app.py
   ```

## ⚙️ Configuration

- **Anomaly Detection** (`analytics/anomaly_detection.py`):
  ```python
  thresholds = {
      'cpu': 80,      # CPU usage above 80%
      'memory': 90,   # Memory usage above 90%
      'disk': 85      # Disk usage above 85%
  }
  ```

- **Metrics Collection** (`agents/system_metrics_agent.py`):
  - Collection interval: 5 seconds (configurable)
  - Server identification: Automatic

- **Dashboard** (`dashboard/app.py`):
  - Port: 5000 (configurable)
  - History: Last 100 metrics per server

## 🔒 Security

- Environment variables for sensitive data
- Docker container isolation
- Secure SMTP communication
- No hardcoded credentials

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Chart.js](https://www.chartjs.org/) for beautiful visualizations
- [psutil](https://github.com/giampaolo/psutil) for system metrics
- [scikit-learn](https://scikit-learn.org/) for predictive analytics

## 📞 Support

For support, email a.kalisapudi@gmail.com or open an issue on GitHub.

## Future Improvements

- [ ] Add support for distributed tracing
- [ ] Integrate with Prometheus/Grafana
- [ ] Implement more advanced ML models
- [ ] Add user authentication
- [ ] Support for custom metrics
- [ ] Kubernetes deployment configuration 