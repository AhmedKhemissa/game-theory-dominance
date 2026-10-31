"""Tests unitaires des cas limites, des règles de dominance et des entrées/sorties."""
import os
import tempfile
import pytest

from src.models.game import NormalFormGame
from src.models.step import DominanceMode
from src.solvers.dominance import check_dominance
from src.solvers.eliminator import DominanceEliminator
from src.io.parser import load_game_file, load_json_game, load_text_game, save_json_game
from src.io.random_generator import generate_random_game
from src.display.matrix_formatter import MatrixFormatter


def test_identical_payoffs_convention() -> None:
    """
    Vérifie la convention fondamentale du sujet :
    'Deux stratégies ayant exactement les mêmes gains ne se dominent pas l'une l'autre.'
    """
    game = NormalFormGame(
        players=["J1", "J2"],
        strategies={
            "J1": ["A", "B"],
            "J2": ["X", "Y"],
        },
        payoffs={
            ("A", "X"): (5.0, 1.0),
            ("A", "Y"): (5.0, 1.0),
            ("B", "X"): (5.0, 1.0),
            ("B", "Y"): (5.0, 1.0),
        },
    )

    # A vs B pour J1 : gains identiques (5, 5)
    is_dom_strict, _ = check_dominance(game, "J1", "A", "B", DominanceMode.STRICT)
    assert is_dom_strict is False

    is_dom_weak, _ = check_dominance(game, "J1", "A", "B", DominanceMode.FAIBLE)
    assert is_dom_weak is False

    is_dom_weak_rev, _ = check_dominance(game, "J1", "B", "A", DominanceMode.FAIBLE)
    assert is_dom_weak_rev is False

    # Le solveur ne doit rien éliminer
    solver = DominanceEliminator(mode=DominanceMode.FAIBLE)
    report = solver.solve(game)
    assert report.total_steps == 0
    assert report.reduced_game.shape == (2, 2)


def test_json_round_trip() -> None:
    """Vérifie la sérialisation et désérialisation JSON."""
    game = NormalFormGame(
        players=["P1", "P2"],
        strategies={"P1": ["Up", "Down"], "P2": ["Left", "Right"]},
        payoffs={
            ("Up", "Left"): (10.0, -1.0),
            ("Up", "Right"): (2.0, 3.0),
            ("Down", "Left"): (0.0, 0.0),
            ("Down", "Right"): (4.0, 4.0),
        },
        name="Test Serialization",
    )

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        save_json_game(game, tmp_path)
        reloaded = load_json_game(tmp_path)
        assert reloaded.players == game.players
        assert reloaded.strategies == game.strategies
        assert reloaded.payoffs == game.payoffs
        assert reloaded.name == game.name
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_text_game_parser() -> None:
    """Vérifie le chargement d'un fichier .game au format texte."""
    text_content = """
    NAME: Simple Game
    PLAYERS: Alice, Bob
    STRATEGIES Alice: Cooperate, Defect
    STRATEGIES Bob: Cooperate, Defect
    PAYOFFS:
    Cooperate, Cooperate -> 3, 3
    Cooperate, Defect -> 0, 5
    Defect, Cooperate -> 5, 0
    Defect, Defect -> 1, 1
    """

    with tempfile.NamedTemporaryFile(suffix=".game", mode="w", delete=False) as tmp:
        tmp.write(text_content)
        tmp_path = tmp.name

    try:
        game = load_text_game(tmp_path)
        assert game.players == ["Alice", "Bob"]
        assert game.strategies["Alice"] == ["Cooperate", "Defect"]
        assert game.strategies["Bob"] == ["Cooperate", "Defect"]
        assert game.payoffs[("Defect", "Cooperate")] == (5.0, 0.0)

        # Test élimination sur ce Dilemme du Prisonnier : Defect domine strictement Cooperate !
        solver = DominanceEliminator(mode=DominanceMode.STRICT)
        report = solver.solve(game)
        assert report.is_unique_profile is True
        assert report.unique_profile == ("Defect", "Defect")
        assert report.unique_payoffs == (1.0, 1.0)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_random_generator_seed() -> None:
    """Vérifie que la graine aléatoire garantit la reproductibilité."""
    g1 = generate_random_game(n_players=3, strategy_counts=[2, 3, 2], seed=42)
    g2 = generate_random_game(n_players=3, strategy_counts=[2, 3, 2], seed=42)

    assert g1.players == g2.players
    assert g1.strategies == g2.strategies
    assert g1.payoffs == g2.payoffs


def test_matrix_formatter_n_players() -> None:
    """Vérifie que le formateur matriciel génère des sous-matrices pour N >= 3."""
    game = generate_random_game(n_players=3, strategy_counts=[2, 2, 2], seed=123)
    formatted = MatrixFormatter.format_game(game)

    assert "SOUS-MATRICE POUR : Joueur 3" in formatted
    assert "Joueur 1" in formatted
    assert "Joueur 2" in formatted
