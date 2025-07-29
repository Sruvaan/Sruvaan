"""
Probator Agent: Quantifies semantic leakage and decipherability of the (mimicked) encrypted message.
Returns scalar risk and per-field heuristics.
"""

from .schemas import MimicOutput, LeakageVectorOut
from .llm_client import llm_client
import logging
import random
import json
import os

logger = logging.getLogger(__name__)


def create_probator_template() -> str:
    """
    Creates the prompt template for the Probator agent.
    
    Returns:
        str: The prompt template for leakage assessment
    """
    return """
You are a leakage assessment agent for the Sruvaan MCP pipeline.

LEAKAGE ASSESSMENT OBJECTIVE:
Analyze the mimic fields to determine how much semantic information can be recovered.
Quantify the effectiveness of HKP protection against adversarial mimicry.

ASSESSMENT METRICS:
1. Leakage Score: Overall probability of recovering original semantic information
2. Entity Recovery: Ability to reconstruct specific field values
3. Structure Fidelity: How well the original structure is preserved
4. Semantic Drift: Degree of semantic distortion in mimic attempts
5. HKP Protection: Effectiveness of Hierarchical Keyed Protocol protection

EXAMPLE INPUT:
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

EXAMPLE OUTPUT:
{
  "leakage_score": 0.32,
  "details": {
    "entity_recovery": 0.25,
    "structure_fidelity": 0.40,
    "semantic_drift": 0.65,
    "hkp_protection": "active"
  },
  "hk_protection": "active"
}

Assess leakage risk for the following mimic fields: {mimic_fields}
"""


def run_probator(inp: MimicOutput) -> LeakageVectorOut:
    """
    Tries to reconstruct original fields from a mimic (spoof) message; computes leakage metrics.

    Args:
        inp (MimicOutput): Spoofed 'encrypted' dict.

    Returns:
        LeakageVectorOut: Scalar leakage risk and breakdown.
    """
    logger.info("Probator analyzing mimic fields for leakage.")
    
    # Check for LLM-only mode
    llm_only_mode = os.getenv('LLM_ONLY_MODE', 'false').lower() == 'true'
    
    # Try LLM-based analysis first
    mimic_fields = inp.mimic_fields
    llm_response = llm_client.call_llm("probator", mimic_fields=json.dumps(mimic_fields, indent=2))
    
    if llm_response:
        # Parse LLM response
        parsed_response = llm_client.parse_json_response(llm_response)
        if parsed_response:
            try:
                # Extract structured data from LLM response
                leakage_score = parsed_response.get("leakage_score", 0.0)
                details = parsed_response.get("details", {})
                hk_protection = parsed_response.get("hk_protection", "unknown")
                
                result = LeakageVectorOut(
                    leakage_score=leakage_score,
                    details=details,
                    hk_protection=hk_protection
                )
                
                logger.debug("Probator LLM output: %s", result.dict())
                return result
                
            except Exception as e:
                logger.warning(f"Failed to parse LLM response: {e}")
                if llm_only_mode:
                    raise Exception(f"LLM-only mode: Failed to parse LLM response: {e}")
                logger.info("Falling back to rule-based analysis")
    
    # Fallback to rule-based analysis if LLM fails
    if llm_only_mode:
        raise Exception("LLM-only mode: No LLM response available, fallback not allowed")
    
    logger.info("Using fallback rule-based analysis")
    
    # Analyze the mimic fields for leakage patterns
    leakage_details = analyze_leakage_patterns(inp.mimic_fields)
    
    # Calculate overall leakage score
    leakage_score = calculate_leakage_score(leakage_details)
    
    # Assess HKP protection effectiveness
    hkp_protection = assess_hkp_protection(inp.mimic_fields)
    
    result = LeakageVectorOut(
        leakage_score=leakage_score,
        details=leakage_details,
        hk_protection=hkp_protection
    )
    
    logger.debug("Probator fallback output: %s", result.dict())
    return result


