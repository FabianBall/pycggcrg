"""

.. moduleauthor:: Fabian Ball <fabian.ball@kit.edu>
"""
from __future__ import absolute_import, division
from unittest import TestCase

from pycggcrg.pycggcrg import RGGraph


class TestRGGraph(TestCase):

    def test_empty_graph(self):
        with self.assertRaises(ValueError) as e:
            RGGraph(0, [])

        self.assertIn('Only graphs with more than two nodes are possible', e.exception.message)

        with self.assertRaises(ValueError) as e:
            RGGraph(2, [])

        self.assertIn('Graph must be connected', e.exception.message)

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
