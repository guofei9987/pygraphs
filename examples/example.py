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

# 1.return: '(src)' 返回节点列表，'[edge]' 返回 边的列表
G.match('(src)').where("src.born in ['1956', '1973'] and src.type == 'person'").returns('(src)')
G.match('[edge]').where("edge.type == 'acted_in' and edge.roles is not Null").returns('[edge]')

# 2. return: 'sub graph' 返回子图对象（Graph 对象）
G.match('(src)-[edge]->(dst)').where("src.type == 'person' and edge.type == 'acted_in' and dst.released > '2000'"). \
    returns('sub graph')

# 3. return: 指定属性，返回结构化数据（如果节点的某个属性不存在，对应单元格值为 Null）
G.match('(src)').where("src.born in ['1956', '1973'] and src.type == 'person'").returns('src.primary_key,src.born')
G.match('[edge]').where("edge.type == 'directed'").returns('edge.type,edge.roles')
G.match('(src)-[edge]->(dst)').where("src.type == 'person' and edge.type == 'acted_in' and dst.released > '2000'"). \
    returns('src.primary_key,src.born,edge.roles,dst.type,dst.released')

# 返回所有节点
G.vertexes
# 返回所有边
G.edges

# %%改
# 改节点属性，mode='update'覆盖已有属性并新增没有的属性，mode='cover'抹除全部旧属性并新增
G.match('(src)').where("src.born in ['1956', '1973'] and src.type == 'person'"). \
    set({'status': 'old man'}, mode='update')
# 查看是否已经改好：
G.match('(src)').where("src.born in ['1956', '1973'] and src.type == 'person'").returns('src.born,src.type,src.status')

# %%删
# 清除所有节点和边
# G.clear()

# 删边，del_edges 批量删，del_edge 单个删
edges_to_del = G.match('[edge]').where("edge.relation=='son'").returns('[edge]')
G.del_edges(edges_to_del=edges_to_del)

# 删节点，del_vertexes 批量删，del_vertex 单个删
vertexes_to_del = G.match('(src)').where("src.primary_key=='Tom'").returns('(src)')
G.del_vertexes(vertexes_to_del=vertexes_to_del)

# %% 持久化
# 从内存把图数据库存到文件
pg.save_db(G, 'db_file.db')
# 从文件读图数据库到内存
G_new = pg.load_db('db_file.db')


#%%


#%%
a="edge.type == 'acted_in' and edge.roles is not Null"

