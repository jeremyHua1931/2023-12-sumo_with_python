# -*- encoding: utf-8 -*-
"""
@File    :   utils.py
@Contact :   jeremyhua@foxmail.com

@Modify Time      @Author       @Version     @Description
------------      -------       --------     -----------
2023/3/1 23:26   HuaZhangzhao    1.0          some utils function
"""
import pytz
import sumolib
from datetime import datetime


def get_datetime():
    """
    This function is used to format the time

    Returns: such as "2023-03-02 11:42:07.701"

    """
    utc_now = pytz.utc.localize(datetime.now())
    daytime = utc_now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    return daytime


def flatten_list(_2d_list):
    """
    This function is used to deal with some list on special situation

    Args:
        _2d_list: input list

    Returns: output list

    """
    flat_list = []
    for element in _2d_list:
        if isinstance(element, list):
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list


def get_net_info():
    """
    This function is used to get junction and edge information with sumolib
    Returns: info_*.txt is in /sumo/info folder

    """
    print("Execute: get_net_info()")

    f_junction_info = open("sumo/info/info_junction.txt", 'w')
    print(datetime.now(), file=f_junction_info)

    f_edge_info = open("sumo/info/info_edge.txt", 'w')
    print(datetime.now(), file=f_edge_info)

    net = sumolib.net.readNet('sumo/map.net.xml')

    # 获取网络中所有节点的x信息
    nodes = net.getNodes()
    print("Network Nodes:\nID\t\t\tX\t\t\tY", file=f_junction_info)
    for node in nodes:
        node_id = node.getID()
        node = net.getNode(node_id)
        x, y = node.getCoord()
        print(
            "{}\t\t{}\t\t{}".format(
                node.getID(),
                x,
                y),
            file=f_junction_info)
    f_junction_info.close()

    # 获取网络中所有边的信息
    edges = net.getEdges()
    print("\nNetwork Edges:\nID\t\t\tFrom\t\t\tTo\t\t\tLength", file=f_edge_info)
    for edge in edges:
        print("{}\t\t{}\t\t{}\t\t{}".format(edge.getID(), edge.getFromNode().getID(),
                                            edge.getToNode().getID(), edge.getLength()), file=f_edge_info)
    f_edge_info.close()

    print("get_net_info() is completed !")
