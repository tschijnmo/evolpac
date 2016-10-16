"""
Main driver function for a simple genetic algorithm.
"""

import itertools
import json
import random

import numpy as np

from .genemanip import (
    gen_random_gene, cross, mutate, GENE_LENGTH, GENE_DT
)


def evolve(
        pop_size, total_steps, score_cb, init=None,
        select_ratio=0.4, new_ratio=0.1,
        breed_new_ratio=0.05, n_cross_pts=1,
        mutate_prob=0.001, n_mutate_pts=1,
        out_prefix='evolution', out_num=20, out_steps=1000, eval_cb=None
):
    """Perform the evolution optimization.

    In this simple genetic algorithm implementation, a group of Pac-mite genes
    are going to be stored in an Nx50 numpy byte array.  We start with a random
    population of the given size, to which some initial elements can be added.
    Then the score call-back function is going to be called with this array of
    genes to get a sequence of score for each of them.  Then the
    ``select_ratio`` gives the ratio to be selected to breed.  The resulted
    evolved population is also able to have some newly generated new genes,
    controlled by ``new_ratio``.  Mutation are only carried out to the new
    children.

    A given number of intermediate results can also be written to JSON files
    every any given number of steps.

    """

    # Population initialization.
    pop = np.empty((pop_size, GENE_LENGTH), dtype=GENE_DT)
    if init is not None:
        init = []
    for i, j in itertools.zip_longest(range(pop_size), init):
        pop[i] = j if j is not None else gen_random_gene()

    # Convert the ratios to integral numbers.
    select_num = int(pop_size * select_ratio)
    new_num = int(pop_size * new_ratio)
    desc_pairs_num, rem = divmod(pop_size - select_num - new_num, 2)
    select_num += rem
    breed_new_num = int(new_num * breed_new_ratio)

    # Evolution main loop.
    for step_idx in range(total_steps):

        # Compute scores.
        scores = score_cb(pop)
        gene_idxes = list(range(pop_size))
        gene_idxes.sort(key=lambda x: scores[x])

        # Output.
        if step_idx % out_steps == 0 or step_idx == total_steps - 1:
            out_idxes = np.array(gene_idxes[-out_num:])
            _dump_pop(
                pop[out_idxes], scores[out_idxes],
                '-'.join([out_prefix, str(step_idx)]),
                eval_cb=eval_cb
            )

        # Gene_idxes will be used as a stack for filling the population.
        parents = list(gene_idxes[-select_num:])
        del gene_idxes[-select_num:]

        # Add the new blood.
        for i in range(new_num):
            idx = gene_idxes.pop()
            pop[idx] = gen_random_gene()
            if i < breed_new_num:
                parents.append(idx)

        # Breed.
        for _ in range(desc_pairs_num):
            parent1, parent2 = random.sample(parents, 2)
            descs = cross(pop[parent1], pop[parent2], n_pts=n_cross_pts)
            for i in descs:
                if random.random() < mutate_prob:
                    mutate(i, n_pts=n_mutate_pts)
            pop[gene_idxes.pop()] = descs[0]
            pop[gene_idxes.pop()] = descs[1]

        assert len(gene_idxes) == 0
        continue

    return None


def _dump_pop(pop, scores, file_name, eval_cb=None):
    """Dump the population into the given file."""

    if eval_cb is None:
        evals = [None for _ in pop]
    else:
        evals = eval_cb(pop)

    res = [
        {'gene': i, 'score': j, 'eval': k}
        for i, j, k in zip(pop, scores, evals)
        ]

    with open(file_name + '.json', 'w') as out_fp:
        json.dump(res, out_fp)

    return None
