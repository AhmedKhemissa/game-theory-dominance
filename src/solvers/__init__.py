"""Module de résolution par élimination itérée."""
from .dominance import check_dominance, find_elimination_candidates
from .eliminator import DominanceEliminator

__all__ = [
    "check_dominance",
    "find_elimination_candidates",
    "DominanceEliminator",
]
