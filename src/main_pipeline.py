"""
Main Pipeline: Orchestrates the 6-agent MCP pipeline end-to-end.
Implements the complete flow from raw instruction to parameter calibration.
"""

from .schemas import RawInstructionInput
from .prompter import run_prompter
from .cryptor import run_cryptor
from .decryptor import run_decryptor
from .mimicus import run_mimicus
from .probator import run_probator
from .praeceptor import run_praeceptor
import logging
import json
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_pipeline_demo():
    """
    Run a complete demo of the 6-agent MCP pipeline.
    """
    logger.info("Starting Sruvaan MCP Pipeline Demo")
    
    # Sample input from protocol spec
    raw_input = RawInstructionInput(
        instruction="Transfer $75,000 to account 7395-8845-2291 from account 1559-6623-4401",
        language="EN"
    )
    
    logger.info("=== PIPELINE EXECUTION ===")
    
    # Agent 1: Prompter
    logger.info("1. Prompter Agent")
    prompter_output = run_prompter(raw_input)
    logger.info(f"   Input: {raw_input.instruction}")
    logger.info(f"   Output: {prompter_output.dict()}")
    
    # Agent 2: Cryptor (HKP Encryption)
    logger.info("2. Cryptor Agent (HKP Encryption)")
    cryptor_output = run_cryptor(prompter_output)
    logger.info(f"   Input: {prompter_output.dict()}")
    logger.info(f"   Output: {cryptor_output.dict()}")
    
    # Agent 3: Decryptor
    logger.info("3. Decryptor Agent")
    decryptor_output = run_decryptor(cryptor_output)
    logger.info(f"   Input: {cryptor_output.dict()}")
    logger.info(f"   Output: {decryptor_output.dict()}")
    
    # Agent 4: Mimicus
    logger.info("4. Mimicus Agent (Adversarial Mimicry)")
    mimicus_output = run_mimicus(decryptor_output)
    logger.info(f"   Input: {decryptor_output.dict()}")
    logger.info(f"   Output: {mimicus_output.dict()}")
    
    # Agent 5: Probator
    logger.info("5. Probator Agent (Leakage Assessment)")
    probator_output = run_probator(mimicus_output)
    logger.info(f"   Input: {mimicus_output.dict()}")
    logger.info(f"   Output: {probator_output.dict()}")
    
    # Agent 6: Praeceptor
    logger.info("6. Praeceptor Agent (Parameter Calibration)")
    praeceptor_output = run_praeceptor(probator_output)
    logger.info(f"   Input: {probator_output.dict()}")
    logger.info(f"   Output: {praeceptor_output.dict()}")
    
    logger.info("=== PIPELINE COMPLETE ===")
    logger.info(f"Final Theta Update: {praeceptor_output.dict()}")
    
    return praeceptor_output


def run_pipeline_with_feedback(initial_theta: Dict[str, float] = None):
    """
    Run the pipeline with feedback loop from Praeceptor to Cryptor.
    
    Args:
        initial_theta: Initial theta parameters for Cryptor
    """
    logger.info("Starting Sruvaan MCP Pipeline with Feedback Loop")
    
    # Sample input
    raw_input = RawInstructionInput(
        instruction="Transfer $50,000 to account 1234-5678-9012-3456 from account 9876-5432-1098-7654",
        language="EN"
    )
    
    # Initial theta parameters
    if initial_theta is None:
        initial_theta = {
            "entropy": 0.5,
            "cipher_strength": 0.8,
            "role_decay": 0.5
        }
    
    logger.info(f"Initial Theta Parameters: {initial_theta}")
    
    # First iteration
    logger.info("=== ITERATION 1 ===")
    prompter_out = run_prompter(raw_input)
    cryptor_out = run_cryptor(prompter_out, initial_theta)
    decryptor_out = run_decryptor(cryptor_out)
    mimicus_out = run_mimicus(decryptor_out)
    probator_out = run_probator(mimicus_out)
    praeceptor_out = run_praeceptor(probator_out)
    
    # Feedback loop: use updated theta for second iteration
    updated_theta = praeceptor_out.theta_update
    logger.info(f"Updated Theta Parameters: {updated_theta}")
    
    # Second iteration with updated parameters
    logger.info("=== ITERATION 2 (with feedback) ===")
    cryptor_out_2 = run_cryptor(prompter_out, updated_theta)
    decryptor_out_2 = run_decryptor(cryptor_out_2)
    mimicus_out_2 = run_mimicus(decryptor_out_2)
    probator_out_2 = run_probator(mimicus_out_2)
    praeceptor_out_2 = run_praeceptor(probator_out_2)
    
    logger.info("=== FEEDBACK LOOP COMPLETE ===")
    logger.info(f"Final Theta Update: {praeceptor_out_2.dict()}")
    
    return praeceptor_out_2


def print_pipeline_summary():
    """
    Print a summary of the pipeline architecture.
    """
    print("\n" + "="*60)
    print("SRUVAAN MCP PIPELINE - 6-AGENT ARCHITECTURE")
    print("="*60)
    print("Agent 1: Prompter")
    print("  - Parses raw user instructions into structured semantic fields")
    print("  - Extracts intent and entities using NLU/LLM")
    print("  - Output: SemanticPromptOut with intent and entities")
    print()
    print("Agent 2: Cryptor (HKP Encryption)")
    print("  - Applies Hierarchical Keyed Protocol (HKP) encryption")
    print("  - Derives role-scoped and time-scoped keys")
    print("  - Generates Proof-of-Protocol (PoP) signatures")
    print("  - Output: EncryptedOutput with HKP fields")
    print()
    print("Agent 3: Decryptor")
    print("  - Reverses HKP encryption using role-based keys")
    print("  - Validates PoP signatures for integrity")
    print("  - Reconstructs original semantic fields")
    print("  - Output: DecryptedFieldsOut for audit/execution")
    print()
    print("Agent 4: Mimicus (Adversarial)")
    print("  - Simulates attacker attempting to mimic encryption patterns")
    print("  - Generates spoof outputs that look legitimate but lack semantic mapping")
    print("  - Probes for leakage and mimicry vulnerabilities")
    print("  - Output: MimicOutput for security testing")
    print()
    print("Agent 5: Probator")
    print("  - Analyzes mimic fields for semantic leakage")
    print("  - Quantifies decipherability and risk metrics")
    print("  - Assesses HKP protection effectiveness")
    print("  - Output: LeakageVectorOut with risk scores")
    print()
    print("Agent 6: Praeceptor")
    print("  - Calibrates encryption parameters based on leakage assessment")
    print("  - Implements feedback loop to Cryptor")
    print("  - Optimizes HKP protection against adversarial mimicry")
    print("  - Output: ThetaUpdate for parameter adjustment")
    print()
    print("FEEDBACK LOOP: Praeceptor → Cryptor")
    print("  - Theta parameters flow back to improve encryption")
    print("  - Continuous optimization of security vs. usability")
    print("="*60)


def main():
    """
    Main entry point for the pipeline demo.
    """
    print_pipeline_summary()
    
    # Run the basic pipeline demo
    print("\nRunning Pipeline Demo...")
    final_result = run_pipeline_demo()
    
    # Run the feedback loop demo
    print("\nRunning Feedback Loop Demo...")
    feedback_result = run_pipeline_with_feedback()
    
    print("\n" + "="*60)
    print("DEMO COMPLETE")
    print("="*60)
    print(f"Basic Pipeline Result: {final_result.dict()}")
    print(f"Feedback Loop Result: {feedback_result.dict()}")
    print("="*60)


if __name__ == "__main__":
    main() 