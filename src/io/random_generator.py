"""Générateur de jeux finis avec gains aléatoires (Exigence R1)."""
import itertools
import random
from typing import Dict, List, Optional, Tuple

from ..models.game import NormalFormGame


def generate_random_game(
    n_players: int = 2,
    strategy_counts: Optional[List[int]] = None,
    min_payoff: int = -5,
    max_payoff: int = 10,
    seed: Optional[int] = None,
    name: Optional[str] = None,
) -> NormalFormGame:
    """
    Génère un jeu à N joueurs avec des stratégies et des gains entiers aléatoires.

    Args:
        n_players: Nombre de joueurs (>= 2).
        strategy_counts: Liste de taille n_players donnant le nombre de stratégies par joueur.
        min_payoff: Borne inférieure des gains.
        max_payoff: Borne supérieure des gains.
        seed: Graine optionnelle pour la reproductibilité.
        name: Nom du jeu généré.
    """
    if n_players < 2:
        raise ValueError("Le nombre de joueurs doit être >= 2.")

    if strategy_counts is None:
        strategy_counts = [2] * n_players

    if len(strategy_counts) != n_players:
        raise ValueError(
            f"strategy_counts doit avoir {n_players} éléments (fourni: {len(strategy_counts)})."
        )

    rng = random.Random(seed)

    players = [f"Joueur {i+1}" for i in range(n_players)]
    strategies: Dict[str, List[str]] = {}

    for i, p in enumerate(players):
        k = strategy_counts[i]
        prefix = chr(ord("A") + i) if i < 26 else f"P{i+1}"
        strategies[p] = [f"{prefix}{s+1}" for s in range(k)]

    all_strat_lists = [strategies[p] for p in players]
    all_profiles = list(itertools.product(*all_strat_lists))

    payoffs: Dict[Tuple[str, ...], Tuple[float, ...]] = {}
    for prof in all_profiles:
        pay = tuple(float(rng.randint(min_payoff, max_payoff)) for _ in range(n_players))
        payoffs[prof] = pay

    game_name = name or f"Jeu Aléatoire ({n_players}J : {'x'.join(str(k) for k in strategy_counts)})"

    return NormalFormGame(
        players=players,
        strategies=strategies,
        payoffs=payoffs,
        name=game_name,
        description=f"Généré aléatoirement avec gains dans [{min_payoff}, {max_payoff}] (graine={seed})",
    )
