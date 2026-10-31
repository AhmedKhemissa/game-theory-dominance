"""Prédicats mathématiques de dominance stricte et faible."""
from typing import List, Optional, Tuple

from ..models.game import NormalFormGame
from ..models.step import DominanceJustification, DominanceMode

EPSILON = 1e-9


def check_dominance(
    game: NormalFormGame,
    player: str,
    strat_b: str,
    strat_a: str,
    mode: DominanceMode,
    eps: float = EPSILON,
) -> Tuple[bool, Optional[DominanceJustification]]:
    """
    Vérifie si la stratégie 'strat_b' domine la stratégie 'strat_a' pour le joueur donné.

    Définitions :
    - Dominance stricte : u_i(b, s_-i) > u_i(a, s_-i) pour tout s_-i.
    - Dominance faible  : u_i(b, s_-i) >= u_i(a, s_-i) pour tout s_-i,
                          AVEC u_i(b, s_-i) > u_i(a, s_-i) pour au moins un s_-i.
    - Convention TP     : Deux stratégies ayant exactement les mêmes gains ne se
                          dominent pas l'une l'autre (retourne False).

    Retourne :
        (is_dominated, justification)
    """
    if strat_b == strat_a:
        return False, None

    opponents_profiles = game.get_opponents_profiles(player)
    comparisons: List[Tuple[Tuple[str, ...], float, float, float]] = []

    has_strict_advantage = False
    all_greater_or_equal = True
    all_strictly_greater = True

    for opp_prof in opponents_profiles:
        prof_b = game.build_full_profile(player, strat_b, opp_prof)
        prof_a = game.build_full_profile(player, strat_a, opp_prof)

        u_b = float(game.get_payoff(prof_b, player))
        u_a = float(game.get_payoff(prof_a, player))
        diff = u_b - u_a

        comparisons.append((opp_prof, u_b, u_a, diff))

        if mode == DominanceMode.STRICT:
            if diff <= eps:
                # Échec immédiat : b ne fait pas strictement mieux
                return False, None
        else:  # DominanceMode.FAIBLE
            if diff < -eps:
                # Échec immédiat : b fait strictement pire sur ce profil
                return False, None
            if diff > eps:
                has_strict_advantage = True

    justification = DominanceJustification(
        player=player,
        dominated_strategy=strat_a,
        dominating_strategy=strat_b,
        mode=mode,
        comparisons=comparisons,
        has_strict_advantage=has_strict_advantage,
        all_greater_or_equal=all_greater_or_equal,
        all_strictly_greater=all_strictly_greater,
    )

    if mode == DominanceMode.STRICT:
        justification.all_strictly_greater = True
        justification.has_strict_advantage = True
        return True, justification

    # Mode FAIBLE : Doit être >= partout ET > sur au moins un profil
    # Si tous les gains sont strictement égaux, has_strict_advantage est False -> retourne False
    if has_strict_advantage:
        justification.all_greater_or_equal = True
        return True, justification

    return False, None


def find_elimination_candidates(
    game: NormalFormGame,
    mode: DominanceMode,
) -> List[Tuple[str, str, str, DominanceJustification]]:
    """
    Trouve toutes les stratégies dominées dans l'état actuel du jeu.

    Retourne une liste de tuples :
        (joueur, stratégie_dominée, stratégie_dominante, justification)
    """
    candidates = []
    for player in game.players:
        active_strats = game.strategies[player]
        if len(active_strats) <= 1:
            continue

        for strat_a in active_strats:
            for strat_b in active_strats:
                if strat_a == strat_b:
                    continue
                is_dom, just = check_dominance(game, player, strat_b, strat_a, mode)
                if is_dom and just is not None:
                    candidates.append((player, strat_a, strat_b, just))
                    # Une stratégie a dominée par une autre b suffit pour être candidate
                    break

    return candidates
