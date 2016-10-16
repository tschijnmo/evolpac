"""Functions for computing average score."""

import itertools

from .duel import duel


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
