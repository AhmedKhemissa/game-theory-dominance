"""Fournisseur des 5 jeux de test officiels du sujet de TP."""
from typing import Dict, List, Tuple

from ..models.game import NormalFormGame
from ..models.step import DominanceMode


def get_example_1() -> NormalFormGame:
    """
    Exemple 1 : 2 joueurs 3x3 (H, M, B vs G, C, D).
    Élimination stricte complète jusqu'au profil unique (H, C) avec gains (2, 3).
    """
    return NormalFormGame(
        name="Exemple 1 : Élimination possible jusqu'à 1x1 (Dominance stricte)",
        description="Jeu 2 joueurs 3x3 aboutissant à (H, C) avec gains (2, 3)",
        players=["Joueur 1", "Joueur 2"],
        strategies={
            "Joueur 1": ["H", "M", "B"],
            "Joueur 2": ["G", "C", "D"],
        },
        payoffs={
            ("H", "G"): (3.0, 1.0),
            ("H", "C"): (2.0, 3.0),
            ("H", "D"): (0.0, 0.0),
            ("M", "G"): (1.0, 2.0),
            ("M", "C"): (1.0, 2.0),
            ("M", "D"): (5.0, 1.0),
            ("B", "G"): (2.0, 2.0),
            ("B", "C"): (0.0, 1.0),
            ("B", "D"): (1.0, 0.0),
        },
    )


def get_example_2() -> NormalFormGame:
    """
    Exemple 2 : Pierre-Feuille-Ciseaux (RPS).
    Aucune stratégie dominée (stricte ou faible). Matrice 3x3 inchangée.
    """
    return NormalFormGame(
        name="Exemple 2 : Élimination impossible (Pierre-Feuille-Ciseaux)",
        description="Jeu à somme nulle où aucune stratégie n'est dominée",
        players=["Joueur 1", "Joueur 2"],
        strategies={
            "Joueur 1": ["Pierre", "Feuille", "Ciseaux"],
            "Joueur 2": ["Pierre", "Feuille", "Ciseaux"],
        },
        payoffs={
            ("Pierre", "Pierre"): (0.0, 0.0),
            ("Pierre", "Feuille"): (-1.0, 1.0),
            ("Pierre", "Ciseaux"): (1.0, -1.0),
            ("Feuille", "Pierre"): (1.0, -1.0),
            ("Feuille", "Feuille"): (0.0, 0.0),
            ("Feuille", "Ciseaux"): (-1.0, 1.0),
            ("Ciseaux", "Pierre"): (-1.0, 1.0),
            ("Ciseaux", "Feuille"): (1.0, -1.0),
            ("Ciseaux", "Ciseaux"): (0.0, 0.0),
        },
    )


def get_example_3() -> NormalFormGame:
    """
    Exemple 3 : Dominance faible et ordre d'élimination (2x3).
    - Mode strict : D est éliminée, il reste 2x2 {H, B} x {G, M}.
    - Mode faible : H x {G, M} ou {H, B} x G selon l'ordre.
    """
    return NormalFormGame(
        name="Exemple 3 : Dominance faible et ordre d'élimination",
        description="Matrice 2x3 illustrant la non-confluence de la dominance faible",
        players=["Joueur 1", "Joueur 2"],
        strategies={
            "Joueur 1": ["H", "B"],
            "Joueur 2": ["G", "M", "D"],
        },
        payoffs={
            ("H", "G"): (2.0, 1.0),
            ("H", "M"): (2.0, 1.0),
            ("H", "D"): (2.0, 0.0),
            ("B", "G"): (2.0, 1.0),
            ("B", "M"): (1.0, 0.0),
            ("B", "D"): (2.0, 0.0),
        },
    )


def get_example_4() -> NormalFormGame:
    """
    Exemple 4 : Jeu public à trois joueurs (2x2x2).
    Chacun choisit C ou N.
    Gain = 2*(#C) - 3 si C, et 2*(#C) si N.
    N domine strictement C pour chaque joueur -> Profil unique (N, N, N) avec gains (0, 0, 0).
    """
    return NormalFormGame(
        name="Exemple 4 : Trois joueurs (Jeu de contribution publique)",
        description="Jeu à 3 joueurs testant le cas général N >= 3",
        players=["Joueur 1", "Joueur 2", "Joueur 3"],
        strategies={
            "Joueur 1": ["C", "N"],
            "Joueur 2": ["C", "N"],
            "Joueur 3": ["C", "N"],
        },
        payoffs={
            ("C", "C", "C"): (3.0, 3.0, 3.0),
            ("C", "C", "N"): (1.0, 1.0, 4.0),
            ("C", "N", "C"): (1.0, 4.0, 1.0),
            ("N", "C", "C"): (4.0, 1.0, 1.0),
            ("C", "N", "N"): (-1.0, 2.0, 2.0),
            ("N", "C", "N"): (2.0, -1.0, 2.0),
            ("N", "N", "C"): (2.0, 2.0, -1.0),
            ("N", "N", "N"): (0.0, 0.0, 0.0),
        },
    )


def get_example_5() -> NormalFormGame:
    """
    Exemple 5 : Exercice 4 de la Série 1 (2 joueurs 3x3).
    Élimination alternée en 4 étapes aboutissant à (A3, B3) avec gains (5, 3).
    """
    return NormalFormGame(
        name="Exemple 5 : Exercice 4 de la Série 1",
        description="Jeu 3x3 avec élimination alternée stricte aboutissant à (A3, B3)",
        players=["Joueur 1", "Joueur 2"],
        strategies={
            "Joueur 1": ["A1", "A2", "A3"],
            "Joueur 2": ["B1", "B2", "B3"],
        },
        payoffs={
            ("A1", "B1"): (10.0, 10.0),
            ("A1", "B2"): (4.0, 9.0),
            ("A1", "B3"): (4.0, 11.0),
            ("A2", "B1"): (5.0, 6.0),
            ("A2", "B2"): (8.0, 3.0),
            ("A2", "B3"): (3.0, 4.0),
            ("A3", "B1"): (4.0, 0.0),
            ("A3", "B2"): (8.0, 1.0),
            ("A3", "B3"): (5.0, 3.0),
        },
    )


def get_all_benchmarks() -> List[Tuple[str, NormalFormGame, DominanceMode, str]]:
    """
    Retourne la liste complète des 5 benchmarks avec leur mode recommandé
    et résultat attendu.
    """
    return [
        (
            "Exemple 1",
            get_example_1(),
            DominanceMode.STRICT,
            "Profil unique (H, C) avec gains (2, 3)",
        ),
        (
            "Exemple 2",
            get_example_2(),
            DominanceMode.STRICT,
            "Aucune élimination, matrice 3x3 inchangée",
        ),
        (
            "Exemple 3 (Strict)",
            get_example_3(),
            DominanceMode.STRICT,
            "D supprimée, reste matrice 2x2 {H, B} x {G, M}",
        ),
        (
            "Exemple 3 (Faible)",
            get_example_3(),
            DominanceMode.FAIBLE,
            "H x {G, M} ou {H, B} x G selon l'ordre",
        ),
        (
            "Exemple 4 (3 joueurs)",
            get_example_4(),
            DominanceMode.STRICT,
            "Profil unique (N, N, N) avec gains (0, 0, 0)",
        ),
        (
            "Exemple 5 (Série 1)",
            get_example_5(),
            DominanceMode.STRICT,
            "Profil unique (A3, B3) avec gains (5, 3)",
        ),
    ]
