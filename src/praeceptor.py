"""
Praeceptor Agent: Updates cryptographic/encryption policy θ based on observed leakage and mimic risk.
Receives feedback, generates next-iteration parameters.
"""

from .schemas import LeakageVectorOut, ThetaUpdate
from .llm_client import llm_client
import logging
import random
import math
import json
import os

logger = logging.getLogger(__name__)


def create_praeceptor_template() -> str:
    """
    Creates the prompt template for the Praeceptor agent.
    
    Returns:
        str: The prompt template for parameter calibration
    """
    return """
You are a parameter calibration agent for the Sruvaan MCP pipeline.

CALIBRATION OBJECTIVE:
Analyze leakage assessment results and adjust encryption parameters to improve security.
Implement feedback loops to optimize HKP protection against adversarial mimicry.

CALIBRATION PARAMETERS:
1. Entropy: Randomness in key derivation (0.0 to 1.0)
2. Cipher Strength: Overall encryption strength (0.0 to 1.0)
3. Role Decay: Rate of role-based key expiration (0.0 to 1.0)
4. HKP Feedback: Whether to update HKP-specific parameters

CALIBRATION LOGIC:
- High leakage score → Increase entropy and cipher strength
- Low HKP protection → Strengthen role-based and time-based constraints
- Pattern consistency in mimic → Adjust field mapping obfuscation
- Semantic drift analysis → Fine-tune semantic preservation vs. security

EXAMPLE INPUT:
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

EXAMPLE OUTPUT:
{
  "theta_update": {
    "entropy": 0.41,
    "cipher_strength": 0.8,
    "role_decay": 0.6
  },
  "mode": "recalibrate",
  "hk_feedback": true
}

Calibrate parameters based on the following leakage assessment: {leakage_assessment}
"""


def run_praeceptor(inp: LeakageVectorOut) -> ThetaUpdate:
    """
    Adjusts encryption parameters using feedback from Probator.

    Args:
        inp (LeakageVectorOut): Leakage metrics.

    Returns:
        ThetaUpdate: Dict with new recommended theta values.
    """
    logger.info("Praeceptor calibrating theta based on leakage_score=%.3f", inp.leakage_score)
    
    # Check for LLM-only mode
    llm_only_mode = os.getenv('LLM_ONLY_MODE', 'false').lower() == 'true'
    
    # Try LLM-based calibration first
    leakage_assessment = inp.dict()
    llm_response = llm_client.call_llm("praeceptor", leakage_assessment=json.dumps(leakage_assessment, indent=2))
    
    if llm_response:
        # Parse LLM response
        parsed_response = llm_client.parse_json_response(llm_response)
        if parsed_response:
            try:
                # Extract structured data from LLM response
                theta_update = parsed_response.get("theta_update", {})
                mode = parsed_response.get("mode", "recalibrate")
                hk_feedback = parsed_response.get("hk_feedback", True)
                
                result = ThetaUpdate(
                    theta_update=theta_update,
                    mode=mode,
                    hk_feedback=hk_feedback
                )
                
                logger.debug("Praeceptor LLM output: %s", result.dict())
                return result
                
            except Exception as e:
                logger.warning(f"Failed to parse LLM response: {e}")
                if llm_only_mode:
                    raise Exception(f"LLM-only mode: Failed to parse LLM response: {e}")
                logger.info("Falling back to rule-based calibration")
    
    # Fallback to rule-based calibration if LLM fails
    if llm_only_mode:
        raise Exception("LLM-only mode: No LLM response available, fallback not allowed")
    
    logger.info("Using fallback rule-based calibration")
    
    # Analyze current leakage and determine parameter adjustments
    theta_update = calibrate_parameters(inp)
    
    # Determine calibration mode based on leakage severity
    mode = determine_calibration_mode(inp.leakage_score)
    
    # Check if HKP feedback is needed
    hk_feedback = inp.hk_protection != "active"
    
    result = ThetaUpdate(
        theta_update=theta_update,
        mode=mode,
        hk_feedback=hk_feedback
    )
    
    logger.debug("Praeceptor fallback output: %s", result.dict())
    return result


