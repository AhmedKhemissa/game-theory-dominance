"""Test de validation des fichiers du dossier data/."""
import glob
import os
import pytest

from src.io.parser import load_game_file
from src.models.step import DominanceMode
from src.solvers.eliminator import DominanceEliminator


def test_load_and_solve_all_data_files() -> None:
    """Vérifie que tous les fichiers du dossier data/ sont valides et solvables."""
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    files = glob.glob(os.path.join(data_dir, "*.*"))
    assert len(files) >= 6, f"Attendu au moins 6 fichiers dans data/, trouvé {len(files)}"

    for fpath in files:
        if not (fpath.endswith(".json") or fpath.endswith(".game")):
            continue
        game = load_game_file(fpath)
        assert game.num_players >= 2

        # Exécuter en mode strict
        solver = DominanceEliminator(mode=DominanceMode.STRICT)
        report = solver.solve(game)
        assert report.reduced_game is not None
