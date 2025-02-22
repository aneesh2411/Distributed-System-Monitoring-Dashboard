"""Tests for database models."""
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.server import Server
from models.metric import Metric

@pytest.fixture
def test_db():
    """Create a test database."""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def test_server_creation(test_db):
    """Test server model creation."""
    server = Server(
        server_id='test-123',
        hostname='test-server',
        ip_address='192.168.1.100',
        os_info='Linux 5.10.0'
    )
    test_db.add(server)
    test_db.commit()

    saved_server = test_db.query(Server).first()
    assert saved_server.server_id == 'test-123'
    assert saved_server.hostname == 'test-server'
    assert saved_server.created_at is not None
    assert saved_server.updated_at is not None

def test_metric_creation(test_db):
    """Test metric model creation."""
    server = Server(
        server_id='test-123',
        hostname='test-server',
        ip_address='192.168.1.100',
        os_info='Linux 5.10.0'
    )
    test_db.add(server)

    metric = Metric(
        server_id=server.server_id,
        cpu_usage=45.5,
        memory_usage=60.0,
        disk_usage=75.2,
        network_stats={'bytes_sent': 1024, 'bytes_recv': 2048}
    )
    test_db.add(metric)
    test_db.commit()

    saved_metric = test_db.query(Metric).first()
    assert saved_metric.server_id == 'test-123'
    assert saved_metric.cpu_usage == 45.5
    assert saved_metric.memory_usage == 60.0
    assert saved_metric.network_stats['bytes_sent'] == 1024

def test_server_metrics_relationship(test_db):
    """Test relationship between server and metrics."""
    server = Server(
        server_id='test-123',
        hostname='test-server',
        ip_address='192.168.1.100',
        os_info='Linux 5.10.0'
    )
    test_db.add(server)

    # Add multiple metrics
    for i in range(3):
        metric = Metric(
            server_id=server.server_id,
            cpu_usage=45.5 + i,
            memory_usage=60.0 + i,
            disk_usage=75.2 + i,
            network_stats={'bytes_sent': 1024 * i, 'bytes_recv': 2048 * i}
        )
        test_db.add(metric)
    
    test_db.commit()

    saved_server = test_db.query(Server).first()
    assert len(saved_server.metrics) == 3
    assert saved_server.metrics[0].cpu_usage == 45.5
    assert saved_server.metrics[-1].cpu_usage == 47.5

def test_cascade_delete(test_db):
    """Test that deleting a server cascades to its metrics."""
    server = Server(
        server_id='test-123',
        hostname='test-server',
        ip_address='192.168.1.100',
        os_info='Linux 5.10.0'
    )
    test_db.add(server)

    metric = Metric(
        server_id=server.server_id,
        cpu_usage=45.5,
        memory_usage=60.0,
        disk_usage=75.2,
        network_stats={'bytes_sent': 1024, 'bytes_recv': 2048}
    )
    test_db.add(metric)
    test_db.commit()

    test_db.delete(server)
    test_db.commit()

    assert test_db.query(Server).count() == 0
    assert test_db.query(Metric).count() == 0 