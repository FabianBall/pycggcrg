"""

.. moduleauthor:: Fabian Ball <fabian.ball@kit.edu>
"""
from __future__ import absolute_import, division
from unittest import TestCase

from pycggcrg.pycggcrg import RGGraph, run_rg, run_cggcrg, run_cggcirg


class TestCGGCRGWrapper(TestCase):

    def test_empty_graph(self):
        with self.assertRaises(ValueError) as e:
            RGGraph(0, [])

        self.assertIn('Only graphs with more than two nodes are possible', e.exception.message)

    def test_disconnected(self):
        data = [
            (2, []),
            (3, [(0, 2)]),
            (4, [(0, 1), (1, 2)]),
            (5, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]),
        ]
        for params in data:
            with self.assertRaises(ValueError) as e:
                RGGraph(*params)

            self.assertIn('Graph must be connected', e.exception.message)

    # def test_loops(self):
    #     data = [
    #         ((2, [(0, 0), (0, 1), (1, 1)]), 0)
    #     ]
    #
    #     for params in data:
    #         self.assertEqual(run_rg(RGGraph(*params[0])), params[1])

    def test_complete(self):
        N = 10
        for n in range(2, N+1):
            g = RGGraph(n, [(u, v) for u in range(n) for v in range(u+1, n)])

            self.assertEqual(g.m, n*(n-1)/2)

            self.assertAlmostEqual(run_rg(g, sample_size=1), 0)
            self.assertAlmostEqual(run_cggcrg(g), 0)
            self.assertAlmostEqual(run_cggcirg(g), 0)

    def test_butterfly(self):
        g = RGGraph(5, [(0, 1), (0, 2), (1, 2), (2, 3), (2, 4), (3, 4)])

        self.assertAlmostEqual(run_rg(g, sample_size=1), 1/9)
        self.assertAlmostEqual(run_cggcrg(g), 1/9)
        self.assertAlmostEqual(run_cggcirg(g), 1/9)

    def test_karate(self):
        g = RGGraph(34, [(0, 31), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 10), (0, 11),
                         (0, 12), (0, 13), (0, 17), (0, 19), (0, 21), (1, 2), (1, 3), (1, 7), (1, 13), (1, 17), (1, 19),
                         (1, 21), (1, 30), (2, 3), (2, 32), (2, 7), (2, 8), (2, 9), (2, 13), (2, 27), (2, 28), (3, 7),
                         (3, 12), (3, 13), (4, 10), (4, 6), (5, 6), (5, 10), (5, 16), (6, 16), (8, 30), (8, 33),
                         (8, 32), (9, 33), (13, 33), (14, 32), (14, 33), (15, 32), (15, 33), (18, 32), (18, 33),
                         (19, 33), (20, 32), (20, 33), (22, 32), (22, 33), (23, 32), (23, 25), (23, 27), (23, 33),
                         (23, 29), (24, 31), (24, 25), (24, 27), (25, 31), (26, 33), (26, 29), (27, 33), (28, 31),
                         (28, 33), (29, 32), (29, 33), (30, 33), (30, 32), (31, 32), (31, 33), (32, 33)])

        self.assertAlmostEqual(run_rg(g, sample_size=1), 0.419789612)
        self.assertAlmostEqual(run_cggcrg(g), 0.419789612)
        self.assertAlmostEqual(run_cggcirg(g), 0.419789612)
