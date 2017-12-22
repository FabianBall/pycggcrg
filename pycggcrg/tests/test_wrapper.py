"""

.. moduleauthor:: Fabian Ball <fabian.ball@kit.edu>
"""
from __future__ import absolute_import, division
from unittest import TestCase
import warnings

from pycggcrg.pycggcrg import RGGraph, RGAlgorithms


class TestRGAlgorithms(TestCase):

    def setUp(self):
        self.butterfly = RGGraph(5, [(0, 1), (0, 2), (1, 2), (2, 3), (2, 4), (3, 4)])

    def test_not_executed(self):
        g = self.butterfly

        alg = RGAlgorithms(g, 0)

        # No algorithm executed yet
        warnings.filterwarnings('ignore')  # Ignore warnings
        self.assertIs(alg.get_modularity(), None)
        self.assertIs(alg.get_partition(), None)

        warnings.filterwarnings('error')  # Raise warnings
        self.assertRaises(Warning, alg.get_modularity)
        self.assertRaises(Warning, alg.get_partition)

    def test_wrong_param(self):
        g = self.butterfly

        alg = RGAlgorithms(g, 0)

        # Wrong parameters
        self.assertRaises(ValueError, alg.run_rg, *(0, 1))
        self.assertRaises(ValueError, alg.run_rg, *(1, -1))
        self.assertRaises(ValueError, alg.run_cggc_rg, *(0, 1))
        self.assertRaises(ValueError, alg.run_cggc_rg, *(1, -1))
        self.assertRaises(ValueError, alg.run_cggci_rg, *(0, 1))
        self.assertRaises(ValueError, alg.run_cggci_rg, *(1, -1))

    def test_multiple_runs(self):
        g = self.butterfly

        alg = RGAlgorithms(g, 0)

        # Multiple algorithm runs should be possible
        alg.run_rg(1, 1)
        self.assertGreaterEqual(alg.get_modularity(), 0)
        alg.run_rg(1, 1)
        self.assertGreaterEqual(alg.get_modularity(), 0)
        alg.run_cggc_rg(1, 1)
        self.assertGreaterEqual(alg.get_modularity(), 0)
        alg.run_cggci_rg(1, 1)
        self.assertGreaterEqual(alg.get_modularity(), 0)
