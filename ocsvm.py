import numpy as np
from sklearn.svm import OneClassSVM

class OneClassSVMMethod():
	"""
	Implements the One-Class SVM method for anomaly detection.

	Methods:
	fit: Fits OCSVM method to a dataset.
	predict: Runs prediction using OCSVM method on a dataset.
	classify: Runs classification using OCSVM method on a datset.
	evaluate: Evaluates OCSVM method accuracy on a dataset.
	"""
	def __init__(self, epsilon=0.5, **kwargs):
		"""
		Initializes an instance of the OneClassSVMMethod class.

		Parameters:
		epsilon [float]: Threshold to classify a point as an anomaly.
		kwargs [**dict]: Keyword arguments for initializing Sklearn.svm.OneClassSVM
		"""
		self._epsilon = epsilon

		self._model = OneClassSVM(**kwargs)

	def fit(self, X, **kwargs):
		"""
		Fits OneClassSVM method to dataset.

		Parameters:
		X [numpy.array]: Dataset of shape (N,M) where N is the number of datapoints and M is the number of features.
		kwargs [**dict]: Keyword arguments passed to Sklearn.svm.OneClassSvm.fit
		"""
		self._model.fit(X, **kwargs)

	def predict(self, X, normalize=False):
		"""
		Runs prediction using OneClassSVM method on dataset.

		Parameters:
		X [numpy.ndarray]: Dataset of shape (N, M) where N is the number of datapoints and M is the number 
		of features which is the same size as the number of features the model was fit on.
		normalize [bool]: Flag to normalize data to range [0,1]. Defaults to False

		Returns:
		[numpy.array]: Probability of anomaly
		"""
		scores = self._model.score_samples(X)
		if not normalize:
			return scores
		return (scores - scores.min()) / (scores.max() - scores.min())

	def classify(self, X):
		"""
		Runs classification using OneClassSVM method on a dataset.

		Parameters:
		X [numpy.ndarray]: Dataset of shape (N, M) where N is the number of datapoints and M is the number 
		of features which is the same size as the number of features the model was fit on.

		Returns:
		[numpy.ndarray]: Array of classifications based on epsilon where 0 means anomaly and 1 mean non-anomaly.
		"""
		scores = self.predict(X, True)
		return scores > self._epsilon

	def evaluate(self, X, y):
		"""
		Evaluates OneClassSVM method accuracy on a dataset.

		Parameters:
		X [numpy.ndarray]: Dataset of shape (N, M) where N is the number of datapoints and M is the number 
		of features which is the same size as the number of features the model was fit on.
		y [numpy.ndarray]: A binary ground truth classification vector of size (N).

		Returns:
		[float]: MD method accuracy.
		"""
		y_hat = self.classify(X)
		return np.mean(y_hat == y)