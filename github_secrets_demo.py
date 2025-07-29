#!/usr/bin/env python3
"""
GitHub Secrets Integration Demo
This script demonstrates how the LLM bots work with GitHub Secrets.
"""

import os
import sys
import logging

# Add src to path
sys.path.insert(0, '.')

from src.config import config
from src.llm_client import llm_client
from src.main_pipeline import run_pipeline_with_feedback

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def demo_github_secrets_integration():
    """Demonstrate GitHub Secrets integration with LLM bots."""
    
    print("=" * 80)
    print("🔐 GITHUB SECRETS INTEGRATION DEMO")
    print("=" * 80)
    
    # Check if we have API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    
    print(f"\n📋 API Key Status:")
    print(f"   OpenAI API Key: {'✅ Found' if openai_key else '❌ Missing'}")
    print(f"   Anthropic API Key: {'✅ Found' if anthropic_key else '❌ Missing'}")
    
    if not openai_key and not anthropic_key:
        print("\n💡 To test with real LLM calls, set your API keys:")
        print("   export OPENAI_API_KEY='your-openai-api-key'")
        print("   export ANTHROPIC_API_KEY='your-anthropic-api-key'")
        print("   python github_secrets_demo.py")
        print("\n🔄 Running with fallback mechanisms...")
    
    # Test configuration
    print(f"\n🔧 Configuration Status:")
    print(f"   Templates loaded: {len(config.templates)} templates")
    print(f"   Configuration valid: {'✅' if config.validate_config() else '❌'}")
    
    # Test LLM clients
    print(f"\n🤖 LLM Client Status:")
    print(f"   OpenAI client: {'✅ Ready' if llm_client.openai_client else '❌ Not available'}")
    print(f"   Anthropic client: {'✅ Ready' if llm_client.anthropic_client else '❌ Not available'}")
    
    # Run a test pipeline
    print(f"\n🚀 Running Pipeline Test...")
    
    test_instruction = "Transfer $50,000 to account 9876-5432-1098-7654 from account 1234-5678-9012-3456"
    
    try:
        result = run_pipeline_with_feedback(test_instruction)
        print(f"\n✅ Pipeline completed successfully!")
        print(f"📊 Final result: {result}")
        
    except Exception as e:
        print(f"\n❌ Pipeline error: {e}")
    
    print("\n" + "=" * 80)
    print("🎉 GITHUB SECRETS DEMO COMPLETE")
    print("=" * 80)

def show_github_secrets_setup():
    """Show how to set up GitHub Secrets."""
    
    print("\n📚 GITHUB SECRETS SETUP GUIDE")
    print("=" * 50)
    
    print("""
1. Go to your GitHub repository
2. Click on 'Settings' tab
3. Click on 'Secrets and variables' → 'Actions'
4. Click 'New repository secret'
5. Add the following secrets:

   Name: OPENAI_API_KEY
   Value: sk-... (your OpenAI API key)

   Name: ANTHROPIC_API_KEY  
   Value: sk-ant-... (your Anthropic API key)

6. The secrets will be automatically available in GitHub Actions
7. For local testing, create a .env file:

   OPENAI_API_KEY=your-openai-api-key
   ANTHROPIC_API_KEY=your-anthropic-api-key
   GITHUB_TOKEN=your-github-token
   GITHUB_REPOSITORY=your-username/your-repo
""")

if __name__ == "__main__":
    demo_github_secrets_integration()
    show_github_secrets_setup() 