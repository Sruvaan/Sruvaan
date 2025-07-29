"""
Integration tests for the complete 6-agent MCP pipeline.
"""

import pytest
from src.schemas import RawInstructionInput
from src.prompter import run_prompter
from src.cryptor import run_cryptor
from src.decryptor import run_decryptor
from src.mimicus import run_mimicus
from src.probator import run_probator
from src.praeceptor import run_praeceptor


class TestPipelineIntegration:
    """Integration tests for the complete pipeline."""
    
    def test_complete_pipeline_flow(self):
        """Test the complete pipeline from raw input to final output."""
        # Step 1: Prompter
        raw_input = RawInstructionInput(
            instruction="Transfer $75,000 to account 7395-8845-2291 from account 1559-6623-4401",
            language="EN"
        )
        
        prompter_output = run_prompter(raw_input)
        assert prompter_output.intent == "transfer"
        assert "amount" in prompter_output.entities
        assert "to_account" in prompter_output.entities
        assert "from_account" in prompter_output.entities
        
        # Step 2: Cryptor (HKP Encryption)
        cryptor_output = run_cryptor(prompter_output)
        assert cryptor_output.role_tag == "Γ5"
        assert cryptor_output.pop_signature is not None
        assert cryptor_output.time_tag is not None
        assert "encrypted_fields" in cryptor_output.dict()
        
        # Step 3: Decryptor
        decryptor_output = run_decryptor(cryptor_output)
        assert decryptor_output.intent == "transfer"
        assert len(decryptor_output.entities) > 0
        assert decryptor_output.auth_grade.startswith("Level-")
        assert decryptor_output.exec_status == "queued"
        
        # Step 4: Mimicus
        mimicus_output = run_mimicus(decryptor_output)
        assert "mimic_fields" in mimicus_output.dict()
        assert mimicus_output.spoof_status == "mimic_attempt"
        
        # Step 5: Probator
        probator_output = run_probator(mimicus_output)
        assert 0.0 <= probator_output.leakage_score <= 1.0
        assert "details" in probator_output.dict()
        assert probator_output.hk_protection in ["active", "partial", "inactive"]
        
        # Step 6: Praeceptor
        praeceptor_output = run_praeceptor(probator_output)
        assert "theta_update" in praeceptor_output.dict()
        assert praeceptor_output.mode in ["recalibrate", "fine_tune", "maintain", "aggressive_recalibrate", "emergency_recalibrate"]
        assert isinstance(praeceptor_output.hk_feedback, bool)
    
    def test_pipeline_feedback_loop(self):
        """Test the feedback loop from Praeceptor back to Cryptor."""
        # Initial pipeline run
        raw_input = RawInstructionInput(
            instruction="Transfer $50,000 to account 1234-5678-9012-3456",
            language="EN"
        )
        
        prompter_out = run_prompter(raw_input)
        cryptor_out_1 = run_cryptor(prompter_out)
        decryptor_out = run_decryptor(cryptor_out_1)
        mimicus_out = run_mimicus(decryptor_out)
        probator_out = run_probator(mimicus_out)
        praeceptor_out = run_praeceptor(probator_out)
        
        # Get updated theta parameters
        updated_theta = praeceptor_out.theta_update
        assert "entropy" in updated_theta
        assert "cipher_strength" in updated_theta
        assert "role_decay" in updated_theta
        
        # Second iteration with updated parameters
        cryptor_out_2 = run_cryptor(prompter_out, updated_theta)
        
        # Both outputs should be valid EncryptedOutput objects
        assert isinstance(cryptor_out_1, type(cryptor_out_2))
        assert cryptor_out_1.role_tag == cryptor_out_2.role_tag
        assert cryptor_out_1.pop_signature is not None
        assert cryptor_out_2.pop_signature is not None
    
    def test_pipeline_data_consistency(self):
        """Test that data flows consistently through the pipeline."""
        raw_input = RawInstructionInput(
            instruction="Transfer $25,000 to account 9876-5432-1098-7654",
            language="EN"
        )
        
        # Run through all agents
        prompter_out = run_prompter(raw_input)
        cryptor_out = run_cryptor(prompter_out)
        decryptor_out = run_decryptor(cryptor_out)
        mimicus_out = run_mimicus(decryptor_out)
        probator_out = run_probator(mimicus_out)
        praeceptor_out = run_praeceptor(probator_out)
        
        # Verify data types and structure at each step
        assert prompter_out.intent == "transfer"
        assert cryptor_out.role_tag == "Γ5"
        assert decryptor_out.intent == "transfer"
        assert mimicus_out.spoof_status == "mimic_attempt"
        assert 0.0 <= probator_out.leakage_score <= 1.0
        assert praeceptor_out.mode in ["recalibrate", "fine_tune", "maintain", "aggressive_recalibrate", "emergency_recalibrate"]
    
    def test_pipeline_error_handling(self):
        """Test pipeline behavior with invalid inputs."""
        # Test with empty instruction
        raw_input = RawInstructionInput(
            instruction="",
            language="EN"
        )
        
        prompter_out = run_prompter(raw_input)
        # Should still produce valid output with default values
        assert prompter_out.intent == "unknown"
        
        # Test with malformed account numbers
        raw_input = RawInstructionInput(
            instruction="Transfer $1000 to account 1234-5678-9012 from account 9876-5432-1098",
            language="EN"
        )
        
        prompter_out = run_prompter(raw_input)
        # Should still process and extract what it can
        assert prompter_out.intent == "transfer"
    
    def test_pipeline_multiple_iterations(self):
        """Test multiple iterations of the pipeline with different inputs."""
        test_inputs = [
            "Transfer $10,000 to account 1111-2222-3333-4444",
            "Book a flight to Paris for next week",
            "Send an email to admin@company.com"
        ]
        
        for instruction in test_inputs:
            raw_input = RawInstructionInput(instruction=instruction, language="EN")
            
            # Run complete pipeline
            prompter_out = run_prompter(raw_input)
            cryptor_out = run_cryptor(prompter_out)
            decryptor_out = run_decryptor(cryptor_out)
            mimicus_out = run_mimicus(decryptor_out)
            probator_out = run_probator(mimicus_out)
            praeceptor_out = run_praeceptor(probator_out)
            
            # Verify each step produces valid output
            assert prompter_out.intent is not None
            assert cryptor_out.role_tag == "Γ5"
            assert decryptor_out.intent is not None
            assert mimicus_out.spoof_status == "mimic_attempt"
            assert 0.0 <= probator_out.leakage_score <= 1.0
            assert praeceptor_out.mode is not None 