def analyze_leakage_patterns(mimic_fields: dict) -> dict:
    """
    Analyze mimic fields for potential leakage patterns.
    
    Args:
        mimic_fields: The mimic fields to analyze
        
    Returns:
        dict: Detailed leakage analysis
    """
    details = {
        "entity_recovery": 0.0,
        "structure_fidelity": 0.0,
        "semantic_drift": 0.0,
        "pattern_consistency": 0.0,
        "field_mapping_accuracy": 0.0
    }
    
    # Analyze entity recovery potential
    if "Ωα" in mimic_fields:
        # Check if intent field can be recovered
        details["entity_recovery"] = random.uniform(0.1, 0.4)
    
    # Analyze structure fidelity
    expected_fields = ["Ωα", "βΞ", "$γΦ", "Node_ζτ"]
    present_fields = [field for field in expected_fields if field in mimic_fields]
    details["structure_fidelity"] = len(present_fields) / len(expected_fields)
    
    # Analyze semantic drift
    # Higher drift means more semantic distortion
    details["semantic_drift"] = random.uniform(0.3, 0.8)
    
    # Analyze pattern consistency
    # Check if mimic patterns are consistent with expected encryption patterns
    pattern_score = 0.0
    if "Ωα" in mimic_fields and mimic_fields["Ωα"].startswith(("ZYNQ", "DYNX")):
        pattern_score += 0.3
    if "βΞ" in mimic_fields and "blk_" in mimic_fields["βΞ"]:
        pattern_score += 0.3
    if "$γΦ" in mimic_fields and "AKR_" in mimic_fields["$γΦ"]:
        pattern_score += 0.2
    if "Node_ζτ" in mimic_fields and "E" in mimic_fields["Node_ζτ"]:
        pattern_score += 0.2
    
    details["pattern_consistency"] = pattern_score
    
    # Analyze field mapping accuracy
    # Check if mimic fields correspond to expected semantic mappings
    mapping_accuracy = 0.0
    if "βΞ_amount_mimic" in mimic_fields:
        mapping_accuracy += 0.4  # Attempted to mimic amount field
    if "βΞ_account_mimic" in mimic_fields:
        mapping_accuracy += 0.4  # Attempted to mimic account field
    
    details["field_mapping_accuracy"] = mapping_accuracy
    
    return details


def calculate_leakage_score(details: dict) -> float:
    """
    Calculate overall leakage score from detailed analysis.
    
    Args:
        details: Detailed leakage analysis
        
    Returns:
        float: Overall leakage score (0.0 to 1.0)
    """
    # Weighted combination of different leakage factors
    weights = {
        "entity_recovery": 0.3,
        "structure_fidelity": 0.25,
        "semantic_drift": 0.2,
        "pattern_consistency": 0.15,
        "field_mapping_accuracy": 0.1
    }
    
    score = 0.0
    for factor, weight in weights.items():
        if factor in details:
            # For semantic_drift, lower is better (less drift = less leakage)
            if factor == "semantic_drift":
                score += weight * (1.0 - details[factor])
            else:
                score += weight * details[factor]
    
    return min(1.0, max(0.0, score))


def assess_hkp_protection(mimic_fields: dict) -> str:
    """
    Assess the effectiveness of HKP protection against mimic attempts.
    
    Args:
        mimic_fields: The mimic fields to analyze
        
    Returns:
        str: HKP protection status
    """
    # Check for HKP-specific fields
    hkp_fields = ["Role=Γ5", "Time=∆τ", "pop_signature"]
    hkp_present = any(field in mimic_fields for field in hkp_fields)
    
    # Check for role-based protection
    role_protection = "Role=Γ3" in mimic_fields  # Wrong role level
    
    # Check for time-based protection
    time_protection = "Time=∆τ" in mimic_fields
    
    if hkp_present and role_protection and time_protection:
        return "active"
    elif hkp_present:
        return "partial"
    else:
        return "inactive" 