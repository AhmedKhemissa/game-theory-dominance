# Rapport de Travaux Pratiques : Dominance Stricte et Faible en Théorie des Jeux
**Filière / Département IA&SD — Master 2**  
*MIV / Master 2 — Travaux Pratiques en Théorie des Jeux*

---

## 1. Objectifs du Projet

L'objectif de ce travail pratique est de développer un programme complet, modulaire et interactif en Python pour :
1. Représenter tout jeu fini sous forme normale comportant un nombre quelconque de joueurs $n \ge 2$ et un nombre quelconque de stratégies pures par joueur ($k_i \ge 1$).
2. Afficher la matrice des gains de manière claire et alignée :
   - Sous forme de matrice 2D classique pour $n = 2$ joueurs.
   - Sous forme de collection de sous-matrices 2D pour $n \ge 3$ joueurs, étiquetées pour chaque profil de stratégies des joueurs $3 \dots n$.
3. Réaliser la simplification du jeu par **élimination itérée des stratégies dominées** étape par étape :
   - En **dominance stricte** (IESDS - *Iterated Elimination of Strictly Dominated Strategies*).
   - En **dominance faible** (IEWDS - *Iterated Elimination of Weakly Dominated Strategies*).
4. Fournir une trace détaillée à chaque étape (joueur, stratégie éliminée, stratégie dominante, preuve mathématique et matrice actualisée) jusqu'à atteindre le point fixe minimal (idéalement un profil unique $1 \times \dots \times 1$).

---

## 2. Comment Lancer le Programme

L'application est immédiatement exécutable dans le terminal :

```bash
cd /Users/ahmed/.gemini/antigravity/scratch/game_theory_dominance

# 1. Lancement du menu interactif (Navigation intuitive) :
python3 run.py

# 2. Validation automatique immédiate des 5 exemples du sujet (en 1 frappe) :
python3 run.py --test

# 3. Exécution de la suite complète de 12 tests automatisés (avec Pytest) :
python3 run.py --pytest
```

---

## 3. Ce qui Fonctionne (Bilan des Exigences R1 à R6)

L'intégralité du cahier des charges est couverte à 100 % sans aucune régression :

| Réf. | Exigence du sujet | Statut | Détails de l'implémentation |
| :---: | :--- | :---: | :--- |
| **R1** | **Saisie du jeu** ($n$ joueurs, $k_i$ stratégies, 3 modes de saisie) | **FONCTIONNEL** | • **Clavier** : Assistant pas-à-pas guidé (`src/io/keyboard_input.py`).<br/>• **Fichier** : Chargeur JSON et format texte compact `.game` (`src/io/parser.py`).<br/>• **Aléatoire** : Générateur paramétrable avec bornes et graine (`src/io/random_generator.py`). |
| **R2** | **Affichage des matrices** ($n=2$ et $n \ge 3$) | **FONCTIONNEL** | • **2 joueurs** : Tableaux avec bordures Unicode soignées et alignement dynamique.<br/>• **$N \ge 3$ joueurs** : Découpage automatique en sous-matrices 2D ($J_1 \times J_2$) conditionnées par chaque combinaison des joueurs $3 \dots N$ (`src/display/matrix_formatter.py`). |
| **R3** | **Dominance stricte** | **FONCTIONNEL** | Détection exacte : $u_i(b, s_{-i}) > u_i(a, s_{-i})$ pour tout $s_{-i} \in S_{-i}$. |
| **R4** | **Dominance faible** | **FONCTIONNEL** | Détection exacte : $u_i(b, s_{-i}) \ge u_i(a, s_{-i})$ avec supériorité stricte pour au moins un profil adverse. Choix du mode au démarrage. |
| **R5** | **Élimination itérée avec trace** | **FONCTIONNEL** | Boucle jusqu'au point fixe affichant pour chaque étape : le joueur, la stratégie éliminée, la dominante, la preuve par profil et la matrice résultante. |
| **R6** | **Résultat final** | **FONCTIONNEL** | Affichage du jeu réduit et diagnostic formel : profil unique ($1 \times 1$) avec gains ou forme indécomposable. |

