"""
Unit tests for the Cryptor agent with HKP encryption.
"""

import pytest
from src.schemas import SemanticPromptOut, EncryptedOutput
from src.cryptor import (
    run_cryptor, 
    apply_hkp_encryption, 
    derive_role_key, 
    encrypt_field, 
    generate_pop_signature
)


class TestCryptor:
    """Test cases for the Cryptor agent."""
    
    def test_run_cryptor_basic(self):
        """Test basic cryptor functionality."""
        input_data = SemanticPromptOut(
            intent="transfer",
            entities={
                "amount": "75000 USD",
                "to_account": "7395-8845-2291",
                "from_account": "1559-6623-4401"
            },
            auth_level="L4",
            status="ready"
        )
        
        result = run_cryptor(input_data)
        
        assert isinstance(result, EncryptedOutput)
        assert "encrypted_fields" in result.dict()
        assert result.role_tag == "Γ5"
        assert result.pop_signature is not None
        assert result.time_tag is not None
    
    def test_hkp_encryption(self):
        """Test HKP encryption functionality."""
        input_data = SemanticPromptOut(
            intent="transfer",
            entities={
                "amount": "50000 USD",
                "to_account": "1234-5678-9012-3456"
            },
            auth_level="L4"
        )
        
        encrypted_fields = apply_hkp_encryption(input_data)
        
        # Check for HKP-specific fields
        assert "Ωα" in encrypted_fields  # Intent field
        assert "$γΦ" in encrypted_fields  # Protocol field
        assert "Node_ζτ" in encrypted_fields  # Protocol field
        
        # Check for entity-specific fields
        entity_fields = [field for field in encrypted_fields.keys() if field.startswith("βΞ_")]
        assert len(entity_fields) > 0
    
    def test_derive_role_key(self):
        """Test role key derivation."""
        field_name = "amount"
        auth_level = "L4"
        theta_params = {"cipher_strength": 0.8}
        
        key = derive_role_key(field_name, auth_level, theta_params)
        
        assert key.startswith("HKP_")
        assert len(key) > 4
    
    def test_encrypt_field(self):
        """Test field encryption."""
        value = "75000 USD"
        key = "HKP_12345678"
        
        encrypted = encrypt_field(value, key)
        
        assert encrypted is not None
        assert len(encrypted) > 0
        assert "_" in encrypted  # Should have prefix format
    
    def test_generate_pop_signature(self):
        """Test Proof-of-Protocol signature generation."""
        encrypted_fields = {
            "Ωα": "DYNX_Ω47",
            "βΞ": "blk_Z9X5",
            "$γΦ": "BXR_Λ03",
            "Node_ζτ": "E13_Tau"
        }
        
        signature = generate_pop_signature(encrypted_fields)
        
        assert signature is not None
        assert len(signature) == 12  # 12-character hex signature
    
    def test_cryptor_with_theta_params(self):
        """Test cryptor with theta parameters."""
        input_data = SemanticPromptOut(
            intent="transfer",
            entities={"amount": "10000 USD"},
            auth_level="L4"
        )
        
        theta_params = {
            "entropy": 0.7,
            "cipher_strength": 0.9,
            "role_decay": 0.6
        }
        
        result = run_cryptor(input_data, theta_params)
        
        assert isinstance(result, EncryptedOutput)
        assert result.role_tag == "Γ5"
    
    def test_hkp_protocol_fields(self):
        """Test that HKP protocol fields are properly included."""
        input_data = SemanticPromptOut(
            intent="transfer",
            entities={"amount": "25000 USD"},
            auth_level="L4"
        )
        
        result = run_cryptor(input_data)
        encrypted_fields = result.encrypted_fields
        
        # Check for HKP-specific protocol fields
        assert "Role=Γ5" in encrypted_fields
        assert "Time=∆τ" in encrypted_fields
        assert encrypted_fields["Role=Γ5"] == "HKP-derived"
    
    def test_cryptor_deterministic_keys(self):
        """Test that same inputs produce consistent key derivation."""
        field_name = "amount"
        auth_level = "L4"
        theta_params = {"cipher_strength": 0.8}
        
        key1 = derive_role_key(field_name, auth_level, theta_params)
        key2 = derive_role_key(field_name, auth_level, theta_params)
        
        assert key1 == key2  # Should be deterministic
    
    def test_cryptor_with_different_auth_levels(self):
        """Test cryptor with different authentication levels."""
        input_data = SemanticPromptOut(
            intent="transfer",
            entities={"amount": "15000 USD"},
            auth_level="L3"
        )
        
        result = run_cryptor(input_data)
        
        assert isinstance(result, EncryptedOutput)
        # Should still use Γ5 role tag for high-privilege operations
        assert result.role_tag == "Γ5" 