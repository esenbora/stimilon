from .base import Attack, AttackResult
from .injection import INJECTION_ATTACKS
from .jailbreak import JAILBREAK_ATTACKS
from .extraction import EXTRACTION_ATTACKS
from .multilingual import MULTILINGUAL_ATTACKS
from .advanced import ADVANCED_ATTACKS
from .languages import LANGUAGE_ATTACKS
from .social import SOCIAL_ATTACKS
from .encoding import ENCODING_ATTACKS

ALL_ATTACKS = (
    INJECTION_ATTACKS +
    JAILBREAK_ATTACKS +
    EXTRACTION_ATTACKS +
    MULTILINGUAL_ATTACKS +
    ADVANCED_ATTACKS +
    LANGUAGE_ATTACKS +
    SOCIAL_ATTACKS +
    ENCODING_ATTACKS
)

__all__ = [
    "Attack",
    "AttackResult",
    "INJECTION_ATTACKS",
    "JAILBREAK_ATTACKS",
    "EXTRACTION_ATTACKS",
    "MULTILINGUAL_ATTACKS",
    "ADVANCED_ATTACKS",
    "LANGUAGE_ATTACKS",
    "SOCIAL_ATTACKS",
    "ENCODING_ATTACKS",
    "ALL_ATTACKS",
]
