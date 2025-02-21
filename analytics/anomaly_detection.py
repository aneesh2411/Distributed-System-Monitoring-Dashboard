import numpy as np

def detect_anomaly(data):
    # Thresholds for different metrics
    thresholds = {
        'cpu': 80,      # CPU usage above 80%
        'memory': 90,   # Memory usage above 90%
        'disk': 85,     # Disk usage above 85%
        'network': {
            'bytes_sent': 1000000,  # 1MB/s
            'bytes_recv': 1000000   # 1MB/s
        }
    }
    
    anomalies = {}
    
    for metric, value in data.items():
        if isinstance(value, dict):
            # Handle nested metrics (like network)
            nested_anomalies = {}
            for sub_metric, sub_value in value.items():
                if (sub_metric in thresholds.get(metric, {}) and 
                    isinstance(sub_value, (int, float)) and
                    sub_value > thresholds[metric][sub_metric]):
                    nested_anomalies[sub_metric] = sub_value
            if nested_anomalies:
                anomalies[metric] = nested_anomalies
        else:
            # Handle simple metrics (cpu, memory, disk)
            if (metric in thresholds and 
                isinstance(value, (int, float)) and 
                value > thresholds[metric]):
                anomalies[metric] = value
    
    return anomalies 