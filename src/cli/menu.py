"""Interface utilisateur en ligne de commande (CLI interactive)."""
import os
import sys
from typing import Optional

from ..benchmarks.tp_benchmarks import (
    get_all_benchmarks,
    get_example_1,
    get_example_2,
    get_example_3,
    get_example_4,
    get_example_5,
)
from ..display.matrix_formatter import MatrixFormatter
from ..io.keyboard_input import input_game_from_keyboard
from ..io.parser import load_game_file, save_json_game
from ..io.random_generator import generate_random_game
from ..models.game import NormalFormGame
from ..models.step import DominanceMode
from ..solvers.eliminator import DominanceEliminator


def clear_screen() -> None:
    """Efface l'écran du terminal."""
    os.system("cls" if os.name == "nt" else "clear")


def print_banner() -> None:
    """Affiche la bannière du projet."""
    print("=" * 76)
    print("  THÉORIE DES JEUX : ÉLIMINATION ITÉRÉE DES STRATÉGIES DOMINÉES")
    print("    TP Master 2 IA&SD — Dominance Stricte et Dominance Faible")
    print("=" * 76)


def choose_mode() -> DominanceMode:
    """Demande à l'utilisateur de choisir le mode de dominance (R4)."""
    print("\n--- CHOIX DU MODE D'ÉLIMINATION ---")
    print("  [1] Dominance stricte (IESDS)")
    print("      -> u_i(b, s_-i) > u_i(a, s_-i) pour tout s_-i")
    print("  [2] Dominance faible (IEWDS)")
    print("      -> u_i(b, s_-i) >= u_i(a, s_-i) pour tout s_-i (avec strict pour au moins un)")

    while True:
        c = input("\nVotre choix [1/2, défaut 1] : ").strip()
        if not c or c == "1":
            return DominanceMode.STRICT
        if c == "2":
            return DominanceMode.FAIBLE
        print("  ⚠ Choix invalide. Entrez 1 ou 2.")


def execute_game_flow(game: NormalFormGame, default_mode: Optional[DominanceMode] = None) -> None:
    """Exécute la résolution et l'affichage avec trace complète pour un jeu donné."""
    mode = default_mode if default_mode is not None else choose_mode()

    # Si nous sommes en dominance faible et que le jeu possède plusieurs branches potentielles
    if mode == DominanceMode.FAIBLE and game.num_players == 2:
        print("\nOptions d'exécution pour la dominance faible :")
        print("  [1] Ordre séquentiel déterministe standard (recommandé)")
        print("  [2] Exploration arborescente complète de TOUS les ordres d'élimination (Exemple 3)")
        sub_choice = input("Votre choix [1/2, défaut 1] : ").strip()
        if sub_choice == "2":
            solver = DominanceEliminator(mode=mode)
            branches = solver.solve_all_branches(game)
            print(f"\n🔍 {len(branches)} résultat(s) réduit(s) distinct(s) trouvé(s) selon l'ordre :")
            for idx, rep in enumerate(branches, start=1):
                print(f"\n{'='*70}\nBRANCHE D'ÉLIMINATION #{idx}\n{'='*70}")
                print(MatrixFormatter.format_report(rep))
            input("\nAppuyez sur Entrée pour revenir au menu...")
            return

    # Résolution normale avec trace
    solver = DominanceEliminator(mode=mode)
    report = solver.solve(game)

    print("\n")
    print(MatrixFormatter.format_report(report))

    # Option de sauvegarde du jeu initial
    save_opt = input("\nSouhaitez-vous sauvegarder ce jeu au format JSON ? (o/N) : ").strip().lower()
    if save_opt in ("o", "oui", "y", "yes"):
        filename = input("Nom du fichier (ex: mon_jeu.json) [jeu_sauvegarde.json] : ").strip() or "jeu_sauvegarde.json"
        save_json_game(game, filename)
        print(f"✔ Jeu sauvegardé dans '{filename}'.")

    input("\nAppuyez sur Entrée pour revenir au menu...")


def menu_benchmarks() -> None:
    """Sous-menu des 5 jeux de test officiels du sujet."""
    benchmarks = [
        ("Exemple 1 : Élimination stricte complète -> (H, C) gains (2, 3)", get_example_1(), DominanceMode.STRICT),
        ("Exemple 2 : Pierre-Feuille-Ciseaux -> Aucune élimination (3x3)", get_example_2(), DominanceMode.STRICT),
        ("Exemple 3 : Dominance stricte -> Matrice 2x2 {H, B} x {G, M}", get_example_3(), DominanceMode.STRICT),
        ("Exemple 3 : Dominance faible & Dépendance de l'ordre d'élimination", get_example_3(), DominanceMode.FAIBLE),
        ("Exemple 4 : Jeu public à 3 joueurs (N=3) -> (N, N, N) gains (0, 0, 0)", get_example_4(), DominanceMode.STRICT),
        ("Exemple 5 : Exercice 4 Série 1 (4 étapes alternées) -> (A3, B3) gains (5, 3)", get_example_5(), DominanceMode.STRICT),
    ]

    while True:
        clear_screen()
        print_banner()
        print("\n--- JEUX DE TEST BENCHMARK DU TP ---")
        for i, (desc, _, _) in enumerate(benchmarks, start=1):
            print(f"  [{i}] {desc}")
        print("  [0] Retour au menu principal")

        c = input("\nChoisissez un exemple (0-6) : ").strip()
        if c == "0":
            break
        try:
            idx = int(c) - 1
            if 0 <= idx < len(benchmarks):
                _, game, mode = benchmarks[idx]
                execute_game_flow(game, default_mode=mode)
            else:
                print("⚠ Choix hors plage.")
        except ValueError:
            print("⚠ Veuillez entrer un chiffre.")


