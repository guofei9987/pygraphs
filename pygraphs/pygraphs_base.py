# -*- coding: utf-8 -*-
# @Time    : 2020/12/05
# @Author  : github.com/guofei9987
import ast
import csv
from pygraphs.tools import PgDict, cql_parser


class Vertex(object):
    def __init__(self, val=None):
        self.val = dict(val) or dict()
        self.src = set()
        self.dst = set()

    def __repr__(self):
        return 'Vertex: primary_key = {}'.format(self.val['primary_key'])


class Edge(object):
    def __init__(self, val=None, src=None, dst=None):
        self.val = dict(val) or dict()
        self.src = src
        self.dst = dst

    def __repr__(self):
        return 'Edge: {} -> {}'.format(self.src.val['primary_key'], self.dst.val['primary_key'])


class Graph(object):
    def __init__(self):
        self.vertexes = dict()
        self.edges = set()

    def add_vertexes_from_list(self, vertexes_list):
        for pk, val in vertexes_list:
            val['primary_key'] = pk
        self.vertexes.update({pk: Vertex(val=val) for pk, val in vertexes_list})

    def add_vertexes_from_file(self, filename):
        with open(filename) as f:
            f_csv = csv.reader(f)
            self.add_vertexes_from_list([[pk, ast.literal_eval(val)] for pk, val in f_csv])

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
        assert not (vertex_to_del.dst or vertex_to_del.src), 'To delete node, you must first delete its edges.'
        self.vertexes.pop(vertex_to_del.val['primary_key'])

    def del_vertexes(self, vertexes_to_del):
        for vertex_to_del in vertexes_to_del:
            self.del_vertex(vertex_to_del)

    def clear(self):
        self.__init__()

    def set_val(self, vertex_or_edge, val):
        vertex_or_edge.val.update(val)

    def match(self, elements):
        # TODO: 输入的字符是任意的
        if elements == '(src)-[edge]->(dst)':
            match_type = 'combined'
            match_elements = 'src', 'edge', 'dst'
        elif elements == '(src)':
            match_type = 'vertex'
            match_elements = 'src'
        elif elements == '[edge]':
            match_type = 'edge'
            match_elements = 'edge'
        else:
            raise KeyError('match(elements) is not correct')

        return MatchObject(match_type, match_elements, self)


class MatchObject(object):
    def __init__(self, match_type, match_elements, graph):
        self.match_type, self.match_elements, self.graph = match_type, match_elements, graph
        self.where_res = None

    def where(self, str_filter):
        str_filter = cql_parser(str_filter)
        where_res = list()
        if self.match_type == 'vertex':
            conditions = eval('lambda {vertex}:'.format(vertex=self.match_elements) + str_filter)
            for pk, vertex in self.graph.vertexes.items():
                if conditions(PgDict(vertex.val)):
                    where_res.append(vertex)

        elif self.match_type == 'edge':
            conditions = eval('lambda {edge}:'.format(edge=self.match_elements) + str_filter)
            for edge in self.graph.edges:
                if conditions(PgDict(edge.val)):
                    where_res.append(edge)

        elif self.match_type == 'combined':
            conditions = eval('lambda {combined}:'.format(combined=','.join(self.match_elements)) + str_filter)
            for edge_ in self.graph.edges:
                if conditions(PgDict(edge_.src.val), PgDict(edge_.val), PgDict(edge_.dst.val)):
                    where_res.append([edge_.src, edge_, edge_.dst])
        self.where_res = where_res
        return self

    def returns(self, expr=''):
        assert self.where_res is not None, 'returns must follow where'
        if expr == '(src)':
            return self.where_res
        elif expr == '[edge]':
            return self.where_res
        elif expr == 'sub graph' or expr == 'sub-graph':
            assert self.match_type == 'combined', '目前只有完整查询可以返回子图对象'
            sub_G = Graph()
            sub_G.edges = {edge for _, edge, _ in self.where_res}
            vertexes = {edge.src for edge in sub_G.edges} | {edge.dst for edge in sub_G.edges}
            sub_G.vertexes = {vertex.val['primary_key']: vertex for vertex in vertexes}
            return sub_G
        else:
            # 返回结构化数据，内容是属性
            if self.match_type in ['vertex', 'edge']:
                raw_data1 = [PgDict(vertex.val) for vertex in self.where_res]
                raw_data2 = [eval('[[{expr}] for {match_elements} in raw_data1]'.
                                  format(expr=expr, match_elements=self.match_elements))]
                return raw_data2
            elif self.match_type == 'combined':
                raw_data1 = [[PgDict(src.val), PgDict(edge.val), PgDict(dst.val)] for src, edge, dst in self.where_res]
                raw_data2 = [eval('[' + expr + ']') for src, edge, dst in raw_data1]
                return raw_data2

    def set(self, val, mode='update'):
        assert self.where_res is not None, 'set must follow where'
        if self.match_type in ['vertex', 'edge']:
            if mode == 'update':
                [vertex_or_edge.val.update(val) for vertex_or_edge in self.where_res]
            if mode == 'cover':
                for vertex_or_edge in self.where_res:
                    vertex_or_edge.val = val

        elif self.match_type == 'combined':
            # TODO: 传入一个变量，指定改哪个元素（上游、边、下游）
            raise ValueError('set to combined match is not supported yet')

    # def delete(self):
    # 感觉在这里做 delete 不太合适
    #     pass
