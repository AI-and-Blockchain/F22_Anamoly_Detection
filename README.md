# Dataset install

```
datasets/
    - elliptic_bitcoin_dataset/
        -elliptic_txs_classes.csv
        -elliptic_txs_edgelist.csv
        -elliptic_txs_features.csv
    -pickles
        -real_edges
    -Result.csv
```

https://www.kaggle.com/datasets/alexbenzik/deanonymized-995-pct-of-elliptic-transactions

https://www.kaggle.com/datasets/ellipticco/elliptic-data-set/code?resource=download


# Install Requirements

```
$ python3 -m venv {venv_name}
$ source {venv_name}/bin/activate
$ python3 -m pip install -r requirements.txt
```

# Run Web Application

```
flask --app app --debug run
```
