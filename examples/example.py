import pygraphs as pg

G = pg.Graph()

# 从csv读取节点并加入图数据库
G.add_vertexes_from_file(filename='Vertexes.csv')

# 从list读取节点并加入图数据库
vertexes_list = [['Tom', {'age': 10}],
                 ['Kitty', {'sex': 'female'}],
                 ['Jimmy', {'sex': 'male', 'age': 35}]
                 ]
G.add_vertexes_from_list(vertexes_list=vertexes_list)

print(G.vertexes)
# %%
# 从csv读取关系并加入图数据库
G.add_edges_from_file(filename='Edges.csv')

# 从 list 读取并加入图数据库
edges_list = [['Tom', {'relation': 'son'}, 'Jimmy'],
              ['Kitty', {'relation': 'wife'}, 'Jimmy'],
              ]
G.add_edges_from_list(edges_list=edges_list)
print(G.edges)

# %% 查
# 按照主键来查询
print(G.vertexes['Frank Darabont'])

# 按特定过滤条件查询节点
young_people = G.query(condition_vertex=lambda x: ('born' in x) and x['born'] > '1975')
print(young_people)

# 按特定过滤条件查询边
relation_son = G.query(condition_edge=lambda x: 'relation' in x and x['relation'] == 'son')
print(relation_son)

# 返回所有节点
G.vertexes
# 返回所有边
G.edges
# %%
# 复杂查询
for edge in G.edges:
    if 'type' in edge.val and edge.val['type'] == 'acted_in':
        src = edge.src
        if 'born' in src.val and src.val['born'] > '1975':
            print(src, ';', edge)

# %%改
# 改节点属性，已有的属性被覆盖，如果没有属性则新建
G.set_val(G.vertexes['Kitty'], {'sex': 'male', 'height': '1.8m'})
print(G.vertexes['Kitty'].val)

# 改边的属性，已有的属性被覆盖，如果没有属性则新建
edge_to_set = list(relation_son)[0]
G.set_val(edge_to_set, {'relation': 'husband'})
print(edge_to_set.val)

# %%删
# 清除所有节点和边
# G.clear()

# 删边，del_edges 批量删，del_edge 单个删
G.del_edges(edges_to_del=relation_son)

# 删节点，del_vertexes 批量删，del_vertex 单个删
G.del_vertex(vertex_to_del=G.vertexes['Tom'])

# %% 持久化
# 从内存把图数据库存到文件
pg.save_db(G, 'db_file.db')
# 从文件读图数据库到内存
G_new = pg.load_db('db_file.db')
