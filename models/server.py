"""Server model for storing server information."""
from typing import Any
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base import Base

class Server(Base):
    """Server model."""
    
    __tablename__ = 'servers'

    server_id = Column(String(36), primary_key=True)
    hostname = Column(String(255), nullable=False)
    ip_address = Column(String(45), nullable=False)  # IPv6 compatible
    os_info = Column(String(255), nullable=False)
    
    # Relationship with metrics
    metrics = relationship('Metric', back_populates='server', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        """String representation."""
        return f'<Server {self.hostname} ({self.ip_address})>'

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary with additional fields."""
        data = super().to_dict()
        data['metrics'] = [metric.to_dict() for metric in self.metrics[-10:]]  # Last 10 metrics
        return data 