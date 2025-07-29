"""
Cryptor Agent: Applies Hierarchical Keyed Protocol (HKP) encryption to semantic fields from prompter.
Outputs an obfuscated, role-locked encrypted object.
"""

from .schemas import SemanticPromptOut, EncryptedOutput
from .llm_client import llm_client
from typing import Dict, Any
import logging
import hashlib
import datetime
import secrets
import json
import os

logger = logging.getLogger(__name__)


def create_cryptor_template() -> str:
    """
    Creates the prompt template for the Cryptor agent with HKP focus.
    
    Returns:
        str: The prompt template for HKP encryption
    """
    return """
You are a Hierarchical Keyed Protocol (HKP) encryption agent for the Sruvaan MCP pipeline.

HIERARCHICAL KEYED PROTOCOL (HKP) REQUIREMENTS:
1. Derive role-scoped keys (Role=Γ5 for high-privilege operations)
2. Embed time-based constraints (Time=∆τ) for epoch-based access control
3. Generate Proof-of-Protocol (PoP) signatures for integrity
4. Apply field-wise encryption with hierarchical key derivation

ENCRYPTION PROCESS:
1. Parse the semantic fields from the prompter
2. Apply HKP encryption to each field with role and time constraints
3. Generate a PoP signature from the encrypted payload
4. Return the encrypted output with protocol metadata

EXAMPLE INPUT:
{
  "intent": "transfer",
  "entities": {
    "amount": "75000 USD",
    "to_account": "7395-8845-2291",
    "from_account": "1559-6623-4401"
  }
}

EXAMPLE OUTPUT:
{
  "encrypted_fields": {
    "Ωα": "DYNX_Ω47",
    "βΞ": "blk_Z9X5", 
    "$γΦ": "BXR_Λ03",
    "Node_ζτ": "E13_Tau",
    "Role=Γ5": "HKP-derived",
    "Time=∆τ": "2025-07-29T10:30:00Z"
  },
  "role_tag": "Γ5",
  "pop_signature": "abc123def456",
  "time_tag": "2025-07-29T10:30:00Z"
}

Encrypt the following semantic fields using HKP: {semantic_fields}
"""


def run_cryptor(inp: SemanticPromptOut, theta_params: Dict[str, float] = None) -> EncryptedOutput:
    """
    Hierarchically encrypts parsed prompt fields, outputting a cipher object with protocol-mandated fields.
    Implements role-locked encryption and attaches Proof-of-Protocol tags.

    Args:
        inp (SemanticPromptOut): Structured fields (intent, entities, auth_level, timestamp, etc.)
        theta_params (optional): Encryption policies/config (from Praeceptor feedback).

    Returns:
        EncryptedOutput: Dict with fieldwise encryption, plus PoP and meta fields.
    """
    logger.info("Encrypting prompt: %s", inp.dict())
    
    # Check for LLM-only mode
    llm_only_mode = os.getenv('LLM_ONLY_MODE', 'false').lower() == 'true'
    
    # Try LLM-based encryption first
    semantic_fields = inp.dict()
    llm_response = llm_client.call_llm("cryptor", semantic_fields=json.dumps(semantic_fields, indent=2))
    
    if llm_response:
        # Parse LLM response
        parsed_response = llm_client.parse_json_response(llm_response)
        if parsed_response:
            try:
                # Extract structured data from LLM response
                encrypted_fields = parsed_response.get("encrypted_fields", {})
                role_tag = parsed_response.get("role_tag", "Γ5")
                pop_signature = parsed_response.get("pop_signature", "")
                time_tag = parsed_response.get("time_tag", datetime.datetime.utcnow().isoformat())
                
                encrypted = EncryptedOutput(
                    encrypted_fields=encrypted_fields,
                    role_tag=role_tag,
                    pop_signature=pop_signature,
                    time_tag=time_tag
                )
                
                logger.debug("Cryptor LLM output: %s", encrypted.dict())
                return encrypted
                
            except Exception as e:
                logger.warning(f"Failed to parse LLM response: {e}")
                if llm_only_mode:
                    raise Exception(f"LLM-only mode: Failed to parse LLM response: {e}")
                logger.info("Falling back to rule-based encryption")
    
    # Fallback to rule-based encryption if LLM fails
    if llm_only_mode:
        raise Exception("LLM-only mode: No LLM response available, fallback not allowed")
    
    logger.info("Using fallback rule-based encryption")
    
    # Generate time tag for epoch-based access control
    time_tag = datetime.datetime.utcnow().isoformat()
    
    # Apply HKP encryption to fields
    encrypted_fields = apply_hkp_encryption(inp, theta_params)
    
    # Add protocol metadata
    encrypted_fields.update({
        "Role=Γ5": "HKP-derived",
        "Time=∆τ": time_tag,
    })
    
    # Generate Proof-of-Protocol signature
    pop_signature = generate_pop_signature(encrypted_fields)
    
    encrypted = EncryptedOutput(
        encrypted_fields=encrypted_fields,
        role_tag="Γ5",
        pop_signature=pop_signature,
        time_tag=time_tag
    )
    
    logger.debug("Cryptor fallback output: %s", encrypted.dict())
    return encrypted


