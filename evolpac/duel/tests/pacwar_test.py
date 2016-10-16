"""Tests for the pacwar core."""

import unittest

import numpy as np

from evolpac.duel.duel import battle
from evolpac.duel import run_duel, run_tournament, run_tournament_
from evolpac.genemanip import gen_random_gene

class CoreTest(unittest.TestCase):
    """Tests for the core C extension."""

    def test_one_three(self):
        """Test the battling between all 1 and all 3."""
        rounds, c1, c2 = battle([1] * 50, [3] * 50)

        self.assertEqual(rounds, 500)
        self.assertEqual(c1, c2)
        self.assertEqual(c1, 57)

    def test_duel_tour(self):
        """Test duel and tournament has same result."""
        genes_duel = [[1] * 50, [3] * 50]
        genes_tour = np.array(genes_duel, dtype=np.byte)

        duel_res = run_duel(*genes_duel)
        tour_res = run_tournament(genes_tour)

        for i in range(0, 2):
            self.assertEqual(duel_res[i], tour_res[i])

    def test_tour(self):
        """Tests the C and Python version of tournament."""
        n_genes = 10
        genes = np.array(
            [gen_random_gene() for _ in range(n_genes)],
            dtype=np.byte
        )

        c_res = run_tournament(genes)
        python_res = run_tournament_(genes)
        diff = c_res - python_res

        self.assertFalse(diff.any())

