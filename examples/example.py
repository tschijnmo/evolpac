"""A simple example for the optimization of the killer PAC-mite."""

from evolpac.duel import run_tournament, eval_w_sample
from evolpac.evolve import evolve
from evolpac.genemanip import gen_random_gene


def main():
    """The main driver."""

    eval_sample = [gen_random_gene() for _ in range(5)]

    evolve(100, 5000, run_tournament, eval_cb=eval_w_sample(eval_sample),
           out_steps=100)


if __name__ == '__main__':
    main()
