"""

.. moduleauthor:: Fabian Ball <fabian.ball@kit.edu>
"""
from math import log, ceil
from random import randint

from cggc_rg import RGGraph, RGAlgorithms


def make_graph(n, edge_list, check_connectedness=True):
    """
    Create a graph of *n* nodes given a list of edges.

    *check_connectedness* should be True unless you are sure that the graph
    is really connected.

    :param n: Number of nodes
    :type n: int
    :param edge_list: An iterable of edges, each edge is a 2-tuple of node ids
    :type edge_list: iterable
    :param check_connectedness: (Optional) Perform a check if the edge_list describes a connected graph
    :type check_connectedness: bool
    :return: A graph, suitable to execute (CGGC)RG on
    :rtype: :class:`cggc_rg.RGGraph`
    """
    try:
        return RGGraph(n, list(edge_list), check_connectedness)
    except IndexError as e:
        if '_M_range_check' in e.message:
            raise ValueError('Invalid node id detected: {}'.format(e))

    return None


def _get_seed():
    return randint(0, 2**16 - 1)


def run_rg(g, sample_size=2, runs=1, return_partition=False, seed=None):
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
    :param seed: (Optional) A seed to instantiate the pseudo RNG
    :type seed: int
    :return: The modularity and the partition if *return_partition* is True
    :rtype: float | float, list
    """
    seed = seed if seed is not None else _get_seed()
    algo = RGAlgorithms(g, seed)

    algo.run_rg(sample_size, runs)
    modularity = algo.get_modularity()

    if return_partition:
        partition = algo.get_partition()

        return modularity, partition
    else:
        return modularity


def run_cggcrg(g, ensemble_size=None, sample_size_restart=2, return_partition=False, seed=None):
    """
    Run the plain CGGC-RG algorithm.

    :param g: A graph (use :func:`pyrg.make_graph` the create one)
    :type g: :class:`pyrg.RGGraph`
    :param ensemble_size: (Optional) Number of initial partitions
    :type ensemble_size: int | None
    :param sample_size_restart: How many clusters shall be picked for search in one iteration?
    :type sample_size_restart: int
    :param return_partition: (Optional) If True, returns the resulting partition
    :type return_partition: bool
    :param seed: (Optional) A seed to instantiate the pseudo RNG
    :type seed: int
    :return: The modularity and the partition if *return_partition* is True
    :rtype: float | float, list
    """
    seed = seed if seed is not None else _get_seed()
    algo = RGAlgorithms(g, seed)

    if not ensemble_size:
        ensemble_size = int(ceil(log(g.n)))

    algo.run_cggc_rg(ensemble_size, sample_size_restart)
    modularity = algo.get_modularity()

    if return_partition:
        partition = algo.get_partition()

        return modularity, partition
    else:
        return modularity


def run_cggcirg(g, ensemble_size=None, sample_size_restart=2, return_partition=False, seed=None):
    """
    Run the iterated CGGC-RG algorithm.

    :param g: A graph (use :func:`pyrg.make_graph` the create one)
    :type g: :class:`pyrg.RGGraph`
    :param ensemble_size: (Optional) Number of initial partitions
    :type ensemble_size: int | None
    :param sample_size_restart: How many clusters shall be picked for search in one iteration?
    :type sample_size_restart: int
    :param return_partition: (Optional) If True, returns the resulting partition
    :type return_partition: bool
    :param seed: (Optional) A seed to instantiate the pseudo RNG
    :type seed: int
    :return: The modularity and the partition if *return_partition* is True
    :rtype: float | float, list
    """
    seed = seed if seed is not None else _get_seed()
    algo = RGAlgorithms(g, seed)

    if not ensemble_size:
        ensemble_size = int(ceil(log(g.n)))

    algo.run_cggci_rg(ensemble_size, sample_size_restart)
    modularity = algo.get_modularity()

    if return_partition:
        partition = algo.get_partition()

        return modularity, partition
    else:
        return modularity
