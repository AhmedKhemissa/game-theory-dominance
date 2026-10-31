# TP Théorie des Jeux : Dominance Stricte et Dominance Faible
**Master 2 IA&SD — Département Informatique / FI**

Application modulaire et interactive en Python pour l'analyse et la résolution de jeux finis sous forme normale à $N$ joueurs par **élimination itérée des stratégies dominées** (strictes et faibles), avec traçage pas-à-pas et affichage matriciel soigné.

---

## 1. Fonctionnalités Implémentées

Le programme satisfait l'intégralité des exigences **R1 à R6** du cahier des charges :

- **R1. Saisie du jeu** :
  - **Saisie interactive au clavier** : Assistant guidé pas-à-pas avec valeurs par défaut et contrôle des erreurs.
  - **Fichiers structurés** : Import et export automatiques au format **JSON** ou format texte compact **`.game`**.
  - **Génération aléatoire** : Paramétrable par nombre de joueurs, nombre de stratégies par joueur ($k_i$), intervalle de gains $[u_{\min}, u_{\max}]$ et graine de reproductibilité (`seed`).
- **R2. Affichage matriciel** :
  - **Pour 2 joueurs** : Tableaux 2D avec bordures Unicode soignées, Joueur 1 en lignes, Joueur 2 en colonnes, cellules au format $(u_1, u_2)$.
  - **Pour $N \ge 3$ joueurs** : Découpage automatique en sous-matrices 2D pour les Joueurs 1 et 2, itérées et clairement étiquetées pour chaque combinaison possible des stratégies des Joueurs $3 \dots N$.
- **R3. Dominance stricte (IESDS)** : Détection et élimination des stratégies vérifiant $\forall s_{-i}, u_i(b, s_{-i}) > u_i(a, s_{-i})$.
- **R4. Dominance faible (IEWDS)** : Détection et élimination des stratégies vérifiant $\forall s_{-i}, u_i(b, s_{-i}) \ge u_i(a, s_{-i})$ avec au moins une inégalité stricte.
- **R5. Élimination itérée avec trace** :
  - Affichage à chaque tour du joueur concerné et de la stratégie éliminée.
  - Identification de la stratégie dominante.
  - Preuve mathématique complète (comparaison gain par gain pour chaque profil adverse $s_{-i}$).
  - Affichage de la matrice mise à jour après élimination.
- **R6. Résultat final** :
  - Affichage clair du jeu réduit résiduel.
  - Indication explicite si le jeu est réduit à un **profil unique** (matrice $1 \times \dots \times 1$) avec son vecteur de gains, ou s'il s'agit d'une forme indécomposable.
- **Bonus : Exploration arborescente (Branching DFS)** :
  - Permet d'explorer toutes les trajectoires possibles en dominance faible (non-confluence) pour trouver tous les équilibres terminaux possibles (Exemple 3).

---

## 2. Installation et Prérequis

Le projet requiert **Python 3.9+** et les bibliothèques `numpy` et `pytest` (optionnel pour les tests).

```bash
cd /Users/ahmed/.gemini/antigravity/scratch/game_theory_dominance
pip install -r requirements.txt
```

---

## 3. Utilisation

### Mode Interactif (Menu Principal)
Lancez simplement l'application via :
```bash
python3 run.py
```

Le menu interactif propose :
1. **Lancer un des 5 exemples de test du TP** (en 1 clic).
2. **Charger un jeu depuis un fichier** (JSON ou `.game`).
3. **Saisie interactive d'un jeu au clavier**.
4. **Générer un jeu aléatoire**.
5. **Lancer la validation complète des benchmarks**.

### Mode Ligne de Commande (Tests et Intégration)
```bash
# Lancer la validation interne des 5 benchmarks officiels :
python3 run.py --test

# Lancer la suite de tests unitaires et d'intégration avec pytest :
python3 run.py --pytest
```

---

## 4. Organisation du Projet

```
game_theory_dominance/
├── README.md                          # Documentation utilisateur et technique
├── RAPPORT_TP.md                      # Rapport académique d'analyse et résultats
├── requirements.txt                   # Dépendances Python (numpy, pytest)
├── run.py                             # Point d'entrée principal exécutable
├── data/                              # Fichiers de données des 5 benchmarks
│   ├── exemple_1.json                 # Exemple 1 : Stricte -> (H, C)
│   ├── exemple_2_pfc.json             # Exemple 2 : Chifoumi -> Inchangé
│   ├── exemple_3_ordre.json           # Exemple 3 : Dépendance de l'ordre
│   ├── exemple_4_trois_joueurs.json   # Exemple 4 : Cas 3 joueurs -> (N, N, N)
│   ├── exemple_5_serie1.json          # Exemple 5 : Série 1 Ex 4 -> (A3, B3)
│   └── exemple_1.game                 # Exemple 1 au format texte compact
├── src/
│   ├── models/                        # Modèle Game et structures d'étapes (TraceStep)
│   │   ├── game.py
│   │   └── step.py
│   ├── solvers/                       # Moteur de dominance et élimination itérée
│   │   ├── dominance.py
│   │   └── eliminator.py
│   ├── display/                       # Formateur matriciel 2D et N-joueurs
│   │   └── matrix_formatter.py
│   ├── io/                            # Gestionnaires d'entrées (JSON, Clavier, Random)
│   │   ├── parser.py
│   │   ├── keyboard_input.py
│   │   └── random_generator.py
│   ├── benchmarks/                    # Définitions intégrées des 5 exemples officiels
│   │   └── tp_benchmarks.py
│   └── cli/                           # Menu interactif et expérience utilisateur
│       └── menu.py
└── tests/                             # Suite de tests automatisés (12 tests)
    ├── test_benchmarks.py
    ├── test_dominance_rules.py
    └── test_data_files.py
```

---

## 5. Formats de Fichiers Reconnus

### Format JSON (`.json`)
```json
{
  "name": "Exemple 1",
  "players": ["Joueur 1", "Joueur 2"],
  "strategies": {
    "Joueur 1": ["H", "M", "B"],
    "Joueur 2": ["G", "C", "D"]
  },
  "payoffs": {
    "H, G": [3, 1],
    "H, C": [2, 3],
    "H, D": [0, 0],
    "M, G": [1, 2],
    "M, C": [1, 2],
    "M, D": [5, 1],
    "B, G": [2, 2],
    "B, C": [0, 1],
    "B, D": [1, 0]
  }
}
```

### Format Texte Compact (`.game`)
```text
NAME: Mon Jeu
PLAYERS: Joueur 1, Joueur 2
STRATEGIES Joueur 1: H, B
STRATEGIES Joueur 2: G, D
PAYOFFS:
H, G -> 3, 1
H, D -> 0, 0
B, G -> 2, 2
B, D -> 1, 0
```
