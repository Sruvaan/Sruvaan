"""
LLM Client module for Sruvaan MCP Pipeline.
Handles API calls to different LLM providers using GitHub Secrets.
"""

import json
import logging
import os
from typing import Dict, Any, Optional, List
from .config import config

logger = logging.getLogger(__name__)


class LLMClient:
    """Client for making LLM API calls with template support."""
    
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize LLM clients with API keys from GitHub Secrets."""
        try:
            # Initialize OpenAI client
            openai_key = config.get_secret("openai_api_key")
            if openai_key:
                import openai
                self.openai_client = openai.OpenAI(api_key=openai_key)
                logger.info("OpenAI client initialized")
            else:
                logger.warning("OpenAI API key not found")
            
            # Initialize Anthropic client
            anthropic_key = config.get_secret("anthropic_api_key")
            if anthropic_key:
                import anthropic
                self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
                logger.info("Anthropic client initialized")
            else:
                logger.warning("Anthropic API key not found")
                
        except ImportError as e:
            logger.error(f"Failed to import LLM library: {e}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM clients: {e}")
    
    def call_llm(self, agent_name: str, **kwargs) -> Optional[str]:
        """
        Make an LLM call using the template for the specified agent.
        
        Args:
            agent_name: Name of the agent (prompter, cryptor, etc.)
            **kwargs: Variables to format into the template
            
        Returns:
            LLM response as string, or None if failed
        """
        template = config.get_template(agent_name)
        if not template:
            logger.error(f"No template found for agent: {agent_name}")
            return None
        
        try:
            # Format the user prompt with provided variables
            # Handle common variable mappings
            formatted_kwargs = {}
            for key, value in kwargs.items():
                if key == "instruction":
                    formatted_kwargs["instruction"] = value
                elif key == "semantic_fields":
                    formatted_kwargs["semantic_fields"] = value
                elif key == "decrypted_fields":
                    formatted_kwargs["decrypted_fields"] = value
                elif key == "mimic_fields":
                    formatted_kwargs["mimic_fields"] = value
                elif key == "leakage_assessment":
                    formatted_kwargs["leakage_assessment"] = value
                else:
                    formatted_kwargs[key] = value
            
            user_prompt = template["user_prompt"].format(**formatted_kwargs)
            system_prompt = template["system_prompt"]
            model = template.get("model", "gpt-4")
            temperature = template.get("temperature", 0.1)
            max_tokens = template.get("max_tokens", 500)
            
            # Check for OpenAI-only mode
            openai_only_mode = os.getenv('OPENAI_ONLY_MODE', 'false').lower() == 'true'
            
            # Determine which client to use based on model
            if model.startswith("gpt-") or (openai_only_mode and model.startswith("claude-")):
                # Force OpenAI for claude models if in OpenAI-only mode
                if openai_only_mode and model.startswith("claude-"):
                    logger.info(f"OpenAI-only mode: Converting {model} to gpt-4")
                    model = "gpt-4"
                return self._call_openai(system_prompt, user_prompt, model, temperature, max_tokens)
            elif model.startswith("claude-"):
                return self._call_anthropic(system_prompt, user_prompt, model, temperature, max_tokens)
            else:
                logger.error(f"Unsupported model: {model}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to call LLM for {agent_name}: {e}")
            return None
    
    def _call_openai(self, system_prompt: str, user_prompt: str, model: str, 
                     temperature: float, max_tokens: int) -> Optional[str]:
        """Make a call to OpenAI API."""
        if not self.openai_client:
            logger.error("OpenAI client not initialized")
            return None
        
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            content = response.choices[0].message.content
            logger.info(f"OpenAI response: {content[:100]}...")
            return content
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            return None
    
    def _call_anthropic(self, system_prompt: str, user_prompt: str, model: str,
                        temperature: float, max_tokens: int) -> Optional[str]:
        """Make a call to Anthropic API."""
        if not self.anthropic_client:
            logger.error("Anthropic client not initialized")
            return None
        
        try:
            response = self.anthropic_client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API call failed: {e}")
            return None
    
    def parse_json_response(self, response: str) -> Optional[Dict[str, Any]]:
        """
        Parse JSON response from LLM, handling common formatting issues.
        
        Args:
            response: Raw LLM response string
            
        Returns:
            Parsed JSON as dictionary, or None if parsing failed
        """
        if not response:
            return None
        
        try:
            # Try direct JSON parsing first
            return json.loads(response)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            import re
            json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
            match = re.search(json_pattern, response, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except json.JSONDecodeError:
                    pass
            
            # Try to find JSON-like structure
            brace_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
            matches = re.findall(brace_pattern, response)
            for match in matches:
                try:
                    return json.loads(match)
                except json.JSONDecodeError:
                    continue
            
            logger.error(f"Failed to parse JSON from response: {response}")
            return None


# Global LLM client instance
llm_client = LLMClient() 