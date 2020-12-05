import ast
import csv



class Vertex(object):
    def __init__(self, primary_key, val=None):
        self.primary_key = primary_key
        self.val = val or dict()
        self.src = set()
        self.dst = set()

    def __repr__(self):
        return 'Vertex: primary_key = {}'.format(self.primary_key)


class Edge(object):
    def __init__(self, val=None, src=None, dst=None):
        self.val = val
        self.src = src
        self.dst = dst

    def __repr__(self):
        return 'Edge: {}->{}'.format(self.src.primary_key, self.dst.primary_key)


class Graph(object):
    def __init__(self):
        self.vertexes = dict()
        self.edges = set()

    def add_vertexes_from_list(self, vertexes_list):
        self.vertexes.update({pk: Vertex(primary_key=pk, val=val) for pk, val in vertexes_list})

    def add_vertexes_from_file(self, filename):
        with open(filename) as f:
            f_csv = csv.reader(f)
            self.vertexes.update({pk: Vertex(primary_key=pk, val=ast.literal_eval(val)) for pk, val in f_csv})

    def add_edges_from_list(self, edges_list):
        for src_pk, val, dst_pk in edges_list:
            src, dst = self.vertexes[src_pk], self.vertexes[dst_pk]
            edge = Edge(val=val, src=src, dst=dst)
            src.dst.add(edge)
            dst.src.add(edge)

            self.edges.add(edge)

    def add_edges_from_file(self, filename):
        with open(filename) as f:
            f_csv = csv.reader(f)
            edges_list = [[src_pk, ast.literal_eval(val), dst_pk] for src_pk, val, dst_pk in f_csv]
            self.add_edges_from_list(edges_list)

    def del_edge(self, edge_to_del):
        edge_to_del.src.dst.remove(edge_to_del)
        edge_to_del.dst.src.remove(edge_to_del)
        self.edges.remove(edge_to_del)

    def del_edges(self, edges_to_del):
        for edge_to_del in edges_to_del:
            self.del_edge(edge_to_del)

    def del_vertex(self, vertex_to_del):
        assert not (vertex_to_del.dst or vertex_to_del.src), 'To delete node, you must first delete its relationships.'
        self.vertexes.pop(vertex_to_del.primary_key)

    def del_vertexes(self, vertexes_to_del):
        for vertex_to_del in vertexes_to_del:
            self.del_vertex(vertex_to_del)

    def clear(self):
        self.__init__()

    def set_val(self, vertex_or_edge, val):
        vertex_or_edge.val.update(val)

    def query(self, condition_vertex=None, condition_edge=None):
        '''
        TODO: 增加功能-联动查询
        TODO: 增加功能-CQL语句
        :param condition:
        :return:
        '''
        if condition_vertex is not None and condition_edge is not None:
            raise LookupError('还未实现联动查询')
        res = set()
        if condition_vertex:
            for pk, vertex in self.vertexes.items():
                if condition_vertex(vertex.val):
                    res.add(vertex)
            return res

        if condition_edge:
            res = set()
            for edge in self.edges:
                if condition_edge(edge.val):
                    res.add(edge)
            return res