### Ce qui ne fonctionne pas
- **Aucun dysfonctionnement constaté.** Tous les cas limites (gains identiques, ordre d'élimination en dominance faible, jeux à 3 joueurs) ont été formellement validés par 12 tests automatisés.

---

## 4. Résultats Obtenus sur les 5 Jeux de Test

### Exemple 1 : Élimination stricte complète jusqu'à $1 \times 1$
- **Jeu initial** : 2 joueurs, $3 \times 3$, Joueur 1 $\{H, M, B\}$, Joueur 2 $\{G, C, D\}$.
- **Mode** : Dominance stricte.
- **Trace des étapes** :
  1. **Étape 1** : Pour le Joueur 2, la stratégie `D` est strictement dominée par `C` (et aussi par `G`). `D` est éliminée. Matrice $3 \times 2$.
  2. **Étape 2** : Pour le Joueur 1, la stratégie `M` est strictement dominée par `H` (car $3 > 1$ contre $G$ et $2 > 1$ contre $C$). `M` est éliminée. Matrice $2 \times 2$.
  3. **Étape 3** : Pour le Joueur 1, la stratégie `B` est strictement dominée par `H` (car $3 > 2$ contre $G$ et $2 > 0$ contre $C$). `B` est éliminée. Matrice $1 \times 2$.
  4. **Étape 4** : Pour le Joueur 2, sur la seule ligne restante $H$, la stratégie `G` est strictement dominée par `C` (car $3 > 1$). `G` est éliminée. Matrice $1 \times 1$.
- **Résultat final obtenu** :
  $$\text{Profil unique } (H, C) \quad \text{avec vecteur de gains } (2, 3)$$
- **Conformité** : **100 % conforme au sujet.**

---

### Exemple 2 : Élimination impossible (Pierre-Feuille-Ciseaux)
- **Jeu initial** : 2 joueurs, $3 \times 3$, jeu classique à somme nulle.
- **Mode** : Dominance stricte et dominance faible.
- **Résultat obtenu** :
  - En mode strict : 0 étape d'élimination.
  - En mode faible : 0 étape d'élimination.
  - Message affiché : *« Aucune élimination possible : le jeu reste inchangé (3 × 3). »*
- **Justification théorique** : Pour chaque paire de coups, l'un bat l'autre, l'autre fait match nul ou perd contre un troisième. Aucun coup ne surpasse un autre face à toutes les actions de l'adversaire.
- **Conformité** : **100 % conforme au sujet.**

---

### Exemple 3 : Dominance faible et sensibilité à l'ordre d'élimination
- **Jeu initial** : 2 joueurs, $2 \times 3$, Joueur 1 $\{H, B\}$, Joueur 2 $\{G, M, D\}$.

#### En mode dominance stricte :
- **Trace** : Pour le Joueur 2, `D` est strictement dominée par `G` ($1 > 0$ contre $H$ et $1 > 0$ contre $B$).
- Ensuite, sur la matrice $2 \times 2$ résiduelle, aucune stratégie n'est strictement dominée.
- **Résultat final** : Matrice $2 \times 2$ avec $\{H, B\} \times \{G, M\}$.

#### En mode dominance faible :
Le résultat dépend mathématiquement de l'ordre d'élimination suivi. Le programme propose les deux options :
1. **Ordre standard (Joueur 1 prioritaire)** :
   - Étape 1 : Joueur 1 élimine `B` (faiblement dominée par `H`, car $2 \ge 2$ et $2 > 1$ contre $M$).
   - Étape 2 : Joueur 2 élimine `D` (dominée par `G`).
   - Reste : Joueur 1 $\{H\}$, Joueur 2 $\{G, M\}$ avec gains $(2, 1)$ et $(2, 1)$. Gains identiques $\implies$ arrêt.
   - **Résultat** : $H \times \{G, M\}$.
2. **Ordre alternatif (Joueur 2 élimine $M$ en premier)** :
   - Étape 1 : Joueur 2 élimine `M` (faiblement dominée par `G`).
   - Étape 2 : Joueur 2 élimine `D` (dominée par `G`).
   - Reste : Joueur 1 $\{H, B\}$, Joueur 2 $\{G\}$ avec gains $(2, 1)$ et $(2, 1)$. Gains identiques $\implies$ arrêt.
   - **Résultat** : $\{H, B\} \times G$.
3. **Exploration arborescente complète (Option 2 du CLI)** :
   - L'algorithme DFS explore les deux branches et affiche les **deux jeux réduits possibles**, illustrant parfaitement la non-confluence de la dominance faible.
- **Conformité** : **100 % conforme au sujet.**

---

### Exemple 4 : Cas général à 3 joueurs (Biens Publics)
- **Jeu initial** : 3 joueurs, stratégies $\{C, N\}$ par joueur ($2 \times 2 \times 2 = 8$ profils).
- **Gain** : $u_i = 2 \times (\#C) - 3$ si $C$, et $2 \times (\#C)$ si $N$.
- **Affichage** : Le programme génère automatiquement 2 sous-matrices 2D ($J_1 \times J_2$) clairement étiquetées pour `Joueur 3 = 'C'` et `Joueur 3 = 'N'`.
- **Mode** : Dominance stricte.
- **Trace des étapes** :
  - Pour tout profil adverse des opposants où $k$ joueurs contribuent :
    $$u_i(N) - u_i(C) = 2k - (2(k+1) - 3) = 2k - (2k - 1) = +1 > 0$$
  - La stratégie `N` domine strictement `C` pour les 3 joueurs indépendamment.
  - Le programme élimine successivement `C` pour le Joueur 1, puis pour le Joueur 2, puis pour le Joueur 3 en 3 étapes.
- **Résultat final obtenu** :
  $$\text{Profil unique } (N, N, N) \quad \text{avec vecteur de gains } (0, 0, 0)$$
- **Conformité** : **100 % conforme au sujet.**

---

### Exemple 5 : Exercice 4 de la Série 1 ($3 \times 3$)
- **Jeu initial** : 2 joueurs, $3 \times 3$, Joueur 1 $\{A_1, A_2, A_3\}$, Joueur 2 $\{B_1, B_2, B_3\}$.
- **Mode** : Dominance stricte et dominance faible.
- **Trace des 4 tours** :
  - **Tour 1** : Joueur 2 élimine `B2` (strictement dominée par `B3` car $11 > 9$, $4 > 3$, $3 > 1$).
  - **Tour 2** : Joueur 1 élimine `A2` (strictement dominée par `A1` car $10 > 5$ et $4 > 3$).
  - **Tour 3** : Joueur 2 élimine `B1` (strictement dominée par `B3` car $11 > 10$ et $3 > 0$).
  - **Tour 4** : Joueur 1 élimine `A1` (strictement dominée par `A3` car $5 > 4$).
- **Résultat final obtenu** :
  $$\text{Profil unique } (A_3, B_3) \quad \text{avec vecteur de gains } (5, 3)$$
- **Conformité** : **100 % conforme au sujet (exactement 4 étapes alternées).**

---

## 5. Synthèse des Résultats des Jeux de Test

| Jeu | Mode | Résultat Théorique Attendu | Résultat Obtenu par le Programme | Statut |
| :--- | :---: | :--- | :--- | :---: |
| **Exemple 1** | Strict | Profil unique $(H, C)$, gains $(2, 3)$ | Profil unique $(H, C)$, gains $(2, 3)$ | **VALIDE** |
| **Exemple 2** | Strict / Faible | Aucune élimination, matrice $3 \times 3$ inchangée | Aucune élimination, matrice $3 \times 3$ inchangée | **VALIDE** |
| **Exemple 3** | Strict | $D$ supprimée, reste matrice $2 \times 2$ $\{H, B\} \times \{G, M\}$ | $D$ supprimée, reste matrice $2 \times 2$ $\{H, B\} \times \{G, M\}$ | **VALIDE** |
| **Exemple 3** | Faible | $H \times \{G, M\}$ ou $\{H, B\} \times G$ selon l'ordre | Les deux équilibres trouvés selon l'ordre ou par arbre | **VALIDE** |
| **Exemple 4** (3 joueurs) | Strict | Profil unique $(N, N, N)$, gains $(0, 0, 0)$ | Profil unique $(N, N, N)$, gains $(0, 0, 0)$ | **VALIDE** |
| **Exemple 5** (Série 1) | Strict / Faible | Profil unique $(A_3, B_3)$, gains $(5, 3)$ | Profil unique $(A_3, B_3)$, gains $(5, 3)$ en 4 étapes | **VALIDE** |

---

## 6. Analyse Théorique et Points Clés d'Implémentation

### 1. Prise en compte de la convention des gains identiques
Le sujet spécifie formellement : *« Deux stratégies ayant exactement les mêmes gains ne se dominent pas l'une l'autre. »*
Dans notre implémentation (`src/solvers/dominance.py`), le prédicat de dominance faible exige explicitement l'accumulation d'au moins une supériorité stricte (`has_strict_advantage = True`). Si tous les gains sont égaux, la fonction retourne `False`. Cela empêche toute élimination cyclique ou arbitraire de stratégies équivalentes.

### 2. Robustesse numérique (Flottants IEEE 754)
Toutes les comparaisons de gains utilisent un seuil de précision $\epsilon = 10^{-9}$ :
- Supériorité stricte : $u_b - u_a > \epsilon$
- Supériorité ou égalité : $u_b - u_a \ge -\epsilon$
Cela garantit une insensibilité totale aux micro-imprécisions de calcul flottant.

### 3. Gestion immuable des jeux pour $N$ dimensions
Plutôt que d'altérer physiquement les dimensions des tenseurs NumPy (ce qui décalerait les indices numériques et rendrait le traçage opaque), chaque état de jeu maintient la liste des stratégies actives par joueur. Les suppressions se font en $\mathcal{O}(1)$ et chaque étape conserve un instantané complet et immuable du jeu, permettant le replay et le branching.

---

## 7. Conclusion

Le programme développé constitue une solution logicielle industrielle et pédagogique complète pour l'étude de l'élimination itérée des stratégies dominées. Il allie rigueur mathématique, clarté d'affichage (2D et $N \ge 3$), ergonomie interactive et validation automatique exhaustive.
