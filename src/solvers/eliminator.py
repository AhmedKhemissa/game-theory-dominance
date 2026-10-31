"""Moteur d'élimination itérée des stratégies dominées (IESDS et IEWDS)."""
from typing import Callable, List, Optional, Set, Tuple

from ..models.game import NormalFormGame
from ..models.step import DominanceMode, EliminationStep, TraceReport
from .dominance import find_elimination_candidates


class DominanceEliminator:
    """Moteur résolvant les jeux par élimination itérée avec enregistrement de trace."""

    def __init__(self, mode: DominanceMode = DominanceMode.STRICT) -> None:
        self.mode = mode

    def solve(
        self,
        game: NormalFormGame,
        candidate_selector: Optional[
            Callable[
                [List[Tuple[str, str, str, any]]],
                Tuple[str, str, str, any],
            ]
        ] = None,
    ) -> TraceReport:
        """
        Exécute l'élimination itérée pas-à-pas jusqu'à atteindre un point fixe
        (plus aucune stratégie dominée).

        Args:
            game: Jeu initial.
            candidate_selector: Fonction optionnelle de sélection parmi les candidats
                               (par défaut : premier candidat rencontré).

        Returns:
            TraceReport contenant l'historique complet des étapes et le jeu réduit final.
        """
        current_game = game.clone()
        steps: List[EliminationStep] = []
        step_number = 1

        while True:
            candidates = find_elimination_candidates(current_game, self.mode)
            if not candidates:
                # Point fixe atteint : aucune stratégie dominée restante
                break

            # Sélection du candidat à éliminer
            if candidate_selector is not None:
                selected = candidate_selector(candidates)
            else:
                # Politique déterministe standard : premier candidat rencontré
                selected = candidates[0]

            player, strat_a, strat_b, justification = selected

            # Réalisation de l'élimination
            current_game = current_game.eliminate_strategy(player, strat_a)

            step = EliminationStep(
                step_number=step_number,
                player=player,
                eliminated_strategy=strat_a,
                dominating_strategy=strat_b,
                mode=self.mode,
                justification=justification,
                game_after=current_game.clone(),
            )
            steps.append(step)
            step_number += 1

        is_unique = current_game.is_terminal()
        unique_prof = current_game.get_unique_profile() if is_unique else None
        unique_pay = current_game.get_unique_payoffs() if is_unique else None

        if len(steps) == 0:
            msg = "Aucune élimination possible : le jeu reste inchangé."
        elif is_unique:
            msg = f"Jeu réduit à un profil unique {unique_prof} avec gains {unique_pay}."
        else:
            msg = f"Jeu réduit à une forme indécomposable de dimensions {current_game.shape}."

        return TraceReport(
            initial_game=game.clone(),
            mode=self.mode,
            steps=steps,
            reduced_game=current_game,
            is_unique_profile=is_unique,
            unique_profile=unique_prof,
            unique_payoffs=unique_pay,
            total_steps=len(steps),
            message=msg,
        )

    def solve_all_branches(
        self,
        game: NormalFormGame,
    ) -> List[TraceReport]:
        """
        Explore exhaustivement par parcours arborescent (DFS) tous les ordres
        d'élimination possibles. Particulièrement pertinent en dominance faible
        pour révéler l'ensemble de tous les jeux réduits atteignables.
        """
        all_reports: List[TraceReport] = []
        visited_terminal_signatures: Set[str] = set()

        def dfs(
            cur_game: NormalFormGame,
            cur_steps: List[EliminationStep],
        ) -> None:
            candidates = find_elimination_candidates(cur_game, self.mode)
            if not candidates:
                # Feuille atteinte
                sig = self._game_signature(cur_game)
                if sig not in visited_terminal_signatures:
                    visited_terminal_signatures.add(sig)
                    is_unique = cur_game.is_terminal()
                    rep = TraceReport(
                        initial_game=game.clone(),
                        mode=self.mode,
                        steps=list(cur_steps),
                        reduced_game=cur_game.clone(),
                        is_unique_profile=is_unique,
                        unique_profile=cur_game.get_unique_profile() if is_unique else None,
                        unique_payoffs=cur_game.get_unique_payoffs() if is_unique else None,
                        total_steps=len(cur_steps),
                        message="Branche explorée avec succès.",
                    )
                    all_reports.append(rep)
                return

            for player, strat_a, strat_b, justification in candidates:
                next_game = cur_game.eliminate_strategy(player, strat_a)
                step = EliminationStep(
                    step_number=len(cur_steps) + 1,
                    player=player,
                    eliminated_strategy=strat_a,
                    dominating_strategy=strat_b,
                    mode=self.mode,
                    justification=justification,
                    game_after=next_game.clone(),
                )
                cur_steps.append(step)
                dfs(next_game, cur_steps)
                cur_steps.pop()

        dfs(game.clone(), [])
        return all_reports

    @staticmethod
    def _game_signature(game: NormalFormGame) -> str:
        """Génère une signature unique pour l'état résiduel des stratégies actives."""
        parts = []
        for p in game.players:
            strats = ",".join(sorted(game.strategies[p]))
            parts.append(f"{p}:[{strats}]")
        return ";".join(parts)
