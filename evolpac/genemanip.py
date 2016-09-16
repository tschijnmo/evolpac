"""Manipulation utilities for the genes."""

import random


def cross(gene1, gene2, n_pts=1):
    """Crosses two genes over by the given number of points.

    The crossover points will be randomly selected.
    """

    size = len(gene1)
    assert len(gene2) == size

    points = random.sample(range(size), n_pts)
    points.sort()
    points.append(size)

    res1 = []
    res2 = []

    curr1 = res1
    curr2 = res2
    cross_idx = 0
    next_cross = points[cross_idx]

    # The first is always kept in place, since swapping them is pointless.
    for i in range(0, size):
        curr1.append(gene1[i])
        curr2.append(gene2[i])
        if i == next_cross:
            cross_idx += 1
            next_cross = points[cross_idx]
            curr1, curr2 = curr2, curr1
        continue

    return res1, res2


def mutate(gene, n_pts=1, selection=(0, 1, 2, 3)):
    """Mutate the given gene by uniform selection.

    Note that this subroutine directly manipulates the gene.
    """

    pts = random.sample(range(len(gene)), n_pts)
    for i in pts:
        gene[i] = random.choice(selection)
        continue
    return gene


def gen_random_gene(length, selection=(0, 1, 2, 3)):
    """Generate a random gene."""

    res = []
    for i in range(0, length):
        res.append(random.choice(selection))
        continue
    return res
