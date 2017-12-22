"""

.. moduleauthor:: Fabian Ball <fabian.ball@kit.edu>
"""
from __future__ import absolute_import, division
from unittest import TestCase
from unittest.util import safe_repr

from pycggcrg import run_rg, run_cggcrg, run_cggcirg, make_graph


class TestCGGCRGApi(TestCase):
    def assertAlmostIn(self, member, container, places=None, msg=None, delta=None):
        for container_member in container:
            try:
                self.assertAlmostEqual(member, container_member, places=places, msg=msg, delta=delta)
            except self.failureException:
                pass
            else:
                return  # Found, no further checks

        # Taken from TestCase.assertIn:
        standard_msg = '%s not found in %s (with tolerance)' % (safe_repr(member), safe_repr(container))
        self.fail(self._formatMessage(msg, standard_msg))

    # def test_loops(self):
    #     data = [
    #         ((2, [(0, 0), (0, 1), (1, 1)]), 0)
    #     ]
    #
    #     for params in data:
    #         self.assertEqual(run_rg(RGGraph(*params[0])), params[1])

    def test_complete(self):
        N = 10
        for n in range(2, N + 1):
            g = make_graph(n, [(u, v) for u in range(n) for v in range(u + 1, n)])

            self.assertEqual(g.m, n * (n - 1) / 2)

            self.assertAlmostEqual(run_rg(g, sample_size=1), 0)
            self.assertAlmostEqual(run_cggcrg(g), 0)
            self.assertAlmostEqual(run_cggcirg(g), 0)

    def test_butterfly(self):
        g = make_graph(5, [(0, 1), (0, 2), (1, 2), (2, 3), (2, 4), (3, 4)])

        self.assertAlmostIn(run_rg(g, sample_size=1), (1 / 9, 0))
        self.assertAlmostIn(run_cggcrg(g), (1 / 9, 0))
        self.assertAlmostIn(run_cggcirg(g), (1 / 9, 0))

        # Test the correct randomization by sampling
        # - 4 of 5 results should find the global maximum of 1/9
        # - 1 of 5 results finds the local maximum 0
        # => The exact mean is 4/5 * 1/9 = 4/45
        exact_mean = 4 / 45  # This is the exact mean modularity, determined by analyzing all join paths
        alpha = 10 ** -1  # Some test tolerance

        s = 100
        q_sum = 0
        for _ in range(s):
            q = run_rg(g, sample_size=1)
            q_sum += q

        mean_q = q_sum / s

        self.assertTrue(exact_mean - alpha <= mean_q <= exact_mean + alpha)

    def test_karate(self):
        g = make_graph(34, [(0, 31), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 10),
                            (0, 11), (0, 12), (0, 13), (0, 17), (0, 19), (0, 21), (1, 2), (1, 3), (1, 7),
                            (1, 13), (1, 17), (1, 19), (1, 21), (1, 30), (2, 3), (2, 32), (2, 7), (2, 8),
                            (2, 9), (2, 13), (2, 27), (2, 28), (3, 7), (3, 12), (3, 13), (4, 10), (4, 6),
                            (5, 6), (5, 10), (5, 16), (6, 16), (8, 30), (8, 33), (8, 32), (9, 33), (13, 33),
                            (14, 32), (14, 33), (15, 32), (15, 33), (18, 32), (18, 33), (19, 33), (20, 32),
                            (20, 33), (22, 32), (22, 33), (23, 32), (23, 25), (23, 27), (23, 33), (23, 29),
                            (24, 31), (24, 25), (24, 27), (25, 31), (26, 33), (26, 29), (27, 33), (28, 31),
                            (28, 33), (29, 32), (29, 33), (30, 33), (30, 32), (31, 32), (31, 33), (32, 33)])

        lower = 0.35  # Guessed value
        upper = 0.4197897  # Analytic result (global maximum), rounded up
        self.assertTrue(lower <= run_rg(g, sample_size=1) <= upper)
        self.assertTrue(lower <= run_cggcrg(g) <= upper)
        self.assertTrue(lower <= run_cggcirg(g) <= upper)
