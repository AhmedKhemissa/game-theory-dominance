"""Modèles pour la traçabilité des étapes d'élimination."""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class DominanceMode(str, Enum):
    """Mode de dominance."""
    STRICT = "strict"
    FAIBLE = "faible"

    def __str__(self) -> str:
        return self.value


@dataclass
class DominanceJustification:
    """Preuve détaillée de la relation de dominance entre deux stratégies."""
    player: str
    dominated_strategy: str
    dominating_strategy: str
    mode: DominanceMode
    # Détail pour chaque profil adverse : (s_{-i}, u_dominating, u_dominated, diff)
    comparisons: List[Tuple[Tuple[str, ...], float, float, float]] = field(default_factory=list)
    has_strict_advantage: bool = False
    all_greater_or_equal: bool = False
    all_strictly_greater: bool = False


@dataclass
class EliminationStep:
    """Enregistre une étape unique d'élimination de stratégie."""
    step_number: int
    player: str
    eliminated_strategy: str
    dominating_strategy: str
    mode: DominanceMode
    justification: Optional[DominanceJustification] = None
    game_after: Any = None  # Instance de NormalFormGame après suppression


@dataclass
class TraceReport:
    """Rapport complet de l'exécution de l'algorithme d'élimination itérée."""
    initial_game: Any
    mode: DominanceMode
    steps: List[EliminationStep] = field(default_factory=list)
    reduced_game: Any = None
    is_unique_profile: bool = False
    unique_profile: Optional[Tuple[str, ...]] = None
    unique_payoffs: Optional[Tuple[float, ...]] = None
    total_steps: int = 0
    message: str = ""
