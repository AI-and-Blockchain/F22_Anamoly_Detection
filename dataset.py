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
    implemented_features = ['in_deg', 'out_deg', 'value', 'time', 'ain', 'aout', 'uin', 'uout', 'int_in', 'int_out', 'cluster']

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
        print("Writing edge network to pickle file")
        efile = open('datasets/pickles/real_edges', 'wb')
        pickle.dump(edge_network, efile)
    efile.close()

    for edge in edges:
            if edge[0] in edge_network.keys() and edge[1] in edge_network.keys():
                edge_network[edge[0]]['in_deg'] = 0
                edge_network[edge[1]]['out_deg'] = 0


    for edge in edges:
        if edge[0] in edge_network.keys() and edge[1] in edge_network.keys():

            # In degree
            edge_network[edge[1]]['in_deg'] += 1
            # Out degree
            edge_network[edge[0]]['out_deg'] += 1

            # Unique In degree, in time
            if 'uin' not in edge_network[edge[1]].keys():
                edge_network[edge[1]]['uin_list'] = set()
                edge_network[edge[1]]['in_time'] = set()
            edge_network[edge[1]]['uin_list'].add(edge[0])
            edge_network[edge[1]]['in_time'].add(edge_network[edge[0]]['time'])

            # Unique Out degree, out time
            if 'uout' not in edge_network[edge[0]].keys():
                edge_network[edge[0]]['uout_list'] = set()
                edge_network[edge[0]]['in_time'] = set()
            edge_network[edge[0]]['uout_list'].add(edge[1])
            edge_network[edge[1]]['in_time'].add(edge_network[edge[1]]['time'])

            # Average in-transaction
            if 'ain' not in edge_network[edge[1]].keys():
                edge_network[edge[1]]['ain'] = 0
            edge_network[edge[1]]['ain'] += edge_network[edge[0]]['value']

            # Average out-transaction
            if 'aout' not in edge_network[edge[0]].keys():
                edge_network[edge[0]]['aout'] = 0
            edge_network[edge[0]]['aout'] += edge_network[edge[1]]['value']

    # Calculate average in, out, time intervals
    for edge in edge_network.keys():
        if 'ain' not in edge_network[edge].keys():
            edge_network[edge]['ain'] = 0
        else:
            edge_network[edge]['ain'] /= edge_network[edge]['in_deg']
        if 'aout' not in edge_network[edge].keys():
            edge_network[edge]['aout'] = 0
        else:
            edge_network[edge]['aout'] /= edge_network[edge]['out_deg']

        # Average In intervals
        in_intervals, out_intervals = 0, 0
        if 'in_time' in edge_network[edge].keys():
            ins = list(edge_network[edge]['in_time'])
            if len(ins) > 1:
                ins.sort()
                for i in range(len(ins) - 1):
                    in_intervals += abs(ins[i] - ins[i+1])
                in_intervals /= (len(ins) - 1)
        if 'out_time' in edge_network[edge].keys():
            outs = list(edge_network[edge]['out_time'])
            if len(outs) > 1:
                outs.sort()
                for i in range(len(outs) - 1):
                    out_intervals += abs(outs[i] - outs[i+1])
                out_intervals /= (len(outs) - 1)

        edge_network[edge]['int_in'] = in_intervals
        edge_network[edge]['int_out'] = out_intervals

        n = set()

        if 'uin' not in edge_network[edge].keys():
            edge_network[edge]['uin'] = 0
        else:
            n = n.union(edge_network[edge]['uin_list'])
            edge_network[edge]['uin'] = len(list(edge_network[edge]['uin_list']))
        if 'uout' not in edge_network[edge].keys():
            edge_network[edge]['uout'] = 0
        else:
            n = n.union(edge_network[edge]['uout_list'])
            edge_network[edge]['uout'] = len(list(edge_network[edge]['uout_list']))

        if len(list(n)) > 1:
            clustering = 0
            for j in n:
                for k in n:
                    if j in edge_network.keys() and k in edge_network[j]['uout_list']:
                        clustering += 1
            clustering /= (len(list(n)) * (len(list(n) - 1)))
        else:
            clustering = 0
        edge_network[edge]['cluster'] = clustering

    X, Y = [], []
    labels = {'unknown':0, '1':1, '2':2}

    for point, label in classes:
        if point in edge_network.keys():
            x = [edge_network[point][f] for f in rows]
            X.append(x)
            Y.append(labels[label])
    return X, Y

# X, Y = get_X_Y(['in_deg', 'out_deg', 'value'])
# print(len(X), len(X[0]))
# print(len(Y))


# test = set()
# classes, edges, features = load_dataset()
# test.add(edges[0][0])
# test.add(edges[0][1])
# print(test)