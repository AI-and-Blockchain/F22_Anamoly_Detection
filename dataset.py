import csv
import time
import pickle
import matplotlib.pyplot as plt
import urllib.request
import json

def load_dataset():
    datapath = "datasets/elliptic_bitcoin_dataset/"

    # start = time.time()
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
    # end = time.time()
    # print("Read from .csv files in:", end-start)
    # return classes, edges, features


    users = {}
    for edge in edges:
        for u in edge:
            if u not in users.keys():
                users[u] = 0
            users[u] += 1

    degrees = {}
    for user in users.keys():
        if users[user] not in degrees.keys():
            degrees[users[user]] = 0
        degrees[users[user]] += 1

    print("Number of Users", len(users.keys()))
    print("Number of Transactions", len(edges))
    for key in sorted(degrees.keys()):
        plt.plot(key, degrees[key], 'b.')
    plt.yscale('log')
    plt.savefig('figures/degree_distribution.png')
    plt.clf()

    print("Number of Labels", len(classes))
    print("Number of features", len(features))

    # return classes, edges, features

# cfile = open(datapath + "classes", 'wb')
# pickle.dump(classes, cfile)
# cfile.close()
# efile = open(datapath + "edges", 'wb')
# pickle.dump(edges, efile)
# efile.close()
# ffile = open(datapath + "features", 'wb')
# pickle.dump(features, ffile)
# ffile.close()

# start = time.time()
# cfile = open(datapath + "classes", 'rb')
# classes = pickle.load(cfile)
# cfile.close()
# efile = open(datapath + "edges", 'rb')
# edges = pickle.load(efile)
# efile.close()
# ffile = open(datapath + "features", 'rb')
# features = pickle.load(ffile)
# ffile.close()
# end = time.time()
# print("Read from pickle files in:", end-start)

# print(classes[0])
# print(edges[0])
# print(features[0])
# print(len(classes), len(edges), len(features))

# # Split into two graphs: edges as nodes, users as nodes

def get_txn_real():

    # For each transaction in list,
    # pull json data from url
    # first id -> update out data, txn value, time
    # second id -> update in data, txn value, time
    # get time from block url req, store in map for the blocks.

    url = 'https://blockchain.info/rawtx/' + 'd6176384de4c0b98702eccb97f3ad6670bc8410d9da715fe5b49462d3e603993'
    with urllib.request.urlopen(url) as ul:
        data = json.load(ul)
        for key in data.keys():
            print(key, data[key])

get_txn_real()
# load_dataset()




# 230425980 74d9bb85c6bbc471c6e18f409d23c3ef1191725bdb90376fdff66fd31da41043
# -> 5530458 906c816344eb837a6ddcf75dece1c07f0c2a87885e0ea93158d9865648138e2e

# <- 98374661 fc2611086db6f80b635c097a82ee451674a762481c9318684446e2658527566e