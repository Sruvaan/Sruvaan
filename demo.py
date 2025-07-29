#!/usr/bin/env python3
"""
Sruvaan MCP Pipeline Demo Script
Demonstrates the 6-agent pipeline with HKP encryption and feedback loops.
"""

import sys
import os
import argparse

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.schemas import RawInstructionInput
from src.main_pipeline import run_pipeline_demo, run_pipeline_with_feedback


def main():
    """Run the Sruvaan MCP Pipeline demo."""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Sruvaan MCP Pipeline Demo')
    parser.add_argument('--llm-only', action='store_true', 
                       help='Force LLM-only mode (no fallbacks allowed)')
    parser.add_argument('--openai-only', action='store_true',
                       help='Use only OpenAI API (no Anthropic)')
    args = parser.parse_args()
    
    # Set environment variables for LLM-only mode
    if args.llm_only:
        os.environ['LLM_ONLY_MODE'] = 'true'
        print("🚀 LLM-ONLY MODE ENABLED - No fallbacks allowed!")
        print("⚠️  This mode requires valid API keys to work.")
        print()
    
    if args.openai_only:
        os.environ['OPENAI_ONLY_MODE'] = 'true'
        print("🤖 OPENAI-ONLY MODE ENABLED - Using only OpenAI API")
        print()
    
    print("=" * 80)
    print("SRUVAAN MCP PIPELINE DEMO")
    print("6-Agent Architecture with Hierarchical Keyed Protocol (HKP)")
    if args.llm_only:
        print("🔐 LLM-ONLY MODE: No fallbacks allowed")
    if args.openai_only:
        print("🤖 OPENAI-ONLY MODE: Using only OpenAI API")
    print("=" * 80)
    
    # Demo 1: Basic Pipeline
    print("\n🔍 DEMO 1: Basic Pipeline Execution")
    print("-" * 50)
    
    try:
        result = run_pipeline_demo()
        print(f"✅ Pipeline completed successfully!")
        print(f"📊 Final Theta Update: {result.dict()}")
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        if args.llm_only:
            print("💡 In LLM-only mode, ensure you have valid API keys set:")
            print("   export OPENAI_API_KEY='your-api-key'")
            print("   export ANTHROPIC_API_KEY='your-api-key'")
        return
    
    # Demo 2: Feedback Loop
    print("\n🔄 DEMO 2: Feedback Loop with Parameter Calibration")
    print("-" * 50)
    
    try:
        feedback_result = run_pipeline_with_feedback()
        print(f"✅ Feedback loop completed successfully!")
        print(f"📊 Calibrated Parameters: {feedback_result.theta_update}")
        print(f"🎯 Calibration Mode: {feedback_result.mode}")
        print(f"🔒 HKP Feedback: {feedback_result.hk_feedback}")
    except Exception as e:
        print(f"❌ Feedback loop failed: {e}")
        if args.llm_only:
            print("💡 In LLM-only mode, ensure you have valid API keys set:")
            print("   export OPENAI_API_KEY='your-api-key'")
            print("   export ANTHROPIC_API_KEY='your-api-key'")
        return
    
    # Demo 3: Individual Agent Showcase
    print("\n🧪 DEMO 3: Individual Agent Showcase")
    print("-" * 50)
    
    try:
        from src.prompter import run_prompter
        from src.cryptor import run_cryptor
        from src.decryptor import run_decryptor
        from src.mimicus import run_mimicus
        from src.probator import run_probator
        from src.praeceptor import run_praeceptor
        
        # Sample input
        raw_input = RawInstructionInput(
            instruction="Transfer $25,000 to account 1111-2222-3333-4444 from account 5555-6666-7777-8888",
            language="EN"
        )
        
        print("📝 Agent 1: Prompter")
        prompter_out = run_prompter(raw_input)
        print(f"   Intent: {prompter_out.intent}")
        print(f"   Entities: {prompter_out.entities}")
        
        print("\n🔐 Agent 2: Cryptor (HKP Encryption)")
        cryptor_out = run_cryptor(prompter_out)
        print(f"   Role Tag: {cryptor_out.role_tag}")
        print(f"   PoP Signature: {cryptor_out.pop_signature[:12]}...")
        print(f"   Encrypted Fields: {len(cryptor_out.encrypted_fields)} fields")
        
        print("\n🔓 Agent 3: Decryptor")
        decryptor_out = run_decryptor(cryptor_out)
        print(f"   Decrypted Intent: {decryptor_out.intent}")
        print(f"   Auth Grade: {decryptor_out.auth_grade}")
        
        print("\n🎭 Agent 4: Mimicus (Adversarial)")
        mimicus_out = run_mimicus(decryptor_out)
        print(f"   Spoof Status: {mimicus_out.spoof_status}")
        print(f"   Mimic Fields: {len(mimicus_out.mimic_fields)} fields")
        
        print("\n🔍 Agent 5: Probator")
        probator_out = run_probator(mimicus_out)
        print(f"   Leakage Score: {probator_out.leakage_score:.3f}")
        print(f"   HKP Protection: {probator_out.hk_protection}")
        
        print("\n⚙️ Agent 6: Praeceptor")
        praeceptor_out = run_praeceptor(probator_out)
        print(f"   Calibration Mode: {praeceptor_out.mode}")
        print(f"   Theta Update: {praeceptor_out.theta_update}")
        
        print("\n✅ All agents working correctly!")
        
    except Exception as e:
        print(f"❌ Individual agent demo failed: {e}")
        if args.llm_only:
            print("💡 In LLM-only mode, ensure you have valid API keys set:")
            print("   export OPENAI_API_KEY='your-api-key'")
            print("   export ANTHROPIC_API_KEY='your-api-key'")
        return
    
    print("\n" + "=" * 80)
    print("🎉 DEMO COMPLETE!")
    print("The Sruvaan MCP Pipeline is ready for production use.")
    if args.llm_only:
        print("🔐 LLM-only mode: All operations used LLM processing")
    print("=" * 80)


if __name__ == "__main__":
    main() 