def calibrate_parameters(leakage_assessment: LeakageVectorOut) -> dict:
    """
    Calibrate encryption parameters based on leakage assessment.
    
    Args:
        leakage_assessment: The leakage assessment results
        
    Returns:
        dict: Updated theta parameters
    """
    # Base parameters
    base_entropy = 0.5
    base_cipher_strength = 0.8
    base_role_decay = 0.5
    
    # Adjust based on leakage score
    leakage_score = leakage_assessment.leakage_score
    
    # High leakage requires stronger encryption
    if leakage_score > 0.5:
        entropy_adjustment = min(0.3, leakage_score * 0.4)
        cipher_adjustment = min(0.2, leakage_score * 0.3)
        role_decay_adjustment = min(0.3, leakage_score * 0.5)
    else:
        # Low leakage allows for some optimization
        entropy_adjustment = max(-0.1, (0.5 - leakage_score) * 0.2)
        cipher_adjustment = max(-0.1, (0.5 - leakage_score) * 0.15)
        role_decay_adjustment = max(-0.1, (0.5 - leakage_score) * 0.25)
    
    # Adjust based on specific leakage details
    details = leakage_assessment.details
    
    # Entity recovery affects entropy
    if details.get("entity_recovery", 0) > 0.3:
        entropy_adjustment += 0.1
    
    # Structure fidelity affects cipher strength
    if details.get("structure_fidelity", 0) > 0.5:
        cipher_adjustment += 0.1
    
    # Semantic drift affects role decay
    if details.get("semantic_drift", 0) < 0.4:  # Low drift means good protection
        role_decay_adjustment -= 0.1
    
    # Calculate final parameters with bounds
    new_entropy = max(0.1, min(1.0, base_entropy + entropy_adjustment))
    new_cipher_strength = max(0.3, min(1.0, base_cipher_strength + cipher_adjustment))
    new_role_decay = max(0.1, min(1.0, base_role_decay + role_decay_adjustment))
    
    return {
        "entropy": round(new_entropy, 3),
        "cipher_strength": round(new_cipher_strength, 3),
        "role_decay": round(new_role_decay, 3)
    }


def determine_calibration_mode(leakage_score: float) -> str:
    """
    Determine the calibration mode based on leakage severity.
    
    Args:
        leakage_score: The overall leakage score
        
    Returns:
        str: Calibration mode
    """
    if leakage_score > 0.7:
        return "emergency_recalibrate"
    elif leakage_score > 0.5:
        return "aggressive_recalibrate"
    elif leakage_score > 0.3:
        return "recalibrate"
    elif leakage_score > 0.1:
        return "fine_tune"
    else:
        return "maintain"


def analyze_hkp_effectiveness(leakage_assessment: LeakageVectorOut) -> dict:
    """
    Analyze the effectiveness of HKP protection.
    
    Args:
        leakage_assessment: The leakage assessment results
        
    Returns:
        dict: HKP effectiveness analysis
    """
    hkp_analysis = {
        "role_protection": "unknown",
        "time_protection": "unknown",
        "pop_effectiveness": "unknown",
        "overall_hkp_score": 0.0
    }
    
    # Analyze based on leakage details
    details = leakage_assessment.details
    
    # Role protection analysis
    if "pattern_consistency" in details and details["pattern_consistency"] < 0.5:
        hkp_analysis["role_protection"] = "strong"
    else:
        hkp_analysis["role_protection"] = "weak"
    
    # Time protection analysis
    if "structure_fidelity" in details and details["structure_fidelity"] < 0.6:
        hkp_analysis["time_protection"] = "strong"
    else:
        hkp_analysis["time_protection"] = "weak"
    
    # PoP effectiveness analysis
    if "field_mapping_accuracy" in details and details["field_mapping_accuracy"] < 0.3:
        hkp_analysis["pop_effectiveness"] = "strong"
    else:
        hkp_analysis["pop_effectiveness"] = "weak"
    
    # Calculate overall HKP score
    protection_scores = []
    if hkp_analysis["role_protection"] == "strong":
        protection_scores.append(1.0)
    else:
        protection_scores.append(0.0)
    
    if hkp_analysis["time_protection"] == "strong":
        protection_scores.append(1.0)
    else:
        protection_scores.append(0.0)
    
    if hkp_analysis["pop_effectiveness"] == "strong":
        protection_scores.append(1.0)
    else:
        protection_scores.append(0.0)
    
    hkp_analysis["overall_hkp_score"] = sum(protection_scores) / len(protection_scores)
    
    return hkp_analysis 