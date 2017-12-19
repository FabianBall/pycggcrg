# distutils: language=c++
from libcpp.list cimport list
from libcpp.pair cimport pair
from libcpp.vector cimport vector


cdef extern from 'graph.h':
    cdef cppclass Graph:
        Graph(int vertexcount, list[pair[int, int]]* elist) except +

        int get_vertex_count()
        int get_edge_count()


cdef extern from 'partition.h':
    ctypedef list[int] t_id_list
    ctypedef vector[t_id_list*] t_partition

    cdef cppclass Partition:
        Partition(int size) except +

        t_partition* get_partition_vector() except +
        # vector[list[int]]* get_partition_vector() except +


cdef extern from 'modoptimizer.h':
    cdef cppclass ModOptimizer:
        ModOptimizer(Graph* graph) except +

        Partition* get_clusters() except +

        double ClusterRG(int sample_size, int runs) except +
        double ClusterCGGC(int ensemble_size, int sample_size_restart, bint iterative) except +
        # double GetModularityFromClustering(Graph* graph, Partition* clusters) except +
