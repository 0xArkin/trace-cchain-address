import sys
import requests
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def scrap(address):
    # get contracts
    """endpoint = "https://api.covalenthq.com/v1/43114/tokens/tokenlists/all/"
    contracts = requests.get(endpoint.format(address)).json()
    if contracts["error"]:
        print("error: can't fetch contracts")
        quit()
    contracts = contracts["data"]["items"]
    contracts = [contract['contract_address'] for contract in contracts]
    """
    contracts = [line.rstrip() for line in open('contracts.csv')]

    # get transactions
    endpoint = "https://api.covalenthq.com/v1/43114/address/{}/transactions_v2/?page-size=999999"
    r = requests.get(endpoint.format(address)).json()

    if r["error"]:
        print('error: verify your address')
        quit()

    nodes = []
    edges = []
    for tx in r["data"]["items"]:
        if type(tx['from_address']) is str and type(tx['to_address']) is str:
            line = tx['from_address'] + ',' + tx['to_address']
            edges.append(line)
            if tx['from_address'] not in nodes:
                nodes.append(tx['from_address'])
            if tx['to_address'] not in nodes:
                nodes.append(tx['to_address'])
    print(f"{len(r['data']['items'])} transactions found")

    g = nx.DiGraph()
    for edge in edges:
        x = edge.split(",")
        g.add_edge(x[0], x[1], weight=edges.count(edge))
    pos = nx.spring_layout(g, k=15 * 1 / np.sqrt(len(g.nodes())), iterations=20)
    edge_labels = {(u, v): d['weight'] for u, v, d in g.edges(data=True)}

    pos_attrs = {}
    for node, coords in pos.items():
        pos_attrs[node] = (coords[0], coords[1] + 0.08)

    labels = {}
    color_map = []
    for index, item in enumerate(g.nodes):
        labels[item] = item[0:8]
        if item == address.lower():
            color_map.append('red')
        elif item in contracts:
            color_map.append('orange')
        else:
            color_map.append('grey')

    nx.draw_networkx_nodes(g, pos, node_size=20, node_color=list(color_map))
    nx.draw_networkx_edges(g, pos)
    nx.draw_networkx_labels(g, pos_attrs, font_size=8, labels=labels)
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)
    plt.title(address + " -> " + str(len(r['data']['items'])) + " transactions")
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    """
    if len(sys.argv) != 2:
        print("usage: python3 main.py address")
        quit()
    scrap(sys.argv[1])
    """
    scrap("0xBd1509926AC0Fee9F49D3959d00eFA5500476cFE")
