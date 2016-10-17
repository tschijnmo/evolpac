"""Manipulation utilities for the genes."""

import random

import numpy as np
import numpy.random as nprandom


GENE_LOW = 0
GENE_HIGH = 4
GENE_BITS = (0, 1, 2, 3)
GENE_LENGTH = 50
GENE_DT = np.byte


def cross(gene1, gene2, n_pts=1):
    """Crosses two genes over by the given number of points.

    The crossover points will be randomly selected.
    """

    assert len(gene1) == GENE_LENGTH
    assert len(gene2) == GENE_LENGTH

    points = random.sample(range(GENE_LENGTH), n_pts)
    points.sort()
    points.append(GENE_LENGTH)

    res1 = []
    res2 = []

    curr1 = res1
    curr2 = res2
    cross_idx = 0
    next_cross = points[cross_idx]

    # The first is always kept in place, since swapping them is pointless.
    for i in range(0, GENE_LENGTH):
        curr1.append(gene1[i])
        curr2.append(gene2[i])
        if i == next_cross:
            cross_idx += 1
            next_cross = points[cross_idx]
            curr1, curr2 = curr2, curr1
        continue

    return res1, res2


def mutate(gene, n_pts=1):
    """Mutate the given gene by uniform selection.

    Note that this subroutine directly manipulates the gene.
    """

    pts = random.sample(range(len(gene)), n_pts)
    for i in pts:
        gene[i] = random.choice(GENE_BITS)
        continue
    return gene


def gen_random_gene():
    """Generate a random gene."""
    return nprandom.randint(
        GENE_LOW, GENE_HIGH, size=GENE_LENGTH, dtype=GENE_DT
    )


def get_gene_from_str(s):
    """Generates a gene value from a string."""
    res = [int(i) for i in s]
    assert len(res) == GENE_LENGTH
    assert all(GENE_LOW <= i and i < GENE_HIGH for i in res)
    return res
