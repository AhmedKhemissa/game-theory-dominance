"""Module de chargement et sauvegarde des jeux (JSON et texte structuré)."""
import json
import os
import re
from typing import Any, Dict, List, Tuple

from ..models.game import NormalFormGame


def load_json_game(file_path: str) -> NormalFormGame:
    """Charge un jeu depuis un fichier JSON."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Le fichier '{file_path}' n'existe pas.")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    name = data.get("name", os.path.basename(file_path))
    description = data.get("description", "")
    players: List[str] = data["players"]
    strategies: Dict[str, List[str]] = data["strategies"]

    raw_payoffs = data["payoffs"]
    payoffs: Dict[Tuple[str, ...], Tuple[float, ...]] = {}

    for key_str, pay_val in raw_payoffs.items():
        # Clé attendue : "H, G" ou "C, C, C" ou tuple JSON
        if isinstance(key_str, str):
            profile_tuple = tuple(s.strip() for s in key_str.split(","))
        elif isinstance(key_str, (list, tuple)):
            profile_tuple = tuple(key_str)
        else:
            raise ValueError(f"Format de clé de profil non reconnu : {key_str}")

        payoffs[profile_tuple] = tuple(float(v) for v in pay_val)

    return NormalFormGame(
        players=players,
        strategies=strategies,
        payoffs=payoffs,
        name=name,
        description=description,
    )


def save_json_game(game: NormalFormGame, file_path: str) -> None:
    """Sauvegarde une instance de NormalFormGame au format JSON."""
    data = {
        "name": game.name,
        "description": game.description,
        "players": game.players,
        "strategies": game.strategies,
        "payoffs": {
            ", ".join(prof): list(pay) for prof, pay in game.payoffs.items()
        },
    }

    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_text_game(file_path: str) -> NormalFormGame:
    """
    Charge un jeu depuis un fichier texte structuré (.game).
    Format :
        NAME: Mon Jeu
        PLAYERS: J1, J2
        STRATEGIES J1: A, B
        STRATEGIES J2: C, D
        PAYOFFS:
        A, C -> 3, 1
        A, D -> 0, 2
        ...
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Le fichier '{file_path}' n'existe pas.")

    name = "Jeu Texte"
    description = ""
    players: List[str] = []
    strategies: Dict[str, List[str]] = {}
    payoffs: Dict[Tuple[str, ...], Tuple[float, ...]] = {}

    in_payoffs = False

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.upper().startswith("NAME:"):
                name = line.split(":", 1)[1].strip()
            elif line.upper().startswith("DESCRIPTION:"):
                description = line.split(":", 1)[1].strip()
            elif line.upper().startswith("PLAYERS:"):
                raw_p = line.split(":", 1)[1]
                players = [p.strip() for p in raw_p.split(",") if p.strip()]
            elif line.upper().startswith("STRATEGIES"):
                m = re.match(r"STRATEGIES\s+([^:]+):(.*)", line, re.IGNORECASE)
                if m:
                    p_name = m.group(1).strip()
                    s_list = [s.strip() for s in m.group(2).split(",") if s.strip()]
                    strategies[p_name] = s_list
            elif line.upper().startswith("PAYOFFS:"):
                in_payoffs = True
            elif in_payoffs and "->" in line:
                prof_part, pay_part = line.split("->", 1)
                prof = tuple(s.strip() for s in prof_part.split(",") if s.strip())
                pay = tuple(float(v.strip()) for v in pay_part.split(",") if v.strip())
                payoffs[prof] = pay

    return NormalFormGame(
        players=players,
        strategies=strategies,
        payoffs=payoffs,
        name=name,
        description=description,
    )


def load_game_file(file_path: str) -> NormalFormGame:
    """Charge automatiquement un jeu selon l'extension du fichier (.json ou .game / .txt)."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".json":
        return load_json_game(file_path)
    else:
        return load_text_game(file_path)
