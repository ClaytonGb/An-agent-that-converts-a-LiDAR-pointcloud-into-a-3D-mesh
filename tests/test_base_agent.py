"""Unit tests for BaseAgent."""

import unittest
from agents.base_agent import BaseAgent


class ConcreteAgent(BaseAgent):
    """Concrete implementation of BaseAgent for testing."""
    
    def process(self, data):
        """Simple process implementation."""
        return data


class TestBaseAgent(unittest.TestCase):
    """Test cases for BaseAgent."""
    
    def test_agent_initialization(self):
        """Test that agent initializes correctly."""
        agent = ConcreteAgent("TestAgent")
        self.assertEqual(agent.name, "TestAgent")
        self.assertIsNotNone(agent.logger)
    
    def test_logging_methods(self):
        """Test that logging methods don't raise errors."""
        agent = ConcreteAgent("TestAgent")
        
        # These should not raise exceptions
        agent.log_info("Info message")
        agent.log_warning("Warning message")
        agent.log_error("Error message")
    
    def test_get_status(self):
        """Test get_status method."""
        agent = ConcreteAgent("TestAgent")
        status = agent.get_status()
        
        self.assertIsInstance(status, dict)
        self.assertEqual(status['name'], "TestAgent")
        self.assertEqual(status['status'], 'active')
    
    def test_process_method_exists(self):
        """Test that process method is implemented."""
        agent = ConcreteAgent("TestAgent")
        result = agent.process("test_data")
        self.assertEqual(result, "test_data")


if __name__ == '__main__':
    unittest.main()

