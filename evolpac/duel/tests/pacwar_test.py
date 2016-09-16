"""Tests for the pacwar core."""

import unittest

from evolpac.duel._PyPacwar import battle

class CoreTest(unittest.TestCase):
    """Tests for the core C extension."""

    def test_one_three(self):
        """Test the battling between all 1 and all 3."""
        rounds, c1, c2 = battle([1] * 50, [3] * 50)

        self.assertEqual(rounds, 500)
        self.assertEqual(c1, c2)
        self.assertEqual(c1, 57)
