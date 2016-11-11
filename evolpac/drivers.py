"""
Some driver functions for the evolution algorithm
=================================================

This module contains some simple driver functions that do some kind of
high-level jobs.

"""

from evolpac.avescore import compute_cross_ave_score

from evolpac.evolve import evolve
from evolpac.genemanip import form_gene_str, write_gene_strs


def form_pool(num, out_fp,
              pop_size=100, evol_steps=200, score_cb=compute_cross_ave_score,
              **kwargs):
    """Form a pool of winners from random initial pool."""

    n_found = 0
    while n_found < num:
        res = evolve(
            pop_size, evol_steps, score_cb,
            out_prefix=None, **kwargs
        )

        # Get only the unique genes to write.
        res_strs = set(form_gene_str(i) for i in res)
        write_gene_strs(res_strs, out_fp)

        n_found += len(res_strs)

    return
