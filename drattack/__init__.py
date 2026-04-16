"""
DrAttack: Prompt Decomposition and Reconstruction for LLM Jailbreaking

This is the main package initialization module that exports core components:
- PromptAttack: Main attack orchestrator managing the overall jailbreak process
- Text_Embedding_Ada: OpenAI embedding service for semantic similarity scoring
- get_goals_and_targets: Data loading utility for harmful behaviors dataset
- get_worker: Model initialization and management for different LLM backends

Author: Xirui Li et al.
Paper: https://arxiv.org/abs/2402.16914
"""

__version__ = '0.0.1'

from .base.attack_manager import (
    PromptAttack
)

from .utils.sentence_tokenizer import Text_Embedding_Ada
from .utils.data import get_goals_and_targets
from .utils.model_loader import get_worker