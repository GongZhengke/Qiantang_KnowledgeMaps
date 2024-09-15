from py2neo import Graph, Node, Relationship
import csv

# 连接neo4j数据库，输入地址、用户名、密码
graph = Graph('http://localhost:7474/', auth=("neo4j", "gongzhengke"))
# 清空原有neo4j数据库
graph.delete_all()

# 打开name.csv文件
with open('../data/name.csv', 'r', encoding='utf-8') as name:
    # 打开csv文件
    reader_name = csv.reader(name)
    # 把读取到的数据放在list列表中，并赋给data
    data_name = list(reader_name)
print(data_name[1])

# 打开zly.csv文件
with open('../data/zly.csv', 'r', encoding='utf-8') as zly_index:
    # 打开csv文件
    reader_zly = csv.reader(zly_index)
    # 把读取到的数据放在list列表中，并赋给data
    data_zly = list(reader_zly)
print(data_zly[1])
# 这两个list用来存放后面要新建的Node的实例

# node用来存放Node实例，当找到隶属流域在已有的流域中时，获取所在的下标，读取该位置的Node实例
node = list()
# 用来存放省
nodeLake_province = list()
# 用来存放市
nodeLake_city = list()
# 用来存放区县
nodeLake_county = list()
# 用来存放水库
nodeLake_reservoir = list()

# num用来存放流域编号，用于查找隶属流域是否在已有的流域中
ly_number = list()
# 用来存放流域名称
ly_name = list()
# 用来存放省
numLake_province = list()
# 用来存放市
numLake_city = list()
# 用来存放区县
numLake_county = list()
# 用来存放水库所属水系
numLake_reservoir = list()

for i in range(0, len(data_zly) - 1):
    # 建立 流域 结点
    node.append(Node('ly', name=data_zly[i + 1][2], id=data_zly[i + 1][0], number=data_zly[i + 1][1], length=data_zly[i + 1][5], area=data_zly[i + 1][6]))
    graph.create(node[i])
    # 存放流域编号
    ly_number.append(dict(node[i])['number'])
    # 存放流域名
    ly_name.append(dict(node[i])['name'])

for i in range(0, len(data_name) - 1):
    # 建立 水库 结点
    nodeLake_reservoir.append(Node('zm', id=data_name[i + 1][0], name=data_name[i + 1][6], jd=data_name[i + 1][10], wd=data_name[i + 1][11], zcsw=data_name[i + 1][20]))
    graph.create(nodeLake_reservoir[i])
    # 存放水库所属流域
    numLake_reservoir.append(data_name[i + 1][14])
    if data_name[i + 1][2] in numLake_province:
        print()
    else:
        nodeLake_province.append(Node('pro', name=data_name[i + 1][2]))
        numLake_province.append(data_name[i + 1][2])
    if data_name[i + 1][3] in numLake_city:
        print()
    else:
        nodeLake_city.append(Node('sss', name=data_name[i + 1][3]))
        numLake_city.append(data_name[i + 1][3])
    if data_name[i + 1][4] in numLake_county:
        print()
    else:
        nodeLake_county.append(Node('ssx', name=data_name[i + 1][4]))
        numLake_county.append(data_name[i + 1][4])

# 因为数据有很多，需要逐行遍历，
for i in range(0, len(data_zly) - 1):
    # dict是将Node的实例转成json字符，并且判断隶属流域是否存在
    if data_zly[i + 1][7] != '':
        # 如果存在的情况下，查看隶属流域是否存在已有的流域中
        # 如果存在，则会进入这里，对num中找到下标
        if data_zly[i + 1][7] in ly_number:
            # 寻找下标
            zly_index = ly_number.index(data_zly[i + 1][7])
            # 创建 流域——流域 关系
            lyToLy = Relationship(node[i], 'inflows', node[zly_index], rel='inflows')
            graph.create(lyToLy)

for i in range(0, len(data_name) - 1):
    if numLake_reservoir[i] != '':
        if numLake_reservoir[i] not in ly_name:
            node.append(Node('lyn', name=str(data_name[i + 1][14])))
            graph.create(node[len(node)-1])
            ly_name.append(data_name[i + 1][14])
        lyIndex = ly_name.index(data_name[i + 1][14])
        proIndex = numLake_province.index(data_name[i + 1][2])
        sssIndex = numLake_city.index(data_name[i + 1][3])
        ssxIndex = numLake_county.index(data_name[i + 1][4])
        graph.create(nodeLake_province[proIndex])
        graph.create(nodeLake_city[sssIndex])
        graph.create(nodeLake_county[ssxIndex])
        # 创建 省——市 关系
        proToCity = Relationship(nodeLake_city[sssIndex], 'belongs to', nodeLake_province[proIndex], rel='belongs to')
        graph.create(proToCity)
        # 创建 市——区 关系
        cityToCounty = Relationship(nodeLake_county[ssxIndex], 'belongs to', nodeLake_city[sssIndex], rel='belongs to')
        # 创建 区——水库 关系
        countyToRes = Relationship(nodeLake_reservoir[i], 'located in', nodeLake_county[ssxIndex], rel='located in')
        graph.create(cityToCounty)
        graph.create(countyToRes)
        # 创建 省——流域 关系
        proToLy = Relationship(node[lyIndex], 'flows through', nodeLake_province[proIndex], rel='flows through')
        graph.create(proToLy)

    # 创建 流域——水库 关系
    if numLake_reservoir[i] != '':
        lyIndex = ly_name.index(data_name[i + 1][14])
        lyToRes = Relationship(node[lyIndex], 'inflows', nodeLake_reservoir[i], rel='inflows')
        graph.create(lyToRes)

print("运行完成")