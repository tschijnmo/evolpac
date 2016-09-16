"""
Main driver function for a simple genetic algorithm.
"""

import json
import operator
import random

from .genemanip import gen_random_gene, cross, mutate


def evolve(
        pop_size, total_steps, score_cb, init=None,
        gene_length=50, gene_bits=(0, 1, 2, 3),
        select_ratio=0.4, new_ratio=0.1, breed_new_ratio=0.05,
        mutate_prob=0.001, n_cross_pts=1, n_mutate_pts=1,
        out_prefix='evolution', out_num=20, out_steps=1000, eval_cb=None
):
    """Perform the evolution optimization.

    In this simple genetic algorithm implementation, we start with a random
    population of the given size, to which some given elements can be added.
    Then the score call-back function is going to be called with the list of
    all such genes to get the list of pairs of score and the original genes.
    Then the ``select_ratio`` gives the ratio to be selected to breed.  The
    resulted evolved population is also able to have some newly generated new
    genes, controlled by ``new_ratio``. Mutation are only carried out to the
    new children.

    A given number of intermediate results can also be written to JSON files
    every any given number of steps.

    """

    # Population initialization.
    pop = []
    if init is not None:
        pop.extend(init)
    for _ in range(pop_size - len(pop)):
        pop.append(gen_random_gene(gene_length, selection=gene_bits))
        continue

    # Evolution main loop.
    select_num = int(pop_size * select_ratio)
    new_num = int(pop_size * new_ratio)
    breed_new_num = int(pop_size * breed_new_ratio)
    for step_idx in range(total_steps):

        # Compute scores.
        pop_w_score = score_cb(pop)
        pop_w_score.sort(
            key=operator.itemgetter(0), reversed=True
        )  # Skip genes for performance.

        # Select and output.
        pop = [i[1] for i in pop_w_score[0:select_num]]
        if step_idx % out_steps == 0 or step_idx == total_steps - 1:
            _dump_pop(
                pop[0:out_num], '-'.join([out_prefix, str(step_idx)]),
                eval_cb=eval_cb
            )

        # Add the new blood.
        for _ in range(new_num):
            pop.append(gen_random_gene(gene_length, selection=gene_bits))
            continue

        # Breed.
        parents = pop[0:select_num + breed_new_num]
        for _ in range(pop_size - len(pop)):
            parent1, parent2 = random.sample(parents, 2)
            desc = cross(parent1, parent2, n_pts=n_cross_pts)
            if random.random() < mutate_prob:
                mutate(desc, n_pts=n_mutate_pts, selection=gene_bits)
            pop.append(desc)

        continue

    return None


def _dump_pop(pop, file_name, eval_cb=None):
    """Dump the population into the given file."""
    if eval_cb is None:
        def eval_cb(genes):
            return ((None, i) for i in genes)

    with open(file_name + '.json', 'w') as out_fp:
        json.dump(
            [{'gene': gene, 'eval': eval} for eval, gene in eval_cb(pop)],
            out_fp
        )

    return None
