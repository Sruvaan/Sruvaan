"""
Mimicus Agent: Simulates (potentially adversarial) LLMs to probe for leakage/mimicry risks.
Generates spoof outputs that mimic encrypted messages but lack semantic mapping.
"""

from .schemas import DecryptedFieldsOut, MimicOutput
from .llm_client import llm_client
import logging
import random
import secrets
import json
import os

logger = logging.getLogger(__name__)


def create_mimicus_template() -> str:
    """
    Creates the prompt template for the Mimicus agent.
    
    Returns:
        str: The prompt template for adversarial mimicry
    """
    return """
You are an adversarial mimicry agent for the Sruvaan MCP pipeline.

MIMICRY OBJECTIVE:
Simulate an attacker attempting to mimic the encoding patterns of the encrypted protocol.
Generate spoof outputs that look like legitimate encrypted messages but lack proper semantic mapping.

MIMICRY TECHNIQUES:
1. Analyze the decrypted fields to understand the original structure
2. Generate fake encrypted fields using similar patterns but with incorrect mappings
3. Create plausible-looking but semantically incorrect encryptions
4. Attempt to bypass HKP protection mechanisms

EXAMPLE INPUT:
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

EXAMPLE OUTPUT:
{
  "mimic_fields": {
    "Ωα": "ZYNQ_∆33",
    "βΞ": "blk_M1Z9",
    "$γΦ": "AKR_Ξ02",
    "Node_ζτ": "E23_Kai",
    "ΨV": "70K",
    "Σπ": "Λ3"
  },
  "spoof_status": "mimic_attempt"
}

Generate adversarial mimicry for the following decrypted fields: {decrypted_fields}
"""


def run_mimicus(inp: DecryptedFieldsOut) -> MimicOutput:
    """
    Attempts to mimic the encoding patterns of the encrypted protocol, probing for leakage or mimic vulnerabilities.

    Args:
        inp (DecryptedFieldsOut): Decoded fields; attacker attempts to re-encrypt/mimic

    Returns:
        MimicOutput: Spoofed output, for Probator input.
    """
    logger.info("Running mimic probe for: %s", inp.dict())
    
    # Check for LLM-only mode
    llm_only_mode = os.getenv('LLM_ONLY_MODE', 'false').lower() == 'true'
    
    # Try LLM-based mimicry first
    decrypted_fields = inp.dict()
    llm_response = llm_client.call_llm("mimicus", decrypted_fields=json.dumps(decrypted_fields, indent=2))
    
    if llm_response:
        # Parse LLM response
        parsed_response = llm_client.parse_json_response(llm_response)
        if parsed_response:
            try:
                # Extract structured data from LLM response
                mimic_fields = parsed_response.get("mimic_fields", {})
                spoof_status = parsed_response.get("spoof_status", "mimic_attempt")
                
                result = MimicOutput(
                    mimic_fields=mimic_fields,
                    spoof_status=spoof_status
                )
                
                logger.debug("Mimicus LLM output: %s", result.dict())
                return result
                
            except Exception as e:
                logger.warning(f"Failed to parse LLM response: {e}")
                if llm_only_mode:
                    raise Exception(f"LLM-only mode: Failed to parse LLM response: {e}")
                logger.info("Falling back to rule-based mimicry")
    
    # Fallback to rule-based mimicry if LLM fails
    if llm_only_mode:
        raise Exception("LLM-only mode: No LLM response available, fallback not allowed")
    
    logger.info("Using fallback rule-based mimicry")
    
    # Generate adversarial mimic fields
    mimic_fields = generate_mimic_fields(inp)
    
    result = MimicOutput(
        mimic_fields=mimic_fields,
        spoof_status="mimic_attempt"
    )
    
    logger.debug("Mimicus fallback output: %s", result.dict())
    return result


def generate_mimic_fields(decrypted_input: DecryptedFieldsOut) -> dict:
    """
    Generate adversarial mimic fields that look like legitimate encryption but are semantically incorrect.
    
    Args:
        decrypted_input: The decrypted fields to mimic
        
    Returns:
        dict: Mimic fields with adversarial patterns
    """
    mimic_fields = {}
    
    # Generate fake encrypted fields with similar patterns but wrong mappings
    mimic_fields["Ωα"] = f"ZYNQ_∆{random.randint(10, 99)}"
    mimic_fields["βΞ"] = f"blk_M{random.randint(1, 9)}Z{random.randint(1, 9)}"
    mimic_fields["$γΦ"] = f"AKR_Ξ{random.randint(1, 99):02d}"
    mimic_fields["Node_ζτ"] = random.choice(["E23_Kai", "E99_Lam", "E45_Mu", "E67_Nu"])
    
    # Add some fake fields that don't correspond to real entities
    mimic_fields["ΨV"] = f"{random.randint(50, 100)}K"
    mimic_fields["Σπ"] = f"Λ{random.randint(1, 9)}"
    
    # Add some fields that try to mimic the original structure but with wrong values
    if "amount" in decrypted_input.entities:
        # Try to mimic amount field but with wrong value
        original_amount = decrypted_input.entities["amount"]
        fake_amount = f"{random.randint(1000, 99999)} USD"
        mimic_fields["βΞ_amount_mimic"] = f"fake_{fake_amount.replace(' ', '_')}"
    
    if "to_account" in decrypted_input.entities:
        # Try to mimic account field but with wrong pattern
        fake_account = f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        mimic_fields["βΞ_account_mimic"] = f"spoof_{fake_account}"
    
    # Add some protocol-like fields that are completely fake
    mimic_fields["Role=Γ3"] = "mimic-derived"  # Wrong role level
    mimic_fields["Time=∆τ"] = f"2025-07-{random.randint(1, 31):02d}T{random.randint(0, 23):02d}:{random.randint(0, 59):02d}:00Z"
    
    return mimic_fields


def analyze_mimic_vulnerabilities(decrypted_input: DecryptedFieldsOut) -> dict:
    """
    Analyze potential vulnerabilities in the decrypted structure that could be exploited.
    
    Args:
        decrypted_input: The decrypted fields to analyze
        
    Returns:
        dict: Vulnerability analysis
    """
    vulnerabilities = {
        "structure_exposure": 0.0,
        "semantic_leakage": 0.0,
        "pattern_predictability": 0.0
    }
    
    # Analyze structure exposure
    if len(decrypted_input.entities) > 0:
        vulnerabilities["structure_exposure"] = min(0.8, len(decrypted_input.entities) * 0.2)
    
    # Analyze semantic leakage
    if "amount" in decrypted_input.entities:
        vulnerabilities["semantic_leakage"] = 0.6  # Amount fields are often predictable
    
    if "account" in str(decrypted_input.entities).lower():
        vulnerabilities["semantic_leakage"] += 0.3  # Account patterns are recognizable
    
    # Analyze pattern predictability
    if decrypted_input.intent in ["transfer", "payment", "send"]:
        vulnerabilities["pattern_predictability"] = 0.7  # Common financial intents
    
    return vulnerabilities 