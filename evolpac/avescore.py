"""Functions for computing average score."""

import itertools

from .duel import duel


def compute_cross_ave_score(genes):
    """Computes the cross average score of all duels among the genes."""

    n_genes = len(genes)
    scores = [0 for _ in genes]
    for i, j in itertools.combinations(range(n_genes), 2):
        s_i, s_j = duel(genes[i], genes[j])
        scores[i] += s_i
        scores[j] += s_j
        continue

    factor = 1.0 / (n_genes - 1)
    return [
        (i * factor, j) for i, j in zip(scores, genes)
        ]


def compute_ave_score_w_sample(genes, samples):
    """Computes the average score for duelling with a random sample."""

    scores = [0 for _ in genes]
    for i, v in enumerate(genes):
        for j in samples:
            score, _ = duel(v, j)
            scores[i] += score
            continue
        continue

    factor = 1.0 / len(samples)
    return [
        (i * factor, j) for i, j in zip(scores, genes)
        ]
