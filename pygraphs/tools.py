import pickle
import sys


def save_db(db, filename='pg.db'):
    sys.setrecursionlimit(10000)
    with open(filename, 'wb') as f:
        pickle.dump(db, f, True)


def load_db(filename='pg.db'):
    with open(filename, 'rb') as f:
        db = pickle.load(f)
    return db


class TrueNone(object):
    '''
    用于支持 query 语句，
    此对象无论遇到何种运算均返回 False
    所以在调用"不存在的对象"，采用此对象
    '''

    def __add__(self, other): return False

    def __sub__(self, other): return False

    def __mul__(self, other): return False

    def __truediv__(self, other): return False

    def __floordiv__(self, other): return False

    def __mod__(self, other): return False

    def __divmode__(self, other): return False

    def __pow__(self, other): return False

    def __lshift__(self, other): return False

    def __rshift__(self, other): return False

    def __and__(self, other): return False

    def __or__(self, other): return False

    def __xor__(self, other): return False

    def __eq__(self, other): return True if other is None else False

    def __repr__(self):
        return 'Null'


class PgDict(dict):
    '''
    用于支持 query 语句类似 node.type 的语句，
    并且遇到不存在的属性，返回一个无论如何运算都 False 的对象，而不是直接报错
    '''

    def __getattr__(self, s):
        return self.get(s, TrueNone())


def cql_parser(cql=''):
    # 预处理 cql 文本
    cql = cql.replace('is Null', "=='None'")
    cql = cql.replace('is not Null', "!='None'")

    # TODO: 单等号替换为双等号
    return cql


def to_echarts(graph, category):
    # 把 Graph 对象转换成 echarts 直接可用的数据结构
    nodes_for_echarts = [{'name': pk, 'symbolSize': 15, 'category': vertex.val[category]}
                         for pk, vertex in graph.vertexes.items()]
    edge_for_echarts = [{"source": edge.src.val['primary_key'], "target": edge.dst.val['primary_key']}
                        for edge in graph.edges]
    graph_category = [{"name": i, "symbol": j}
                      for i, j in zip(*({node['category'] for node in nodes_for_echarts},
                                        ['circle', 'diamond', 'triangle', 'rect', 'roundRect', 'pin'] * 20))
                      ]
    return nodes_for_echarts, edge_for_echarts, graph_category


if __name__ == '__name__':
    tn = TrueNone()
    assert tn % 1 is False
    assert tn + 1 is False
    assert tn // 2 is False
    assert tn == None
    # 现在还不能支持 tn is None 这种语句
