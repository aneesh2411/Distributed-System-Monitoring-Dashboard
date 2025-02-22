"""API package initialization."""
from flask import Flask
from flask_restx import Api

api = Api(
    title='System Monitoring API',
    version='1.0',
    description='A RESTful API for system monitoring and metrics collection',
    doc='/docs',
    prefix='/api/v1'
) 