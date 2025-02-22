"""Tests for the system metrics collection module."""
import pytest
from unittest.mock import patch, MagicMock
from agents.system_metrics_agent import get_system_metrics, get_server_info, collect_and_send_metrics

@pytest.mark.unit
def test_get_system_metrics():
    """Test that system metrics are collected correctly"""
    metrics = get_system_metrics()
    
    # Check if all required metrics are present
    assert 'cpu' in metrics
    assert 'memory' in metrics
    assert 'disk' in metrics
    assert 'network' in metrics
    
    # Check if metrics are within valid ranges
    assert 0 <= metrics['cpu'] <= 100
    assert 0 <= metrics['memory'] <= 100
    assert 0 <= metrics['disk'] <= 100
    assert isinstance(metrics['network']['bytes_sent'], (int, float))
    assert isinstance(metrics['network']['bytes_recv'], (int, float))

@pytest.mark.unit
def test_get_server_info():
    """Test that server information is collected correctly"""
    server_info = get_server_info()
    
    # Check if all required fields are present
    assert 'hostname' in server_info
    assert 'ip' in server_info
    assert 'os' in server_info
    assert 'server_id' in server_info
    
    # Check if server_id is a valid UUID
    import uuid
    assert uuid.UUID(server_info['server_id'])

@pytest.mark.integration
@patch('requests.post')
def test_metrics_sending(mock_post, mock_metrics, mock_server_info):
    """Test that metrics are sent correctly to the dashboard"""
    # Mock the response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'status': 'success'}
    mock_post.return_value = mock_response
    
    # Mock get_system_metrics and get_server_info
    with patch('agents.system_metrics_agent.get_system_metrics', return_value=mock_metrics), \
         patch('agents.system_metrics_agent.get_server_info', return_value=mock_server_info), \
         patch('time.sleep', return_value=None):
        try:
            collect_and_send_metrics()
        except KeyboardInterrupt:
            pass
    
    # Verify that post was called with correct data structure
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert 'json' in kwargs
    data = kwargs['json']
    
    assert 'timestamp' in data
    assert data['server_info'] == mock_server_info
    assert data['metrics'] == mock_metrics

@pytest.mark.integration
@patch('requests.post')
def test_metrics_sending_failure(mock_post, mock_metrics, mock_server_info):
    """Test handling of failed metrics sending"""
    # Mock a failed response
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_post.return_value = mock_response
    
    # Mock get_system_metrics and get_server_info
    with patch('agents.system_metrics_agent.get_system_metrics', return_value=mock_metrics), \
         patch('agents.system_metrics_agent.get_server_info', return_value=mock_server_info), \
         patch('time.sleep', return_value=None), \
         patch('logging.error') as mock_log:
        try:
            collect_and_send_metrics()
        except KeyboardInterrupt:
            pass
    
    # Verify error was logged
    mock_log.assert_called_with(
        "Failed to send metrics. Status code: %s",
        500
    ) 