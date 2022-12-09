
# CAT: A Web3 Application for Detecting Ponzi Accounts
With the prevalence of blockchain as an investment opportunity, particularly with rapidly growing crypto-currencies like Bitcoin and Ether, scams and fraud on blockchains have also become common-place. With the massive amounts of transactions being executed every minute, it is impossible to manually verify every transaction that occurs, and the exact nature of any two scams may be wildly different. As such, it seems appropriate to leverage machine learning in detecting fraudulent or scam activity on blockcahins. We aimed to develop a full-stack system that would allow anyone to quickly check an address's history on the Ethereum blockchain and get a prediction of its trustworthiness.

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

# Folders
* application - Contains flask app files.
* data - Contains data processing notebook.
* figures - Figures used for final report.
* model - Model and experiment files.
* smart_contract - Smart contract files.
