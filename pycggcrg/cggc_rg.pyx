"""

.. moduleauthor:: Fabian Ball <fabian.ball@kit.edu>
"""
import warnings

from libcpp.list cimport list as cpp_list
from libcpp.pair cimport pair
from libcpp.vector cimport vector
from libc.stdlib cimport srand

from pycggcrg cimport cggc_rg


cdef class RGGraph(object):
    """
    Python class to wrap the C++ RG graph implementation
    """
    cdef cggc_rg.Graph *_thisptr

    def __cinit__(self, int n, edges, check_connectedness=True):
        """
        Initialize a simple graph of *n* nodes using a list of *edges*.
        Each edge is a 2-tuple of node ids.

        :param n:
        :param edges:
        """
        cdef cpp_list[pair[int, int]] edge_list = edges

        if n < 2:
            raise ValueError('Only graphs with more than two nodes are possible')

        if len(edge_list) < n-1 or check_connectedness and not self._check_connectedness(n, edges):
            raise ValueError('Graph must be connected')

        self._thisptr = new cggc_rg.Graph(n, &edge_list)


    def _check_connectedness(self, n, edge_list):
        reachability = [{i} for i in range(n)]
        for edge in edge_list:
            a, b = edge
            if len(reachability[a]) < len(reachability[b]):
                a, b = b, a

            reachability[a].update(reachability[b])
            for idx in reachability[b]:
                reachability[idx] = reachability[a]

        return len(reachability[0]) == n

    def __dealloc__(self):
        if self._thisptr is not NULL:
            del self._thisptr

    cdef cggc_rg.Graph* get_graph(self):
        return self._thisptr

    @property
    def n(self):
        return self._thisptr.get_vertex_count()

    @property
    def m(self):
        return self._thisptr.get_edge_count()


cdef class RGAlgorithms:
    """
    Python class to wrap the C++ RG algorithms implementation
    """
    cdef cggc_rg.ModOptimizer *_thisptr
    cdef cggc_rg.Graph *_graph
    cdef _run

    def __cinit__(self, RGGraph graph, int seed):
        cdef cggc_rg.Graph *g = graph.get_graph()

        self._graph = g
        self._thisptr = new cggc_rg.ModOptimizer(g)

        self._run = False

        srand(seed)  # Important! Set the seed for the standard pseudo random generator

    def __dealloc__(self):
        if self._thisptr is not NULL:
            del self._thisptr

    def run_rg(self, int sample_size, int runs):
        """
        Execute the RG algorithm with *sample_size* random cluster picks per iteration.
        A total number of *runs* is executed, the result is the best out of it.

        :param sample_size: Number of random picks per iteration
        :type sample_size: int
        :param runs: Number of algorithm runs
        :type runs: int
        """
        if sample_size < 1:
            raise ValueError("sample_size must be greater zero")

        if runs < 1:
            raise ValueError("runs must be greater zero")

        self._thisptr.ClusterRG(sample_size, runs)
        self._run = True

    def run_cggc_rg(self, int ensemble_size, int sample_size_restart):
        """
        Execute the CGGC-RG algorithm with *ensemble_size* generated partitions to combine
        and *sample_size_restart* random cluster picks per iteration for the final run.

        :param ensemble_size: Number of ensemble partitions to generate
        :type ensemble_size: int
        :param sample_size_restart: Number of random picks per iteration
        :type sample_size_restart: int
        """
        if ensemble_size < 1:
            raise ValueError("ensemble_size must be greater zero")

        if sample_size_restart < 1:
            raise ValueError("sample_size_restart must be greater zero")

        self._thisptr.ClusterCGGC(ensemble_size, sample_size_restart, 0)
        self._run = True

    def run_cggci_rg(self, int ensemble_size, int sample_size_restart):
        """
        Execute the CGGCi-RG algorithm with *ensemble_size* generated partitions to combine
        and *sample_size_restart* random cluster picks per iteration for the final run.

        :param ensemble_size: Number of ensemble partitions to generate
        :type ensemble_size: int
        :param sample_size_restart: Number of random picks per iteration
        :type sample_size_restart: int
        """
        if ensemble_size < 1:
            raise ValueError("ensemble_size must be greater zero")

        if sample_size_restart < 1:
            raise ValueError("sample_size_restart must be greater zero")

        self._thisptr.ClusterCGGC(ensemble_size, sample_size_restart, 1)
        self._run = True

    def get_modularity(self):
        """
        Get the maximal modularity value found.

        :return: Modularity
        :rtype: float | None
        """
        if not self._run:
            warnings.warn("No algorithm was executed.")
            return None

        if not self._thisptr.GetClusters():
            raise TypeError("Something went wrong! No partition available")

        return self._thisptr.GetModularityFromClustering(self._graph, self._thisptr.GetClusters())

    def get_partition(self):
        """
        Get the modularity maximal partition.

        :return: Partition as list of lists of node ids
        :rtype: list | None
        """
        if not self._run:
            warnings.warn("No algorithm was executed.")
            return None

        if not self._thisptr.GetClusters():
            raise TypeError("Something went wrong! No partition available")

        cdef cggc_rg.t_partition *partition
        cdef cggc_rg.t_id_list *cluster
        partition = self._thisptr.GetClusters().get_partition_vector()

        py_partition = []
        for i in range(partition.size()):
            cluster = partition.at(i)
            py_partition.append(cluster[0])

        return py_partition
