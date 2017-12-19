"""

.. moduleauthor:: Fabian Ball <fabian.ball@kit.edu>
"""
from math import log, ceil

from cggc_rg import RGGraph, RGAlgorithms


def make_graph(n, edge_list, check_connectedness=True):
    """

    :param n:
    :param edge_list:
    :param check_connectedness:
    :return:
    """
    try:
        return RGGraph(n, edge_list, check_connectedness)
    except IndexError as e:
        if '_M_range_check' in e.message:
            raise ValueError('Invalid node id detected: {}'.format(e))

    return None


def run_rg(g, sample_size=2, runs=1, return_partition=False):
    """
    Execute the single randomized greedy algorithm.

    :param g: A graph (use :func:`pyrg.make_graph` the create one)
    :type g: :class:`pyrg.RGGraph`
    :param sample_size: How many clusters shall be picked for search in one iteration?
    :type sample_size: int
    :param runs: Number of independent runs to obtain the best result
    :type runs: int
    :param return_partition: (Optional) If True, returns the resulting partition
    :type return_partition: bool
    :return: The modularity
    :rtype: float
    """
    algo = RGAlgorithms(g)

    modularity = algo.run_rg(sample_size, runs)

    if return_partition:
        partition = algo.get_partition()

        return modularity, partition
    else:
        return modularity


def run_cggcrg(g, ensemble_size=None, sample_size_restart=2, return_partition=False):
    """

    :param g: A graph (use :func:`pyrg.make_graph` the create one)
    :type g: :class:`pyrg.RGGraph`
    :param ensemble_size: (Optional) Number of initial partitions
    :type ensemble_size: int | None
    :param sample_size_restart: How many clusters shall be picked for search in one iteration?
    :type sample_size_restart: int
    :param return_partition: (Optional) If True, returns the resulting partition
    :type return_partition: bool
    :return:
    """
    algo = RGAlgorithms(g)

    if not ensemble_size:
        ensemble_size = int(ceil(log(g.n)))

    modularity = algo.run_cggc_rg(ensemble_size, sample_size_restart)

    if return_partition:
        partition = algo.get_partition()

        return modularity, partition
    else:
        return modularity


def run_cggcirg(g, ensemble_size=None, sample_size_restart=2, return_partition=False):
    """

    :param g: A graph (use :func:`pyrg.make_graph` the create one)
    :type g: :class:`pyrg.RGGraph`
    :param ensemble_size: (Optional) Number of initial partitions
    :type ensemble_size: int | None
    :param sample_size_restart: How many clusters shall be picked for search in one iteration?
    :type sample_size_restart: int
    :param return_partition: (Optional) If True, returns the resulting partition
    :type return_partition: bool
    :return:
    """
    algo = RGAlgorithms(g)

    if not ensemble_size:
        ensemble_size = int(ceil(log(g.n)))

    modularity = algo.run_cggci_rg(ensemble_size, sample_size_restart)

    if return_partition:
        partition = algo.get_partition()

        return modularity, partition
    else:
        return modularity
