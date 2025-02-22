"""Test fixtures for the test suite."""
import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_metrics():
    """Fixture that returns mock system metrics"""
    return {
        'cpu': 45.5,
        'memory': 60.0,
        'disk': 75.2,
        'network': {
            'bytes_sent': 1024,
            'bytes_recv': 2048
        }
    }

@pytest.fixture
def mock_server_info():
    """Fixture that returns mock server information"""
    return {
        'hostname': 'test-server',
        'ip': '192.168.1.100',
        'os': 'Linux 5.10.0',
        'server_id': 'test-id-123'
    }

@pytest.fixture
def mock_redis():
    """Fixture that returns a mock Redis client"""
    redis_mock = MagicMock()
    redis_mock.get.return_value = None
    redis_mock.set.return_value = True
    return redis_mock

@pytest.fixture
def mock_db_session():
    """Fixture that returns a mock database session"""
    session_mock = MagicMock()
    session_mock.commit.return_value = None
    session_mock.rollback.return_value = None
    return session_mock 