def apply_hkp_encryption(semantic_input: SemanticPromptOut, theta_params: Dict[str, float] = None) -> Dict[str, Any]:
    """
    Apply Hierarchical Keyed Protocol encryption to semantic fields.
    
    Args:
        semantic_input: The structured semantic input
        theta_params: Optional encryption parameters from feedback loop
        
    Returns:
        Dict of encrypted field mappings
    """
    # Default encryption parameters
    if theta_params is None:
        theta_params = {
            "entropy": 0.5,
            "cipher_strength": 0.8,
            "role_decay": 0.5
        }
    
    encrypted_fields = {}
    
    # Encrypt intent with role-based key
    intent_key = derive_role_key("intent", semantic_input.auth_level, theta_params)
    encrypted_fields["Ωα"] = encrypt_field(semantic_input.intent, intent_key)
    
    # Encrypt entities with hierarchical keys
    for entity_key, entity_value in semantic_input.entities.items():
        field_key = derive_role_key(entity_key, semantic_input.auth_level, theta_params)
        encrypted_fields[f"βΞ_{entity_key}"] = encrypt_field(entity_value, field_key)
    
    # Add additional protocol fields
    encrypted_fields["$γΦ"] = f"BXR_Λ{secrets.randbelow(100):02d}"
    encrypted_fields["Node_ζτ"] = f"E{secrets.randbelow(100):02d}_Tau"
    
    return encrypted_fields


def derive_role_key(field_name: str, auth_level: str, theta_params: Dict[str, float]) -> str:
    """
    Derive a role-scoped key for a specific field.
    
    Args:
        field_name: Name of the field to encrypt
        auth_level: Authentication level (L1-L5)
        theta_params: Encryption parameters
        
    Returns:
        Derived key string
    """
    # Create a deterministic but role-scoped key
    base = f"{field_name}_{auth_level}_{theta_params.get('cipher_strength', 0.8)}"
    key_hash = hashlib.sha256(base.encode()).hexdigest()[:8]
    return f"HKP_{key_hash}"


def encrypt_field(value: str, key: str) -> str:
    """
    Encrypt a field value using the provided key.
    
    Args:
        value: The value to encrypt
        key: The encryption key
        
    Returns:
        Encrypted field value
    """
    # Simple encryption for demo - in production, use proper cryptographic libraries
    combined = f"{value}_{key}"
    encrypted = hashlib.sha256(combined.encode()).hexdigest()[:12]
    
    # Generate a random prefix for obfuscation
    prefix = secrets.token_hex(2).upper()
    return f"{prefix}_{encrypted}"


def generate_pop_signature(encrypted_fields: Dict[str, Any]) -> str:
    """
    Generate Proof-of-Protocol signature from encrypted fields.
    
    Args:
        encrypted_fields: The encrypted field dictionary
        
    Returns:
        PoP signature string
    """
    # Create a deterministic payload from encrypted fields
    payload = json.dumps(encrypted_fields, sort_keys=True)
    signature = hashlib.sha256(payload.encode()).hexdigest()[:12]
    return signature 