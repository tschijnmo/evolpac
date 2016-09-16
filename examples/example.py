"""A simple example for the optimization of the killer PAC-mite."""

import functools

from evolpac.avescore import compute_cross_ave_score, compute_ave_score_w_sample
from evolpac.evolve import evolve
from evolpac.genemanip import gen_random_gene


def main():
    """The main driver."""

    eval_sample = [gen_random_gene(50) for _ in range(5)]

    evolve(100, 100, compute_cross_ave_score, eval_cb=functools.partial(
        compute_ave_score_w_sample, samples=eval_sample
    ))


if __name__ == '__main__':
    main()
