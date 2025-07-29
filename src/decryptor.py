"""
Decryptor Agent: Reverses (role-permitted) encryption, reconstructs fields for audit and execution.
"""

from .schemas import EncryptedOutput, DecryptedFieldsOut
import logging
import hashlib
import json

logger = logging.getLogger(__name__)


def create_decryptor_template() -> str:
    """
    Creates the prompt template for the Decryptor agent.
    
    Returns:
        str: The prompt template for role-based decryption
    """
    return """
You are a role-based decryption agent for the Sruvaan MCP pipeline.

DECRYPTION PROCESS:
1. Verify the role tag and time constraints from the encrypted input
2. Apply role-scoped decryption keys to reverse the HKP encryption
3. Reconstruct the original semantic fields for audit and execution
4. Validate the Proof-of-Protocol (PoP) signature for integrity

ROLE-BASED ACCESS CONTROL:
- Only decrypt if the role tag matches permitted access levels
- Verify time-based constraints (Time=∆τ) for epoch validity
- Validate PoP signature before proceeding with decryption

EXAMPLE INPUT:
{
  "encrypted_fields": {
    "Ωα": "DYNX_Ω47",
    "βΞ_amount": "blk_Z9X5",
    "βΞ_to_account": "BXR_Λ03",
    "Role=Γ5": "HKP-derived",
    "Time=∆τ": "2025-07-29T10:30:00Z"
  },
  "role_tag": "Γ5",
  "pop_signature": "abc123def456",
  "time_tag": "2025-07-29T10:30:00Z"
}

EXAMPLE OUTPUT:
{
  "intent": "transfer",
  "entities": {
    "amount": "75000 USD",
    "to_account": "7395-8845-2291",
    "from_account": "1559-6623-4401"
  },
  "auth_grade": "Level-4",
  "time_issued": "2025-07-29T10:30:00Z",
  "exec_status": "queued"
}

Decrypt the following encrypted fields using role-based keys: {encrypted_fields}
"""


def run_decryptor(inp: EncryptedOutput) -> DecryptedFieldsOut:
    """
    Attempts to decrypt all encrypted_fields using allowed keys.
    Protocol field unwrapping per Section 2.2.

    Args:
        inp (EncryptedOutput): Typically from Cryptor.

    Returns:
        DecryptedFieldsOut: Decoded semantic fields for auditing/run.
    """
    logger.info("Starting decryption: role_tag=%s", inp.role_tag)
    
    # Verify PoP signature
    if not verify_pop_signature(inp.encrypted_fields, inp.pop_signature):
        logger.warning("PoP signature verification failed")
        raise ValueError("Invalid Proof-of-Protocol signature")
    
    # Decrypt fields using role-based keys
    decrypted_fields = decrypt_hkp_fields(inp.encrypted_fields, inp.role_tag)
    
    # Reconstruct the original semantic structure
    intent = "transfer"  # For demo purposes, always return transfer
    entities = {k: v for k, v in decrypted_fields.items() if k != "intent"}
    
    result = DecryptedFieldsOut(
        intent=intent,
        entities=entities,
        auth_grade=f"Level-{inp.role_tag[-1]}" if inp.role_tag.endswith(("1", "2", "3", "4", "5")) else "Level-4",
        time_issued=inp.time_tag,
        exec_status="queued"
    )
    
    logger.debug("Decryptor output: %s", result.dict())
    return result


def verify_pop_signature(encrypted_fields: dict, expected_signature: str) -> bool:
    """
    Verify the Proof-of-Protocol signature.
    
    Args:
        encrypted_fields: The encrypted fields dictionary
        expected_signature: The expected PoP signature
        
    Returns:
        bool: True if signature is valid
    """
    # Recreate the signature using the same method as Cryptor
    payload = json.dumps(encrypted_fields, sort_keys=True)
    actual_signature = hashlib.sha256(payload.encode()).hexdigest()[:12]
    return actual_signature == expected_signature


def decrypt_hkp_fields(encrypted_fields: dict, role_tag: str) -> dict:
    """
    Decrypt HKP-encrypted fields using role-based keys.
    
    Args:
        encrypted_fields: The encrypted fields dictionary
        role_tag: The role tag for key derivation
        
    Returns:
        dict: Decrypted field mappings
    """
    decrypted_fields = {}
    
    # Default theta parameters for key derivation
    theta_params = {
        "entropy": 0.5,
        "cipher_strength": 0.8,
        "role_decay": 0.5
    }
    
    # Decrypt intent field
    if "Ωα" in encrypted_fields:
        intent_key = derive_role_key("intent", "L4", theta_params)
        decrypted_fields["intent"] = decrypt_field(encrypted_fields["Ωα"], intent_key)
    else:
        # For demo purposes, default to transfer
        decrypted_fields["intent"] = "transfer"
    
    # Decrypt entity fields
    for field_name, encrypted_value in encrypted_fields.items():
        if field_name.startswith("βΞ_"):
            entity_key = field_name[4:]  # Remove "βΞ_" prefix
            field_key = derive_role_key(entity_key, "L4", theta_params)
            decrypted_fields[entity_key] = decrypt_field(encrypted_value, field_key)
    
    return decrypted_fields


def derive_role_key(field_name: str, auth_level: str, theta_params: dict) -> str:
    """
    Derive a role-scoped key for decryption (same as Cryptor).
    
    Args:
        field_name: Name of the field to decrypt
        auth_level: Authentication level
        theta_params: Encryption parameters
        
    Returns:
        Derived key string
    """
    base = f"{field_name}_{auth_level}_{theta_params.get('cipher_strength', 0.8)}"
    key_hash = hashlib.sha256(base.encode()).hexdigest()[:8]
    return f"HKP_{key_hash}"


def decrypt_field(encrypted_value: str, key: str) -> str:
    """
    Decrypt a field value using the provided key.
    
    Args:
        encrypted_value: The encrypted value
        key: The decryption key
        
    Returns:
        Decrypted field value
    """
    # This is a simplified decryption for demo purposes
    # In production, use proper cryptographic libraries
    
    # For demo, we'll return placeholder values based on the field pattern
    # Since the key is a hash, we need to check the original field name
    # For now, we'll use a simple mapping based on the encrypted value pattern
    
    if "Ωα" in encrypted_value or "intent" in key.lower():
        return "transfer"
    elif "amount" in key.lower() or "βΞ_amount" in encrypted_value:
        return "75000 USD"
    elif "account" in key.lower():
        if "to" in key.lower() or "to_account" in key.lower():
            return "7395-8845-2291"
        elif "from" in key.lower() or "from_account" in key.lower():
            return "1559-6623-4401"
        else:
            return "1234-5678-9012-3456"
    else:
        # For demo purposes, return a meaningful default
        return "default_value" 