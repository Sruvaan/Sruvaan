"""
Configuration module for Sruvaan MCP Pipeline.
Handles GitHub Secrets integration and environment variables.
"""

import os
import yaml
from typing import Dict, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class Config:
    """Configuration manager for the Sruvaan MCP Pipeline."""
    
    def __init__(self):
        self.secrets = {}
        self.templates = {}
        self._load_environment()
        self._load_templates()
    
    def _load_environment(self):
        """Load environment variables and GitHub Secrets."""
        # Load from .env file if it exists
        env_file = Path(".env")
        if env_file.exists():
            from dotenv import load_dotenv
            load_dotenv()
        
        # Load LLM API keys from environment variables
        self.secrets = {
            "openai_api_key": os.getenv("OPENAI_API_KEY"),
            "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
            "github_token": os.getenv("GITHUB_TOKEN"),
            "github_repo": os.getenv("GITHUB_REPOSITORY"),
        }
        
        # Validate required secrets
        missing_secrets = [key for key, value in self.secrets.items() 
                          if value is None and key != "github_token"]
        if missing_secrets:
            logger.warning(f"Missing required secrets: {missing_secrets}")
    
    def _load_templates(self):
        """Load YAML templates for LLM prompts."""
        templates_dir = Path("templates")
        if not templates_dir.exists():
            logger.warning("Templates directory not found, creating default templates")
            self._create_default_templates()
            return
        
        for template_file in templates_dir.glob("*.yaml"):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    template_data = yaml.safe_load(f)
                    agent_name = template_file.stem
                    self.templates[agent_name] = template_data
                    logger.info(f"Loaded template for {agent_name}")
            except Exception as e:
                logger.error(f"Failed to load template {template_file}: {e}")
    
    def _create_default_templates(self):
        """Create default YAML templates if they don't exist."""
        templates_dir = Path("templates")
        templates_dir.mkdir(exist_ok=True)
        
        default_templates = {
            "prompter": {
                "system_prompt": "You are a semantic parser for the Sruvaan MCP pipeline. Your task is to extract structured information from user instructions.",
                "user_prompt": """
INSTRUCTIONS:
1. Parse the user instruction to identify the intent (action type)
2. Extract all relevant entities (amounts, accounts, destinations, etc.)
3. Return a JSON object with the following structure:
   - intent: The main action (e.g., "transfer", "book_flight", "send_email")
   - entities: Dictionary of key-value pairs for all extracted information
   - auth_level: Default to "L4" for standard operations

EXAMPLE INPUT: "Transfer $75,000 to account 7395-8845-2291 from account 1559-6623-4401"

EXAMPLE OUTPUT:
{
  "intent": "transfer",
  "entities": {
    "amount": "75000 USD",
    "to_account": "7395-8845-2291",
    "from_account": "1559-6623-4401"
  },
  "auth_level": "L4",
  "timestamp": "2025-07-29T10:30:00Z",
  "status": "ready"
}

Parse the following instruction: {instruction}
""",
                "model": "gpt-4",
                "temperature": 0.1,
                "max_tokens": 500
            },
            "cryptor": {
                "system_prompt": "You are a Hierarchical Keyed Protocol (HKP) encryption agent for the Sruvaan MCP pipeline.",
                "user_prompt": """
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
""",
                "model": "gpt-4",
                "temperature": 0.1,
                "max_tokens": 800
            },
            "mimicus": {
                "system_prompt": "You are an adversarial mimicry agent for the Sruvaan MCP pipeline.",
                "user_prompt": """
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
""",
                "model": "gpt-4",
                "temperature": 0.3,
                "max_tokens": 600
            },
            "probator": {
                "system_prompt": "You are a leakage analysis agent for the Sruvaan MCP pipeline.",
                "user_prompt": """
LEAKAGE ANALYSIS OBJECTIVE:
Analyze encrypted and mimic outputs to quantify semantic leakage and decipherability.
Assess the effectiveness of HKP protection against adversarial mimicry.

ANALYSIS PROCESS:
1. Compare original encrypted fields with mimic fields
2. Quantify semantic leakage patterns
3. Assess HKP protection effectiveness
4. Calculate leakage scores and vulnerability metrics

EXAMPLE INPUT:
Original: {"Ωα": "DYNX_Ω47", "βΞ": "blk_Z9X5"}
Mimic: {"Ωα": "ZYNQ_∆33", "βΞ": "blk_M1Z9"}

EXAMPLE OUTPUT:
{
  "leakage_score": 0.15,
  "vulnerabilities": {
    "structure_exposure": 0.2,
    "semantic_leakage": 0.1,
    "pattern_predictability": 0.3
  },
  "hkp_effectiveness": 0.85
}

Analyze leakage for the following comparison:
Original: {original_fields}
Mimic: {mimic_fields}
""",
                "model": "gpt-4",
                "temperature": 0.1,
                "max_tokens": 400
            },
            "praeceptor": {
                "system_prompt": "You are a cryptographic policy calibration agent for the Sruvaan MCP pipeline.",
                "user_prompt": """
CALIBRATION OBJECTIVE:
Update cryptographic parameters based on leakage assessment feedback.
Optimize HKP encryption parameters to minimize semantic leakage.

CALIBRATION PROCESS:
1. Analyze leakage assessment results
2. Determine optimal parameter adjustments
3. Update theta parameters for next encryption cycle
4. Provide feedback for continuous improvement

EXAMPLE INPUT:
{
  "leakage_score": 0.15,
  "vulnerabilities": {
    "structure_exposure": 0.2,
    "semantic_leakage": 0.1,
    "pattern_predictability": 0.3
  },
  "hkp_effectiveness": 0.85
}

EXAMPLE OUTPUT:
{
  "theta_params": {
    "entropy": 0.6,
    "cipher_strength": 0.9,
    "role_decay": 0.4
  },
  "calibration_mode": "enhanced_protection",
  "effectiveness_score": 0.92
}

Calibrate parameters based on the following assessment: {leakage_assessment}
""",
                "model": "gpt-4",
                "temperature": 0.1,
                "max_tokens": 500
            }
        }
        
        for agent_name, template_data in default_templates.items():
            template_file = templates_dir / f"{agent_name}.yaml"
            with open(template_file, 'w', encoding='utf-8') as f:
                yaml.dump(template_data, f, default_flow_style=False, indent=2)
            logger.info(f"Created default template for {agent_name}")
        
        # Load the created templates
        self._load_templates()
    
    def get_secret(self, key: str) -> Optional[str]:
        """Get a secret value by key."""
        return self.secrets.get(key)
    
    def get_template(self, agent_name: str) -> Optional[Dict]:
        """Get template for a specific agent."""
        return self.templates.get(agent_name)
    
    def validate_config(self) -> bool:
        """Validate that all required configuration is present."""
        # For testing, only require OpenAI API key
        required_secrets = ["openai_api_key"]
        missing_secrets = [secret for secret in required_secrets 
                          if not self.get_secret(secret)]
        
        if missing_secrets:
            logger.error(f"Missing required secrets: {missing_secrets}")
            return False
        
        if not self.templates:
            logger.error("No templates loaded")
            return False
        
        return True


# Global configuration instance
config = Config() 