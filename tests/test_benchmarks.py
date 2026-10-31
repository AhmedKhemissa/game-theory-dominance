"""Validation complète des 5 exemples du sujet de TP avec Pytest."""
import pytest
from src.benchmarks.tp_benchmarks import (
    get_example_1,
    get_example_2,
    get_example_3,
    get_example_4,
    get_example_5,
)
from src.models.step import DominanceMode
from src.solvers.eliminator import DominanceEliminator


def test_example_1_strict() -> None:
    """
    Exemple 1 : 2 joueurs 3x3.
    Résultat attendu : Profil unique (H, C) avec gains (2, 3).
    """
    game = get_example_1()
    solver = DominanceEliminator(mode=DominanceMode.STRICT)
    report = solver.solve(game)

    assert report.is_unique_profile is True
    assert report.unique_profile == ("H", "C")
    assert report.unique_payoffs == (2.0, 3.0)
    assert report.total_steps == 4

    # Vérification des étapes chronologiques
    # Étape 1 : D est éliminée pour le Joueur 2
    assert report.steps[0].player == "Joueur 2"
    assert report.steps[0].eliminated_strategy == "D"

    # Étapes 2 et 3 : M et B éliminées pour le Joueur 1
    j1_eliminated = {report.steps[1].eliminated_strategy, report.steps[2].eliminated_strategy}
    assert j1_eliminated == {"M", "B"}

    # Étape 4 : G est éliminée pour le Joueur 2
    assert report.steps[3].player == "Joueur 2"
    assert report.steps[3].eliminated_strategy == "G"


def test_example_2_rock_paper_scissors() -> None:
    """
    Exemple 2 : Pierre-Feuille-Ciseaux (RPS).
    Résultat attendu : Aucune élimination (strict et faible), matrice 3x3 inchangée.
    """
    game = get_example_2()

    # En mode strict
    solver_strict = DominanceEliminator(mode=DominanceMode.STRICT)
    report_strict = solver_strict.solve(game)
    assert report_strict.total_steps == 0
    assert report_strict.is_unique_profile is False
    assert report_strict.reduced_game.shape == (3, 3)

    # En mode faible
    solver_weak = DominanceEliminator(mode=DominanceMode.FAIBLE)
    report_weak = solver_weak.solve(game)
    assert report_weak.total_steps == 0
    assert report_weak.is_unique_profile is False
    assert report_weak.reduced_game.shape == (3, 3)


def test_example_3_strict() -> None:
    """
    Exemple 3 en mode STRICT :
    Résultat attendu : Seule D est supprimée, il reste la matrice 2x2 {H, B} x {G, M}.
    """
    game = get_example_3()
    solver = DominanceEliminator(mode=DominanceMode.STRICT)
    report = solver.solve(game)

    assert report.total_steps == 1
    assert report.steps[0].player == "Joueur 2"
    assert report.steps[0].eliminated_strategy == "D"
    assert report.is_unique_profile is False
    assert report.reduced_game.shape == (2, 2)
    assert report.reduced_game.strategies["Joueur 1"] == ["H", "B"]
    assert report.reduced_game.strategies["Joueur 2"] == ["G", "M"]


def test_example_3_weak_branching() -> None:
    """
    Exemple 3 en mode FAIBLE :
    Résultat attendu selon l'ordre :
    - Si B éliminée en 1er -> H x {G, M}
    - Si M éliminée en 1er -> {H, B} x G
    La recherche arborescente doit trouver les deux équilibres réduits !
    """
    game = get_example_3()
    solver = DominanceEliminator(mode=DominanceMode.FAIBLE)

    branches = solver.solve_all_branches(game)
    assert len(branches) >= 2

    resulting_signatures = set()
    for rep in branches:
        j1_s = tuple(sorted(rep.reduced_game.strategies["Joueur 1"]))
        j2_s = tuple(sorted(rep.reduced_game.strategies["Joueur 2"]))
        resulting_signatures.add((j1_s, j2_s))

    # Doit contenir à la fois (('H',), ('G', 'M')) et (('B', 'H'), ('G',))
    assert (("H",), ("G", "M")) in resulting_signatures
    assert (("B", "H"), ("G",)) in resulting_signatures


def test_example_4_three_players() -> None:
    """
    Exemple 4 : Jeu public à 3 joueurs (N >= 3).
    Résultat attendu : Profil unique (N, N, N) avec gains (0, 0, 0).
    """
    game = get_example_4()
    solver = DominanceEliminator(mode=DominanceMode.STRICT)
    report = solver.solve(game)

    assert report.is_unique_profile is True
    assert report.unique_profile == ("N", "N", "N")
    assert report.unique_payoffs == (0.0, 0.0, 0.0)
    assert report.total_steps == 3

    # Les 3 stratégies éliminées doivent être 'C' pour chaque joueur
    eliminated_strategies = [step.eliminated_strategy for step in report.steps]
    assert eliminated_strategies == ["C", "C", "C"]


def test_example_5_serie1() -> None:
    """
    Exemple 5 : Exercice 4 de la Série 1 (3x3).
    Résultat attendu : Profil unique (A3, B3) avec gains (5, 3) en 4 tours stricts.
    """
    game = get_example_5()
    solver = DominanceEliminator(mode=DominanceMode.STRICT)
    report = solver.solve(game)

    assert report.is_unique_profile is True
    assert report.unique_profile == ("A3", "B3")
    assert report.unique_payoffs == (5.0, 3.0)
    assert report.total_steps == 4

    # Tour 1 : B2 éliminée pour Joueur 2
    assert report.steps[0].player == "Joueur 2"
    assert report.steps[0].eliminated_strategy == "B2"

    # Tour 2 : A2 éliminée pour Joueur 1
    assert report.steps[1].player == "Joueur 1"
    assert report.steps[1].eliminated_strategy == "A2"

    # Tour 3 : B1 éliminée pour Joueur 2
    assert report.steps[2].player == "Joueur 2"
    assert report.steps[2].eliminated_strategy == "B1"

    # Tour 4 : A1 éliminée pour Joueur 1
    assert report.steps[3].player == "Joueur 1"
    assert report.steps[3].eliminated_strategy == "A1"
