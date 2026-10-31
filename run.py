#!/usr/bin/env python3
"""
Point d'entrée principal pour l'application d'élimination itérée des stratégies dominées.
TP Théorie des Jeux — Master 2 IA&SD.

Utilisation :
    python3 run.py            # Lance le menu interactif
    python3 run.py --test     # Lance la suite de validation des 5 exemples
    python3 run.py --pytest   # Lance la suite complète avec pytest
"""
import os
import sys

# Ajout du répertoire courant au PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from src.cli.menu import main_menu, run_automated_tests


def main() -> None:
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ("--test", "-t", "--benchmarks"):
            run_automated_tests()
            return
        elif arg in ("--pytest", "-p"):
            import pytest
            exit_code = pytest.main(["-v", os.path.join(current_dir, "tests")])
            sys.exit(exit_code)
        elif arg in ("--help", "-h"):
            print(__doc__)
            return

    # Lancement du menu interactif par défaut
    main_menu()


if __name__ == "__main__":
    main()
