import csv
import pickle
import os.path
import urllib.request
import json

def load_dataset():
    datapath = "datasets/elliptic_bitcoin_dataset/"

    with open(datapath + "elliptic_txs_classes.csv") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        classes = [row for row in reader]

        
    with open(datapath + "elliptic_txs_edgelist.csv") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        edges = [row for row in reader]

    with open(datapath + "elliptic_txs_features.csv") as csvfile:
        features = [row for row in csv.reader(csvfile, delimiter=',')]

    return classes, edges, features

    # users = {}
    # for edge in edges:
    #     for u in edge:
    #         if u not in users.keys():
    #             users[u] = 0
    #         users[u] += 1

    # degrees = {}
    # for user in users.keys():
    #     if users[user] not in degrees.keys():
    #         degrees[users[user]] = 0
    #     degrees[users[user]] += 1

    # print("Number of Users", len(users.keys()))
    # print("Number of Transactions", len(edges))
    # for key in sorted(degrees.keys()):
    #     plt.plot(key, degrees[key], 'b.')
    # plt.yscale('log')
    # plt.savefig('figures/degree_distribution.png')
    # plt.clf()

    # print("Number of Labels", len(classes))
    # print("Number of features", len(features))

def get_txn_real():

    datapath = "datasets/"
    real_txns = {}
    with open(datapath + "Result.csv") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for row in reader:
            real_txns[row[0]] = row[1]


    # For each transaction in list,
    # pull json data from url
    # first id -> update out data, txn value, time
    # second id -> update in data, txn value, time
    # get time from block url req, store in map for the blocks.

    count = 0
    edge_network = {}
    for key in real_txns.keys():
       
        url = 'https://blockchain.info/rawtx/' + real_txns[key]
        try:
            with urllib.request.urlopen(url) as ul:
                count += 1
                data = json.load(ul)
                edge_network[key] = {}
                edge_network[key]['in_deg'] = 0
                edge_network[key]['out_deg'] = 0
                edge_network[key]['value'] = data['inputs'][0]['prev_out']['value']
                edge_network[key]['time'] = data['time']

                if count % 1000 == 0:
                    print(count)
        except:
            continue

    
    return edge_network

def get_X_Y(rows: list[str]):
    implemented_features = ['in_deg', 'out_deg', 'value', 'time']

    for r in rows:
        if r not in implemented_features:
            print("Feature:", r, "not implemented yet")
            exit(1)

    classes, edges, features = load_dataset()
    if os.path.isfile('datasets/pickles/real_edges'):
        print("Reading edge network from pickle file")
        efile = open('datasets/pickles/real_edges', 'rb')
        edge_network = pickle.load(efile)
    else:
        print("Generating edge network from blockchain.info API")
        edge_network = get_txn_real()
        for edge in edges:
            if edge[0] in edge_network.keys() and edge[1] in edge_network.keys():
                edge_network[edge[0]]['in_deg'] += 1
                edge_network[edge[1]]['out_deg'] += 1
        print("Writing edge network to pickle file")
        efile = open('datasets/pickles/real_edges', 'wb')
        pickle.dump(edge_network, efile)
    efile.close()

    X, Y = [], []

    for point, label in classes:
        if point in edge_network.keys():
            x = [edge_network[point][f] for f in rows]
            X.append(x)
            Y.append(label)
    return X, Y

# X, Y = get_X_Y(['in_deg', 'out_deg', 'value'])
# print(len(X), len(X[0]))
# print(len(Y))