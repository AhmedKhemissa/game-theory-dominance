"""Modèle de jeu fini sous forme normale pour N joueurs."""
from dataclasses import dataclass, field
import itertools
import math
from typing import Dict, List, Optional, Sequence, Tuple, Union


@dataclass
class NormalFormGame:
    """Représente un jeu fini sous forme normale avec N joueurs et stratégies pures."""
    players: List[str]
    strategies: Dict[str, List[str]]
    payoffs: Dict[Tuple[str, ...], Tuple[float, ...]]
    name: str = "Jeu en forme normale"
    description: str = ""

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        """Valide la cohérence interne du jeu."""
        if len(self.players) < 2:
            raise ValueError(f"Le jeu doit comporter au moins 2 joueurs (fourni: {len(self.players)}).")

        for p in self.players:
            if p not in self.strategies:
                raise ValueError(f"Aucune stratégie définie pour le joueur '{p}'.")
            if len(self.strategies[p]) < 1:
                raise ValueError(f"Le joueur '{p}' doit avoir au moins une stratégie.")

        # Vérification des profils complets
        all_strat_lists = [self.strategies[p] for p in self.players]
        expected_profiles = list(itertools.product(*all_strat_lists))
        expected_count = len(expected_profiles)

        # On vérifie que chaque profil a son vecteur de gains
        missing = [prof for prof in expected_profiles if prof not in self.payoffs]
        if missing:
            raise ValueError(
                f"{len(missing)} profils manquants dans les gains (ex: {missing[:3]}). "
                f"Profils attendus: {expected_count}, profils fournis: {len(self.payoffs)}."
            )

        for prof, pay in self.payoffs.items():
            if len(pay) != len(self.players):
                raise ValueError(
                    f"Le profil {prof} a {len(pay)} gains, attendu {len(self.players)}."
                )

    @property
    def num_players(self) -> int:
        """Nombre de joueurs."""
        return len(self.players)

    @property
    def shape(self) -> Tuple[int, ...]:
        """Nombre de stratégies actives actuelles par joueur."""
        return tuple(len(self.strategies[p]) for p in self.players)

    def get_player_index(self, player: str) -> int:
        """Retourne l'indice (0-based) du joueur."""
        return self.players.index(player)

    def get_opponents(self, player: str) -> List[str]:
        """Retourne la liste des joueurs adverses."""
        return [p for p in self.players if p != player]

    def get_opponents_profiles(self, player: str) -> List[Tuple[str, ...]]:
        """
        Retourne la liste ordonnée de tous les profils de stratégies actives
        des opposants S_{-i}.
        """
        opponents = self.get_opponents(player)
        opponents_strats = [self.strategies[p] for p in opponents]
        return list(itertools.product(*opponents_strats))

    def build_full_profile(
        self, player: str, strategy: str, opponent_profile: Sequence[str]
    ) -> Tuple[str, ...]:
        """
        Reconstitue le profil complet s = (s_1, ..., s_n) en insérant la stratégie
        du joueur à sa position d'origine parmi les stratégies adverses.
        """
        p_idx = self.get_player_index(player)
        full = list(opponent_profile)
        full.insert(p_idx, strategy)
        return tuple(full)

    def get_payoff(self, profile: Tuple[str, ...], player: Optional[str] = None) -> Union[Tuple[float, ...], float]:
        """Retourne le tuple de gains ou le gain individuel d'un joueur."""
        payoffs = self.payoffs[profile]
        if player is not None:
            return payoffs[self.get_player_index(player)]
        return payoffs

    def clone(self) -> "NormalFormGame":
        """Copie profonde propre du jeu et de ses stratégies actives."""
        return NormalFormGame(
            players=list(self.players),
            strategies={p: list(strats) for p, strats in self.strategies.items()},
            payoffs=dict(self.payoffs),
            name=self.name,
            description=self.description
        )

    def eliminate_strategy(self, player: str, strategy: str) -> "NormalFormGame":
        """
        Retourne une nouvelle instance de NormalFormGame où la stratégie donnée
        a été retirée des stratégies actives du joueur.
        """
        if strategy not in self.strategies[player]:
            raise ValueError(f"Stratégie '{strategy}' introuvable pour le joueur '{player}'.")
        if len(self.strategies[player]) <= 1:
            raise ValueError(
                f"Impossible de supprimer la dernière stratégie '{strategy}' du joueur '{player}'."
            )

        new_game = self.clone()
        new_game.strategies[player].remove(strategy)
        return new_game

    def is_terminal(self) -> bool:
        """Retourne True s'il reste exactement 1 stratégie par joueur."""
        return all(len(strats) == 1 for strats in self.strategies.values())

    def get_active_profile_count(self) -> int:
        """Nombre de profils encore actifs dans le jeu."""
        return math.prod(len(strats) for strats in self.strategies.values())

    def get_unique_profile(self) -> Optional[Tuple[str, ...]]:
        """Si terminal, retourne l'unique profil restant."""
        if self.is_terminal():
            return tuple(self.strategies[p][0] for p in self.players)
        return None

    def get_unique_payoffs(self) -> Optional[Tuple[float, ...]]:
        """Si terminal, retourne les gains associés à l'unique profil."""
        prof = self.get_unique_profile()
        if prof is not None:
            return self.payoffs[prof]
        return None