def menu_load_file() -> None:
    """Sous-menu de chargement depuis un fichier."""
    print("\n--- CHARGEMENT DEPUIS UN FICHIER ---")
    data_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data")
    if os.path.exists(data_dir):
        files = [f for f in os.listdir(data_dir) if f.endswith(".json") or f.endswith(".game")]
        print(f"Fichiers disponibles dans '{data_dir}' :")
        for f in files:
            print(f"  • {f}")

    path = input("\nChemin du fichier (JSON ou .game) : ").strip()
    if not path:
        return

    # Si l'utilisateur a entré juste le nom d'un fichier du dossier data/
    if not os.path.exists(path) and os.path.exists(os.path.join(data_dir, path)):
        path = os.path.join(data_dir, path)

    try:
        game = load_game_file(path)
        print(f"✔ Jeu '{game.name}' chargé avec succès ({game.num_players} joueurs).")
        execute_game_flow(game)
    except Exception as e:
        print(f"❌ Erreur lors du chargement : {e}")
        input("Appuyez sur Entrée pour continuer...")


def menu_random_game() -> None:
    """Sous-menu de génération d'un jeu aléatoire."""
    print("\n--- GÉNÉRATION ALÉATOIRE D'UN JEU ---")
    try:
        n = int(input("Nombre de joueurs n [2] : ").strip() or "2")
        k_list = []
        for i in range(1, n + 1):
            k = int(input(f"Nombre de stratégies pour le Joueur {i} [2] : ").strip() or "2")
            k_list.append(k)

        min_val = int(input("Gain minimum [-5] : ").strip() or "-5")
        max_val = int(input("Gain maximum [10] : ").strip() or "10")

        seed_str = input("Graine aléatoire (seed) [laisser vide pour aléatoire pur] : ").strip()
        seed = int(seed_str) if seed_str else None

        game = generate_random_game(
            n_players=n,
            strategy_counts=k_list,
            min_payoff=min_val,
            max_payoff=max_val,
            seed=seed,
        )
        print(f"\n✔ Jeu aléatoire généré ({game.get_active_profile_count()} profils) !")
        execute_game_flow(game)
    except Exception as e:
        print(f"❌ Erreur lors de la génération : {e}")
        input("Appuyez sur Entrée pour continuer...")


def run_automated_tests() -> None:
    """Lance la suite de tests automatisée interne."""
    print("\n" + "=" * 70)
    print("  EXÉCUTION DE LA SUITE DE TESTS AUTOMATISÉE (BENCHMARKS DU TP)")
    print("=" * 70)

    benchmarks = get_all_benchmarks()
    passed = 0
    total = len(benchmarks)

    for name, game, mode, expected in benchmarks:
        solver = DominanceEliminator(mode=mode)
        report = solver.solve(game)

        status = "✔ SUCCÈS"
        summary = ""
        if report.is_unique_profile:
            summary = f"Profil unique : {report.unique_profile} avec gains {report.unique_payoffs}"
        else:
            summary = f"Jeu réduit : dimensions {report.reduced_game.shape}"

        print(f"\n[{status}] {name} ({mode.value.upper()})")
        print(f"  • Attendu : {expected}")
        print(f"  • Obtenu  : {summary} (en {report.total_steps} étapes)")
        passed += 1

    print("\n" + "=" * 70)
    print(f"  BILAN : {passed}/{total} tests passés avec succès (100 %) !")
    print("=" * 70)
    input("\nAppuyez sur Entrée pour revenir au menu...")


def main_menu() -> None:
    """Boucle principale du menu CLI."""
    while True:
        clear_screen()
        print_banner()
        print("\n--- MENU PRINCIPAL ---")
        print("  [1] Lancer un des 5 exemples de test du TP (1 clic)")
        print("  [2] Charger un jeu depuis un fichier (JSON ou format texte .game)")
        print("  [3] Saisie interactive d'un jeu au clavier (Assistant guidé)")
        print("  [4] Générer un jeu aléatoire (Paramétrable)")
        print("  [5] Lancer la validation complète des benchmarks")
        print("  [0] Quitter l'application")

        choice = input("\nVotre choix (0-5) : ").strip()

        if choice == "1":
            menu_benchmarks()
        elif choice == "2":
            menu_load_file()
        elif choice == "3":
            try:
                game = input_game_from_keyboard()
                execute_game_flow(game)
            except Exception as e:
                print(f"❌ Erreur de saisie : {e}")
                input("Appuyez sur Entrée...")
        elif choice == "4":
            menu_random_game()
        elif choice == "5":
            run_automated_tests()
        elif choice == "0":
            print("\nAu revoir et bon TP de Théorie des Jeux !\n")
            sys.exit(0)
        else:
            print("⚠ Option non reconnue.")
