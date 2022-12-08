from application.utils import create_feature_dataframe, MDM, scaleParams
from application.constants import (
	ADDRESS_REGEX,
	MUS, SIGMAS,
	SCALER_MUS, SCALER_SIGMAS,
	EPSILON,
	CONTRACT_ADDRESS, NODE_URL, ABI,
	FEATURES,
	DIGITS,
)

from flask import Flask, render_template, request, redirect, url_for

import pandas as pd
import numpy as np
import time

import re
address_check = re.compile(ADDRESS_REGEX)

from web3 import Web3
global web3
global contract
web3 = Web3(Web3.HTTPProvider(NODE_URL))
contract = web3.eth.contract(address=Web3.toChecksumAddress(CONTRACT_ADDRESS), abi=ABI)

import etherscan
global es
es = etherscan.Client(
	api_key="2P3PIIJR5ETQIDMQET74N8B9HWT5DGJFXY", #CSCI6964 Project
	cache_expire_after=5
)

global WARNING
global CLASSIFICATION
global ADDRESS
WARNING = None
CLASSIFICATION = None

app = Flask(__name__, template_folder="application/templates")
app.config["SECRET_KEY"] = "YOUR SECRET KEY"

@app.route('/', methods=["POST", "GET"])
def index():
	"""
	Render the index.html template and handle text-field address submission

	Text Field:
		Input
			- Address as hexadecimal value string
		Behavior
			- Pass address to process.html
	"""
	global WARNING
	global CLASSIFICATION
	global ADDRESS
	print("Index")
	if not web3.isConnected():
		WARNING = "WARNING: No connection to web3 is present."
	if WARNING:
		print("Warning")
		_w = WARNING
		WARNING = None
		return render_template("index.html", warning=_w)
	if CLASSIFICATION:
		print("Classification")
		_c = CLASSIFICATION
		CLASSIFICATION = None
		return render_template("index.html", classification=_c, address=ADDRESS, alert="success" if _c=="Trustworthy" else "warning")
	return render_template("index.html")

@app.route('/get_features', methods=["POST", "GET"])
def get_features():
	"""
	Verify address, pull transaction history, engineer features, and run classification
	"""
	global WARNING
	global CLASSIFICATION
	global ADDRESS
	global es
	global web3
	global contract
	print("Get Features")
	address = request.form["address"]
	account = request.form["account"]
	pk = request.form["pk"]
	gas = int(request.form["gas"])
	gasPrice = request.form["gasPrice"]
	ADDRESS = address
	print(address)
	if not address_check.match(address.lower()):
		print("INVALID ADDRESS")
		WARNING = f"WARNING: {address} is not a valid Ethereum Address. Please double check formatting."
		return redirect(url_for(".index"))

	if not address_check.match(account.lower()):
		print("INVALID ACCOUNT")
		WARNING = f"WARNING: {account} is not a valid Ethereum Address. Please double check formatting"
		return redirect(url_for(".index"))

	transactions = es.get_transactions_by_address(address)
	df = pd.DataFrame(transactions)
	df["value"] = df["value"].astype(float) * 1e-18
	df["gasLimit"] = df["gas"]
	features = create_feature_dataframe(df)
	features = features[FEATURES]
	features = features.to_numpy().flatten()
	features = (features - np.array(SCALER_MUS)) / np.array(SCALER_SIGMAS)
	inputs = scaleParams(features, DIGITS)

	print(inputs)
	txn_dict = {
		"from" : account,
		'nonce': web3.eth.getTransactionCount(account),
		"gas" : gas,
		"gasPrice" : web3.toWei(gasPrice, 'gwei'),
	}
	txn = contract.functions.detection(inputs[0], inputs[1], inputs[2], inputs[3]).buildTransaction(txn_dict)
	signed_txn = web3.eth.account.signTransaction(txn, private_key=pk)
	sent_txn = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

	try:
		txn_receipt = web3.eth.get_transaction_receipt(sent_txn)
		print(f"TXN : {txn_receipt}")
		CLASSIFICATION = "Trustworthy" if txn_receipt["logs"][0]["return"] else "Not Trustworthy"
	except:
		time.sleep(5)
		score = MDM(features, np.array(MUS), np.array(SIGMAS))
		print(score)
		CLASSIFICATION = "Trustworthy" if score >= EPSILON else "Not Trustworthy"
	return redirect(url_for(".index"))
