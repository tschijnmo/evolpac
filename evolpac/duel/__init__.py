"""Duelling between PAC-mites."""

import itertools

import numpy as np

from .duel import battle
from .tournament import run_tournament


def run_duel(gene1, gene2):
    """Perform duel between the two given genes.

    The score for them will be returned according to the course website_.

    .. website_:  https://www.clear.rice.edu/comp440/modules/termproject
    """

    rounds, c1, c2 = battle(gene1, gene2)

    if c1 >= c2:
        win_c, los_c = c1, c2
        gene1_wins = True
    else:
        win_c, los_c = c2, c1
        gene1_wins = False

    # Accumulate the points according to the rules.
    if los_c == 0:
        if rounds < 100:
            win_p, los_p = 20, 0
        elif rounds < 200:
            win_p, los_p = 19, 1
        elif rounds < 300:
            win_p, los_p = 18, 2
        else:
            win_p, los_p = 17, 3
        assert rounds <= 500
    else:
        ratio = float(win_c) / los_c
        if ratio >= 10:
            win_p, los_p = 13, 7
        elif ratio >= 3:
            win_p, los_p = 12, 8
        elif ratio >= 1.5:
            win_p, los_p = 11, 9
        else:
            win_p, los_p = 10, 10

    if gene1_wins:
        return win_p, los_p
    else:
        return los_p, win_p


def run_tournament_(genes):
    """Run tournaments in Python.

    This is a poor man's version of tournament mainly for testing purpose.
    """

    n_genes = len(genes)
    scores = np.zeros(n_genes, dtype=np.uint)
    for i, j in itertools.combinations(range(n_genes), 2):
        s_i, s_j = run_duel(genes[i], genes[j])
        scores[i] += s_i
        scores[j] += s_j
        continue

    return scores
