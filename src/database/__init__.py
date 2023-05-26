"""
Database package for the Airport Management System.
"""

from .config import DB_CONFIG
from .connection import DatabaseConnection

__all__ = ['DB_CONFIG', 'DatabaseConnection'] 