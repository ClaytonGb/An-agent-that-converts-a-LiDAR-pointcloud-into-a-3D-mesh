"""Base agent class for all agents in the system."""

from abc import ABC, abstractmethod
from typing import Any, Dict
import logging


class BaseAgent(ABC):
    """Abstract base class for all agents."""
    
    def __init__(self, name: str):
        """Initialize the agent.
        
        Args:
            name: Name of the agent
        """
        self.name = name
        self.logger = logging.getLogger(f"Agent.{name}")
        self.logger.setLevel(logging.INFO)
        
        # Only add handler if logger doesn't already have one
        # This prevents duplicate log messages when agents are recreated
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'[%(asctime)s] [{self.name}] %(levelname)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    @abstractmethod
    def process(self, data: Any) -> Any:
        """Process input data and return result.
        
        Args:
            data: Input data to process
            
        Returns:
            Processed result
        """
        pass
    
    def log_info(self, message: str):
        """Log info message."""
        self.logger.info(message)
    
    def log_error(self, message: str):
        """Log error message."""
        self.logger.error(message)
    
    def log_warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status.
        
        Returns:
            Dictionary containing agent status information
        """
        return {
            'name': self.name,
            'status': 'active'
        }
