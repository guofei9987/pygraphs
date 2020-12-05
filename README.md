# pygraphs
A graph database based on Python

纯Python实现的图数据库

- [x] 完备增删改查
- [ ] 改善复杂查询的体验
- [ ] 支持 CQL 语句


## 使用文档

初始化一个空的图数据库
```python
import pygraphs as pg

G = pg.Graph()
```

### 增

增加节点
```python
# 从csv读取节点并加入图数据库
G.add_vertexes_from_file(filename='Vertexes.csv')

# 从list读取节点并加入图数据库
vertexes_list = [['Tom', {'age': 10}],
                 ['Kitty', {'sex': 'female'}],
                 ['Jimmy', {'sex': 'male', 'age': 35}]
                 ]
G.add_vertexes_from_list(vertexes_list=vertexes_list)

print(G.vertexes)
```

增加边
```python
# 从csv读取关系并加入图数据库
G.add_edges_from_file(filename='Edges.csv')

# 从 list 读取并加入图数据库
edges_list = [['Tom', {'relation': 'son'}, 'Jimmy'],
              ['Kitty', {'relation': 'wife'}, 'Jimmy'],
              ]
G.add_edges_from_list(edges_list=edges_list)
print(G.edges)
```

### 查
```python
# 按照主键来查询
print(G.vertexes['Frank Darabont'])

# 按特定过滤条件查询节点
young_people = G.query(condition_vertex=lambda x: ('born' in x) and x['born'] > '1975')
print(young_people)

# 按特定过滤条件查询边
relation_son = G.query(condition_edge=lambda x: 'relation' in x and x['relation'] == 'son')
print(relation_son)


```

复杂查询
```python
for edge in G.edges:
    if 'type' in edge.val and edge.val['type'] == 'acted_in':
        src = edge.src
        if 'born' in src.val and src.val['born'] > '1975':
            print(src, ';', edge)
```

### 删
清除所有节点和边
```python
G.clear()
```

```python
# 删边，G.del_edges 批量删，G.del_edge 单个删
G.del_edges(edges_to_del=relation_son)

# 删节点，G.del_vertexes 批量删，G.del_vertex 单个删
G.del_vertex(vertex_to_del=G.vertexes['Tom'])
```

### 改
改节点属性，已有的属性被覆盖，没有的属性新建

```python
G.set_val(G.vertexes['Kitty'], {'sex': 'male', 'height': '1.8m'})
print(G.vertexes['Kitty'].val)
```

改边的属性，已有的属性被覆盖，没有的属性新建

```python
edge_to_set = list(G.vertexes['Kitty'].dst)[0]
self = G.set_val(edge_to_set, {'relation': 'husband'})
print(edge_to_set.val)
```


### 持久化
把图数据库存到本地
```python
pg.save_db(G, 'db_file.db')
```

从本地读图数据库

```python
G_new = pg.load_db('db_file.db')
```
