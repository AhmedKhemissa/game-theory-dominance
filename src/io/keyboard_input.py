"""Assistant interactif de saisie d'un jeu au clavier (Exigence R1)."""
import itertools
from typing import Dict, List, Tuple

from ..models.game import NormalFormGame


def prompt_int(prompt: str, min_val: int = 1, default: int = 1) -> int:
    """Demande un entier valide à l'utilisateur."""
    while True:
        raw = input(f"{prompt} [{default}] : ").strip()
        if not raw:
            return default
        try:
            val = int(raw)
            if val < min_val:
                print(f"  ⚠ Veuillez entrer un entier >= {min_val}.")
                continue
            return val
        except ValueError:
            print("  ⚠ Valeur invalide, veuillez entrer un nombre entier.")


def prompt_float_vector(prompt: str, expected_len: int) -> Tuple[float, ...]:
    """Demande un vecteur de gains séparés par des virgules ou espaces."""
    while True:
        raw = input(f"{prompt} (ex: 3, 1) : ").strip()
        if not raw:
            print(f"  ⚠ Entrez {expected_len} gains.")
            continue
        # Découpage par virgule ou espace
        parts = [p.strip() for p in raw.replace(",", " ").split() if p.strip()]
        if len(parts) != expected_len:
            print(f"  ⚠ Attendu : {expected_len} valeurs de gains, reçu : {len(parts)}.")
            continue
        try:
            return tuple(float(x) for x in parts)
        except ValueError:
            print("  ⚠ Tous les gains doivent être des nombres réels (ex: 2 ou -1.5).")


def input_game_from_keyboard() -> NormalFormGame:
    """Guide l'utilisateur pas-à-pas pour saisir un jeu complet sous forme normale."""
    print("\n" + "=" * 65)
    print("   ASSISTANT DE SAISIE INTERACTIVE D'UN JEU SOUS FORME NORMALE")
    print("=" * 65)

    name = input("Nom du jeu [Mon Jeu] : ").strip() or "Mon Jeu"

    # 1. Nombre de joueurs
    n_players = prompt_int("Nombre de joueurs n", min_val=2, default=2)

    players: List[str] = []
    print("\n--- Noms des joueurs ---")
    for i in range(1, n_players + 1):
        def_name = f"Joueur {i}"
        p_name = input(f"Nom du joueur {i} [{def_name}] : ").strip() or def_name
        players.append(p_name)

    # 2. Nombre de stratégies par joueur
    strategies: Dict[str, List[str]] = {}
    print("\n--- Stratégies par joueur ---")
    for i, p in enumerate(players):
        k = prompt_int(f"Nombre de stratégies pour '{p}'", min_val=1, default=2)
        p_strats: List[str] = []
        for s_idx in range(1, k + 1):
            def_strat = f"S{s_idx}" if n_players > 2 else ("H" if s_idx == 1 and i == 0 else ("B" if s_idx == 2 and i == 0 else f"S{s_idx}"))
            s_name = input(f"  Stratégie {s_idx} pour '{p}' [{def_strat}] : ").strip() or def_strat
            p_strats.append(s_name)
        strategies[p] = p_strats

    # 3. Saisie des gains pour chaque profil cartésien
    all_strats_list = [strategies[p] for p in players]
    all_profiles = list(itertools.product(*all_strats_list))
    total_profiles = len(all_profiles)

    print(f"\n--- Saisie des gains ({total_profiles} profils au total) ---")
    print(f"Pour chaque profil, entrez les {n_players} gains dans l'ordre : ({', '.join(players)})")

    payoffs: Dict[Tuple[str, ...], Tuple[float, ...]] = {}
    for idx, prof in enumerate(all_profiles, start=1):
        prof_display = ", ".join(f"{players[i]}={prof[i]}" for i in range(n_players))
        prompt_str = f"  [{idx}/{total_profiles}] Gains pour ({prof_display})"
        payoffs[prof] = prompt_float_vector(prompt_str, n_players)

    print("\n✔ Saisie terminée avec succès !")
    return NormalFormGame(
        players=players,
        strategies=strategies,
        payoffs=payoffs,
        name=name,
        description="Saisie manuelle au clavier",
    )
