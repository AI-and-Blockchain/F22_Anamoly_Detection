from flask import Flask, render_template, request, redirect, url_for

import pandas as pd
import numpy as np
import re
from application.utils import create_feature_dataframe, MDM
from application.constants import ADDRESS_REGEX, MUS, SIGMAS, SCALER_MUS, SCALER_SIGMAS, EPSILON
address_check = re.compile(ADDRESS_REGEX)

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
	if WARNING:
		print("Warning")
		_w = WARNING
		WARNING = None
		return render_template("index.html", warning=_w)
	if CLASSIFICATION:
		print("Classification")
		_c = CLASSIFICATION
		CLASSIFICATION = None
		return render_template("index.html", classification=_c, address=ADDRESS)
	return render_template("index.html")

@app.route('/')

# @app.route('/get_features/<string:address>', methods=["POST", "GET"])
# def get_features(address):
# 	print(f"Getting transactions from {address}")
# 	transactions = es.get_transactions_by_address('0x39eB410144784010b84B076087B073889411F878')
# 	print(f"transactions: {transactions}")
# 	return {"transactions" : transactions}

@app.route('/get_features', methods=["POST", "GET"])
def get_features():
	"""
	Verify address, pull transaction history, engineer features, and run classification
	"""
	global WARNING
	global CLASSIFICATION
	global ADDRESS
	global es
	print("Get Features")
	address = request.form["address"]
	ADDRESS = address
	print(address)
	if not address_check.match(address.lower()):
		print("INVALID ADDRESS")
		WARNING = f"WARNING: {address} is not a valid Ethereum Address. Please double check formatting."
		return redirect(url_for(".index"))

	transactions = es.get_transactions_by_address(address)
	df = pd.DataFrame(transactions)
	df["value"] = df["value"].astype(float) * 1e-18
	df["gasLimit"] = df["gas"]
	features = create_feature_dataframe(df)
	features = features[[col for col in features.columns if "benfords" in col]]
	features = features.to_numpy().flatten()
	features = (features - np.array(SCALER_MUS)) / np.array(SCALER_SIGMAS)
	score = MDM(features, np.array(MUS), np.array(SIGMAS))
	print(score)
	CLASSIFICATION = "Legitimate" if score >= EPSILON else "Illegitimate"
	return redirect(url_for(".index"))
