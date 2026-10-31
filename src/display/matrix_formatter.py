"""Moteur d'affichage soigné des matrices de jeux (2 joueurs et N joueurs)."""
import itertools
from typing import Dict, List, Optional, Sequence, Tuple

from ..models.game import NormalFormGame
from ..models.step import EliminationStep, TraceReport


def format_number(val: float) -> str:
    """Affiche un nombre entier sans décimale inutile (ex: 3 au lieu de 3.0)."""
    if abs(val - round(val)) < 1e-9:
        return str(int(round(val)))
    return f"{val:.2f}"


def format_vector(payoffs: Sequence[float]) -> str:
    """Formate un vecteur de gains : (u_1, u_2, ..., u_n)."""
    inner = ", ".join(format_number(v) for v in payoffs)
    return f"({inner})"


class MatrixFormatter:
    """Générateur d'affichages tabulaires élégants pour matrices de gains."""

    @classmethod
    def render_2d_slice(
        cls,
        game: NormalFormGame,
        p1: str,
        p2: str,
        fixed_opponents: Optional[Dict[str, str]] = None,
    ) -> str:
        """
        Génère une table 2D avec Joueur 1 (p1) en lignes et Joueur 2 (p2) en colonnes.
        Si N >= 3, fixed_opponents fixe les stratégies des joueurs 3 à N.
        """
        if fixed_opponents is None:
            fixed_opponents = {}

        p1_strats = game.strategies[p1]
        p2_strats = game.strategies[p2]

        # Déterminer la largeur maximale de la première colonne (étiquettes des lignes)
        p1_label = f"[{p1}]"
        max_row_header_len = max(
            len(p1_label),
            max((len(s) for s in p1_strats), default=4)
        ) + 2

        # Précalculer le contenu des cellules et déterminer les largeurs de colonnes
        cells: Dict[Tuple[str, str], str] = {}
        col_widths: Dict[str, int] = {}

        for col_strat in p2_strats:
            max_len = len(col_strat)
            for row_strat in p1_strats:
                # Reconstituer le profil complet
                prof_dict = {p1: row_strat, p2: col_strat}
                prof_dict.update(fixed_opponents)
                full_prof = tuple(prof_dict[p] for p in game.players)
                pay = game.get_payoff(full_prof)
                cell_text = format_vector(pay)
                cells[(row_strat, col_strat)] = cell_text
                if len(cell_text) > max_len:
                    max_len = len(cell_text)
            col_widths[col_strat] = max_len + 2

        # Construction du tableau avec caractères Unicode soignés
        lines: List[str] = []

        # En-tête des colonnes (Nom du Joueur 2)
        p2_header_title = f"Colonnes : {p2}"
        lines.append(f"  {p2_header_title}")

        # Ligne supérieure
        top_border = "┌" + "─" * max_row_header_len
        for c in p2_strats:
            top_border += "┬" + "─" * col_widths[c]
        top_border += "┐"
        lines.append(top_border)

        # Ligne des noms de colonnes
        header_row = f"│ {p1:<{max_row_header_len - 2}} "
        for c in p2_strats:
            header_row += f"│ {c:^{col_widths[c] - 2}} "
        header_row += "│"
        lines.append(header_row)

        # Séparateur après en-tête
        sep_border = "├" + "─" * max_row_header_len
        for c in p2_strats:
            sep_border += "┼" + "─" * col_widths[c]
        sep_border += "┤"
        lines.append(sep_border)

        # Lignes de données
        for r in p1_strats:
            row_str = f"│ {r:<{max_row_header_len - 2}} "
            for c in p2_strats:
                cell_val = cells[(r, c)]
                row_str += f"│ {cell_val:^{col_widths[c] - 2}} "
            row_str += "│"
            lines.append(row_str)

        # Ligne inférieure
        bottom_border = "└" + "─" * max_row_header_len
        for c in p2_strats:
            bottom_border += "┴" + "─" * col_widths[c]
        bottom_border += "┘"
        lines.append(bottom_border)

        return "\n".join(lines)

    @classmethod
    def format_game(cls, game: NormalFormGame) -> str:
        """
        Formate l'affichage complet du jeu :
        - Si 2 joueurs : une matrice 2D.
        - Si N >= 3 joueurs : une sous-matrice 2D (J1 en lignes, J2 en colonnes)
          pour chaque combinaison des stratégies actives des joueurs 3 à N.
        """
        if game.num_players == 2:
            return cls.render_2d_slice(game, game.players[0], game.players[1])

        # Cas N >= 3 joueurs (Exigence R2)
        p1, p2 = game.players[0], game.players[1]
        other_players = game.players[2:]

        other_strats = [game.strategies[p] for p in other_players]
        all_combinations = list(itertools.product(*other_strats))

        slices_output: List[str] = []
        slices_output.append(
            f"Jeu à {game.num_players} joueurs — Découpage par sous-matrices ({p1} en lignes × {p2} en colonnes) :"
        )

        for combo in all_combinations:
            fixed_map = {other_players[i]: combo[i] for i in range(len(other_players))}
            combo_label = ", ".join(f"{p} = '{s}'" for p, s in fixed_map.items())

            banner = (
                f"\n┌{'─' * 60}┐\n"
                f"│ SOUS-MATRICE POUR : {combo_label:<37} │\n"
                f"└{'─' * 60}┘"
            )
            slices_output.append(banner)
            matrix_str = cls.render_2d_slice(game, p1, p2, fixed_map)
            slices_output.append(matrix_str)

        return "\n".join(slices_output)

    @classmethod
    def format_step(cls, step: EliminationStep) -> str:
        """Formate l'affichage détaillé d'une étape d'élimination (Exigence R5)."""
        lines: List[str] = []
        mode_str = "DOMINANCE STRICTE" if step.mode.value == "strict" else "DOMINANCE FAIBLE"

        header = f" ÉTAPE {step.step_number} : [{mode_str}] "
        lines.append(f"\n╔{'═' * 70}╗")
        lines.append(f"║{header:^70}║")
        lines.append(f"╚{'═' * 70}╝")

        lines.append(f" • Joueur concerné     : {step.player}")
        lines.append(f" • Stratégie éliminée  : '{step.eliminated_strategy}'")
        lines.append(f" • Stratégie dominante : '{step.dominating_strategy}'")

        if step.justification:
            lines.append(" • Preuve mathématique :")
            if step.mode.value == "strict":
                lines.append(
                    f"   Pour tout s_-i, u({step.dominating_strategy}) > u({step.eliminated_strategy}) :"
                )
            else:
                lines.append(
                    f"   Pour tout s_-i, u({step.dominating_strategy}) >= u({step.eliminated_strategy}) "
                    f"avec au moins une supériorité stricte :"
                )

            for opp_prof, u_b, u_a, diff in step.justification.comparisons:
                opp_str = ", ".join(opp_prof) if opp_prof else "Ø"
                symbol = ">" if diff > 1e-9 else ("=" if abs(diff) <= 1e-9 else "<")
                lines.append(
                    f"     - Contre ({opp_str}) : {format_number(u_b)} {symbol} {format_number(u_a)} "
                    f"(écart = {format_number(diff)})"
                )

        lines.append("\n Matrice du jeu après suppression :")
        if step.game_after:
            lines.append(cls.format_game(step.game_after))

        return "\n".join(lines)

    @classmethod
    def format_report(cls, report: TraceReport) -> str:
        """Formate l'ensemble de l'exécution avec état initial, trace et résultat final."""
        lines: List[str] = []

        # En-tête principal
        lines.append("=" * 74)
        lines.append(f"  JEU INITIAL : {report.initial_game.name}")
        lines.append(
            f"  Joueurs : {', '.join(report.initial_game.players)} | "
            f"Dimensions initiales : {' × '.join(str(s) for s in report.initial_game.shape)}"
        )
        lines.append(f"  Mode d'élimination : {report.mode.value.upper()}")
        lines.append("=" * 74)
        lines.append("\n--- MATRICE DU JEU INITIAL ---")
        lines.append(cls.format_game(report.initial_game))

        # Trace des étapes (R5)
        if report.steps:
            lines.append("\n" + "=" * 74)
            lines.append("  DÉBUT DU PROCESSUS D'ÉLIMINATION ITÉRÉE")
            lines.append("=" * 74)
            for step in report.steps:
                lines.append(cls.format_step(step))
        else:
            lines.append("\n" + "-" * 74)
            lines.append("  AUCUNE STRATÉGIE DOMINÉE N'A ÉTÉ DÉTECTÉE DÈS LE DÉPART.")
            lines.append("-" * 74)

        # Résultat final (R6)
        lines.append("\n" + "=" * 74)
        lines.append("  RÉSULTAT FINAL (POINT FIXE ATTEINT)")
        lines.append("=" * 74)
        lines.append(f"  Total d'étapes d'élimination : {report.total_steps}")
        lines.append(f"  Dimensions finales du jeu    : {' × '.join(str(s) for s in report.reduced_game.shape)}")

        if report.is_unique_profile:
            lines.append("\n  ✔ SUCCÈS : LE JEU EST RÉDUIT À UN PROFIL UNIQUE (1 × 1... × 1) !")
            prof_str = ", ".join(f"{p} = '{s}'" for p, s in zip(report.reduced_game.players, report.unique_profile))
            lines.append(f"  • Profil d'équilibre : ({prof_str})")
            pay_str = ", ".join(f"{p} = {format_number(v)}" for p, v in zip(report.reduced_game.players, report.unique_payoffs))
            lines.append(f"  • Vecteur des gains   : {format_vector(report.unique_payoffs)} [{pay_str}]")
        else:
            lines.append("\n  ℹ LE JEU N'A PAS PU ÊTRE RÉDUIT À UN PROFIL UNIQUE.")
            lines.append("  • Stratégies pures restantes par joueur :")
            for p in report.reduced_game.players:
                lines.append(f"    - {p} : {report.reduced_game.strategies[p]}")

        lines.append("=" * 74)
        return "\n".join(lines)
