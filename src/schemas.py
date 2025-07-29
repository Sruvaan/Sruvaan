"""
Pydantic schemas for the 6-agent MCP pipeline.
All data contracts between agents are defined here.
"""

from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime


class RawInstructionInput(BaseModel):
    """Raw user instruction input for the Prompter agent."""
    instruction: str
    language: str = "EN"


class SemanticPromptOut(BaseModel):
    """Structured semantic output from Prompter agent."""
    intent: str  # e.g., "book_flight", "send_email", "transfer"
    entities: Dict[str, str]  # All key info like {"amount": "75000 USD", "destination": "Paris"}
    auth_level: str = "L4"
    timestamp: Optional[str] = None
    status: str = "ready"


class EncryptedOutput(BaseModel):
    """Encrypted output from Cryptor agent with HKP fields."""
    encrypted_fields: Dict[str, Any]
    role_tag: str
    pop_signature: str
    time_tag: str


class DecryptedFieldsOut(BaseModel):
    """Decrypted fields from Decryptor agent."""
    intent: str
    entities: Dict[str, str]  # Generic decrypted structured fields
    auth_grade: str
    time_issued: str
    exec_status: str


class MimicOutput(BaseModel):
    """Mimic output from Mimicus agent for adversarial probing."""
    mimic_fields: Dict[str, Any]
    spoof_status: str


class LeakageVectorOut(BaseModel):
    """Leakage assessment from Probator agent."""
    leakage_score: float
    details: Dict[str, Any]
    hk_protection: str = "active"


class ThetaUpdate(BaseModel):
    """Parameter updates from Praeceptor agent for feedback loop."""
    theta_update: Dict[str, float]
    mode: str = "recalibrate"
    hk_feedback: bool = True 