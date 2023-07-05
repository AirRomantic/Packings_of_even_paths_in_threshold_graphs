import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.threshold import is_threshold_graph


def print_values(*args):
    print("__________")
    for item in args:
        print(item)
    print("__________")


def draw_graf(Graf):
    nx.draw_networkx(Graf, pos=nx.kamada_kawai_layout(Graf))
    plt.show()


def draw_two_graf(Graf1, Graf2):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 5))
    nx.draw_networkx(Graf1, pos=nx.kamada_kawai_layout(Graf1), ax=ax1)
    nx.draw_networkx(Graf2, pos=nx.kamada_kawai_layout(Graf2), ax=ax2)
    plt.show()


def get_unique_list(array):
    unique = []

    for number in array:
        if number in unique:
            continue
        else:
            unique.append(number)
    array.clear()
    for item in unique:
        array.append(item)


def sorted_bubble_degree_nodes(array, N):
    for i in range(N - 1):
        for j in range(N - i - 1):
            if G.degree(array[j]) > G.degree(array[j + 1]):
                buff = array[j]
                array[j] = array[j + 1]
                array[j + 1] = buff


def sorted_by_independent_set_nodes(array, independent_set_array):
    interim_list = []
    for item in array:
        interim_list.append(item)
    array.clear()
    for node in independent_set_array:
        for clique_node in G.neighbors(node):
            array.append(clique_node)
    for item in interim_list:
        array.append(item)
    get_unique_list(array)


def rest_packing(clique_array, easy_way, n):
    if len(easy_way) == 0:
        for i in range(n - 1):
            PG.add_edge(clique_array[0], clique_array[1])
            del clique_array[0]
        del clique_array[0]
    else:
        PG.add_edges_from(easy_way)
        last_node_easy_way = easy_way[-2][1]
        for i in range(n - len(easy_way) - 1):
            PG.add_edge(last_node_easy_way, clique_array[0])
            last_node_easy_way = clique_array[0]
            del clique_array[0]
        easy_way.clear()
    if len(clique_array) >= n:
        rest_packing(clique_array, easy_way, n)


def get_graph_packing(clique_array, independent_set_array, n):
    i = 0
    easy_way = []
    for item in independent_set_array.copy():
        if len(clique_array) != 0:
            if G.has_edge(item, clique_array[0]):
                easy_way.append((item, clique_array[0]))
                if i > 0:
                    easy_way.append((back_delet_node, item))
                back_delet_node = clique_array[0]
                del clique_array[0]
                i = i + 1
            independent_set_array.remove(item)
            if i == n / 2:
                PG.add_edges_from(easy_way)
                easy_way.clear()
                i = 0
                break
    if len(independent_set_array) >= n / 2:
        get_graph_packing(clique_array, independent_set_array, n)
    elif len(clique_array) + 2 * i >= n:
        rest_packing(clique_array, easy_way, n)


list_graf = [(1, 5), (2, 5), (3, 5), (4, 5), (8, 5), (1, 8), (2, 8), (4, 8), (3, 8), (6, 8), (7, 8), (5, 9), (1, 9), (2, 9), (4, 9), (3, 9), (6, 9), (7, 9), (8, 9)]
#list_graf = [(1, 5), (2, 5), (3, 5), (4, 5), (8, 5), (1, 8), (2, 8), (4, 8), (3, 8), (6, 8), (7, 8)]
#list_graf = [(1, 5), (2, 5), (3, 5), (4, 5), (8, 5), (1, 8), (2, 8), (4, 8), (3, 8), (6, 8), (7, 8), (10, 1), (10, 5),(10, 8)]
# инициализируем данный граф G и граф упаковки PG
G = nx.Graph()
PG = nx.Graph()
# определяем все ребра данного графа G
G.add_edges_from(list_graf)
# находим все максимальные клики данного графа G
max_cliques_G = [item for item in nx.find_cliques(G)]
# находим клику с максимальным колличеством вершин
clique_list = sorted(max_cliques_G, key=lambda item: -len(item))[0]
# находим неависимое множество вершин
independent_set_list = list(G.nodes)
for item in clique_list:
    independent_set_list.remove(item)
# совершенно упорядочением клику и независимое множество
sorted_bubble_degree_nodes(independent_set_list, len(independent_set_list))
sorted_by_independent_set_nodes(clique_list, independent_set_list)
# выводим значения: является ли наш граф пороговым, и совершенное множество(клика и независимое множество)
print_values(is_threshold_graph(G), independent_set_list, clique_list)
# упаковываем граф G в граф PG
get_graph_packing(clique_list, independent_set_list, 6)
# рисуем данный нам граф G и граф упаковки PG
draw_two_graf(G, PG)
print_values(independent_set_list, clique_list)