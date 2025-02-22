"""Metric model for storing system metrics."""
from typing import Any
from sqlalchemy import Column, String, Float, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .base import Base

class Metric(Base):
    """Metric model."""
    
    __tablename__ = 'metrics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    server_id = Column(String(36), ForeignKey('servers.server_id'), nullable=False)
    cpu_usage = Column(Float, nullable=False)
    memory_usage = Column(Float, nullable=False)
    disk_usage = Column(Float, nullable=False)
    network_stats = Column(JSON, nullable=False)
    
    # Relationship with server
    server = relationship('Server', back_populates='metrics')

    def __repr__(self) -> str:
        """String representation."""
        return f'<Metric {self.id} for server {self.server_id}>'

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'Metric':
        """Create metric from dictionary."""
        return cls(
            cpu_usage=data['metrics']['cpu'],
            memory_usage=data['metrics']['memory'],
            disk_usage=data['metrics']['disk'],
            network_stats=data['metrics']['network']
        ) 