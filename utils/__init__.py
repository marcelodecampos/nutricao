"""utils package
This package contains utility functions and classes used across the application.
"""

from .cpf import CPF
from .email_validator import is_valid_email
from .logger import get_logger, get_trace_back_from_exception

__all__ = ["CPF", "get_logger", "get_trace_back_from_exception", "is_valid_email"]

__version__ = "0.0.1"
