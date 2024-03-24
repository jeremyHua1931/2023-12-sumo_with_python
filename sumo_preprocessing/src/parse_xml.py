# -*- encoding: utf-8 -*-
"""
@File    :   parse_xml.py
@Contact :   jeremyhua@foxmail.com

@Modify Time      @Author       @Version     @Description
------------      -------       --------     -----------
2023/3/5 14:03   HuaZhangzhao    1.0          parse net.xml into .jsons
"""
import json
import xml.etree.ElementTree as ET


def parse_edges(root) -> list:
    """
    This function is used to extract edge tags
    Args:
        root: the origin net.xml

    Returns: results is preserved in /res

    """
    edges = []
    for edge in root.iter('edge'):
        edge_id = edge.get('id')
        if edge.get('function') == "internal":
            e_function = edge.get('function')
            edge_dict = {'id': edge_id, 'function': e_function}
        else:
            e_from = edge.get('from')
            e_to = edge.get('to')
            e_priority = edge.get('priority')
            edge_dict = {
                'id': edge_id,
                'from': e_from,
                'to': e_to,
                'priority': e_priority}
        lanes = []
        for lane in edge.iter('lane'):
            lane_dict = lane.attrib
            lanes.append(lane_dict)
        edge_dict['lanes'] = lanes
        edges.append(edge_dict)

    edges_origin = edges
    # 获取边的数量
    num_edges = len(edges)

    # 存储旧id和新id的映射关系
    edge_id_map = {}
    lane_id_map = {}

    # 遍历edges，并替换id和lanes中的id
    for i in range(num_edges):
        # 替换边的id
        old_edge_id = edges[i]['id']
        new_edge_id = str((i + 1) * 100)
        # ! Attention:带有"internal"的边属于自动生成的边,一般来说需要数字id前面加上":"
        # if 'function' in edges[i]:
        #     if edges[i]['function']=="internal":
        #         new_edge_id=str(":"+new_edge_id)
        edge_id_map[old_edge_id] = new_edge_id
        edges[i]['id'] = new_edge_id

        # 获取车道的数量
        num_lanes = len(edges[i]['lanes'])

        # 定义一个计数器，用于生成lane的id
        lane_id_counter = 1

        # 遍历车道，并替换id
        for j in range(num_lanes):
            old_lane_id = edges[i]['lanes'][j]['id']

            # the difference between the generation of lane_id
            # now the lane_id is  200_1
            new_lane_id = str((i + 1) * 100) + "_" + str(-1 + lane_id_counter)
            # however, lane_id here is 200+1=201
            # new_lane_id = str((i+1) * 100 + lane_id_counter)

            lane_id_map[old_lane_id] = new_lane_id
            edges[i]['lanes'][j]['id'] = new_lane_id
            lane_id_counter += 1

    # 保存结果
    with open('res/result_edges_parse.json', 'w') as f:
        json.dump(edges, f)
    with open('res/result_id_map_edge.json', 'w') as f:
        json.dump(edge_id_map, f)
    with open('res/result_id_map_lane.json', 'w') as f:
        json.dump(lane_id_map, f)

    return [edges_origin, edges, edge_id_map, lane_id_map]


def parse_junction(root, lane_id_map):
    """
    This function is used to extract junction tags
    Args:
        root: the origin net.xml
        lane_id_map:  (old_lane_id: new_lane_id)

    Returns: results is preserved in /res

    """
    junctions = []
    for junction in root.iter('junction'):
        junction_id = junction.get('id')
        junction_type = junction.get('type')
        junction_dict = {'id': junction_id, 'type': junction_type}
        junction_dict.update(junction.attrib)
        requests = []
        for request in junction.iter('request'):
            request_dict = request.attrib
            requests.append(request_dict)
        junction_dict['requests'] = requests
        junctions.append(junction_dict)

    junctions_origin = junctions

    # 替换边的新id
    # 自动生成的junction(其id为边id, 对应的edge标签带有function="internal"), 需要加上":"
    for x in junctions:
        inc_lanes = x['incLanes'].split()
        for i in range(len(inc_lanes)):
            if inc_lanes[i] in lane_id_map:
                inc_lanes[i] = lane_id_map[inc_lanes[i]]
        x['incLanes'] = ' '.join(inc_lanes)

        int_lanes = x['intLanes'].split()
        for i in range(len(int_lanes)):
            if int_lanes[i] in lane_id_map:
                int_lanes[i] = lane_id_map[int_lanes[i]]
        x['intLanes'] = ' '.join(int_lanes)

        # ! Attention: # 以带有"internal"的边id为junction的新id,
        # 属于自动生成的junction, 地图上多个junction重合, 只保留一个主要的junction
        # 一般来说需要数字id前面加上":"
        if x['id'] in lane_id_map:
            x['id'] = str(":" + lane_id_map[x['id']])

    # 保存结果
    with open('res/result_junctions_parse.json', 'w') as f:
        json.dump(junctions, f)

    return junctions_origin, junctions


def parse_connection(root, edge_id_map, lane_id_map):
    """
    This function is used to extract connection tags
    Args:
        root: the origin net.xml
        edge_id_map: (old_edge_id: new_edge_id)
        lane_id_map: (old_lane_id: new_lane_id)

    Returns: results is preserved in /res

    """
    connections = []
    for connection in root.iter('connection'):
        connection_dict = connection.attrib
        connections.append(connection_dict)
    connections_origin = connections

    # 替换边的新id
    for x in connections:
        if x['from'] in edge_id_map:
            x['from'] = edge_id_map[x['from']]
        if x['to'] in edge_id_map:
            x['to'] = edge_id_map[x['to']]
        if 'via' in x and x['via'] in lane_id_map:
            x['via'] = lane_id_map[x['via']]

    # 保存结果
    with open('res/result_connections_parse.json', 'w') as f:
        json.dump(connections, f)

    return connections_origin, connections


def parse_xml_main(net_xml_file):
    """
    This function is used to call detail parse functions mentioned above
    Args:
        net_xml_file: the origin net.xml

    Returns: None

    """
    # 解析XML文件
    tree = ET.parse(net_xml_file)
    root = tree.getroot()

    # 定义存储edge、junction和connection的列表
    edges_origin, edges, edge_id_map, lane_id_map = parse_edges(root=root)
    junctions_origin, junctions = parse_junction(
        root=root, lane_id_map=lane_id_map)
    connections_origin, connections = parse_connection(
        root=root, edge_id_map=edge_id_map, lane_id_map=lane_id_map)

    print("edge tage number: ", len(edges))
    print("junction tage number: ", len(junctions))
    print("connect tage number: ", len(connections))
    print("Parse net.xml is completed!")
