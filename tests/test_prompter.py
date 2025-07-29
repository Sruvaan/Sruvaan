"""
Unit tests for the Prompter agent.
"""

import pytest
from src.schemas import RawInstructionInput, SemanticPromptOut
from src.prompter import run_prompter, extract_intent, extract_entities


class TestPrompter:
    """Test cases for the Prompter agent."""
    
    def test_run_prompter_basic(self):
        """Test basic prompter functionality."""
        input_data = RawInstructionInput(
            instruction="Transfer $75,000 to account 7395-8845-2291 from account 1559-6623-4401",
            language="EN"
        )
        
        result = run_prompter(input_data)
        
        assert isinstance(result, SemanticPromptOut)
        assert result.intent == "transfer"
        assert "amount" in result.entities
        assert "to_account" in result.entities
        assert "from_account" in result.entities
        assert result.auth_level == "L4"
        assert result.status == "ready for execution"
    
    def test_extract_intent_transfer(self):
        """Test intent extraction for transfer operations."""
        instruction = "Transfer $1000 to account 1234-5678-9012-3456"
        intent = extract_intent(instruction)
        assert intent == "transfer"
    
    def test_extract_intent_booking(self):
        """Test intent extraction for booking operations."""
        instruction = "Book a flight to Paris for next week"
        intent = extract_intent(instruction)
        assert intent == "book_flight"
    
    def test_extract_intent_email(self):
        """Test intent extraction for email operations."""
        instruction = "Send an email to john@example.com"
        intent = extract_intent(instruction)
        assert intent == "send_email"
    
    def test_extract_intent_unknown(self):
        """Test intent extraction for unknown operations."""
        instruction = "Random text without clear intent"
        intent = extract_intent(instruction)
        assert intent == "unknown"
    
    def test_extract_entities_amount(self):
        """Test entity extraction for amounts."""
        instruction = "Transfer $50,000 to account 1234-5678-9012-3456"
        entities = extract_entities(instruction)
        
        assert "amount" in entities
        assert entities["amount"] == "50000 USD"
    
    def test_extract_entities_accounts(self):
        """Test entity extraction for account numbers."""
        instruction = "Transfer $1000 to account 7395-8845-2291 from account 1559-6623-4401"
        entities = extract_entities(instruction)
        
        assert "to_account" in entities
        assert "from_account" in entities
        assert entities["to_account"] == "7395-8845-2291"
        assert entities["from_account"] == "1559-6623-4401"
    
    def test_extract_entities_destination(self):
        """Test entity extraction for destinations."""
        instruction = "Book a flight to Paris from London"
        entities = extract_entities(instruction)
        
        assert "destination" in entities
        assert entities["destination"] == "Paris"
    
    def test_prompter_with_different_languages(self):
        """Test prompter with different language inputs."""
        input_data = RawInstructionInput(
            instruction="Transfer $1000 to account 1234-5678-9012-3456",
            language="FR"
        )
        
        result = run_prompter(input_data)
        
        assert isinstance(result, SemanticPromptOut)
        assert result.intent == "transfer"
        assert len(result.entities) > 0 