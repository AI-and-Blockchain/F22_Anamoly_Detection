import numpy as np
from scipy.stats import multivariate_normal

class MahalanobisDistenceMethod():
    """
    Implements the Mahalanobis distence method for anomaly detection.

    Methods:
        set_epsilon: Update threshold for classification.
        parameters: Returns the multivariate normal model parameters.
        fit: Fits MD method to a dataset.
        predict: Runs prediction using MD method on a dataset.
        classify: Runs classification using MD method on a dataset.
        evaluate: Evaluates MD method accuracy on a dataset.
    """
    def __init__(self, epsilon=0.98):
        """
        Initializes an instance of the MahalanobisDistenceMethod class.

        Parameters:
            epsilon [float]: Threshold to classify a point as an anomaly.
        """
        self._epsilon = epsilon
        
        self._mu = None
        self._cov = None
        
        self.model = None
        
    def set_epsilon(self, epsilon):
        """
        Update epsilon value for thresholding in classification.

        Parameters:
            epsilon [float]: Threshold to classify a point as an anomaly.
        """
        self._epsilon = epsilon
    
    def parameters(self):
        """
        Get the model parameters.

        Return:
            [tuple[numpy.ndarray, numpy.ndarray]] -- Tuple containing mean and covariance matrix.
        """
        return (self._mu, self._cov)

    def fit(self, X):
        """
        Fits MD method to a dataset.

        Parameters:
            X [numpy.ndarray]: Dataset of shape (N, M) where N is the number of datapoints and M is the number 
                                of features.

        Exception:
            If data results in a non-postive definite covaraince matrix then an exception is raised.
        """
        m, _ = X.shape

        self._mu = np.mean(X, axis=0)
        self._cov = np.cov(X.T)  
        
        self.model = multivariate_normal(mean=self._mu, cov=self._cov, allow_singular=True)

    def predict(self, X):
        """
        Runs prediction using MD method on a dataset.

        Parameters:
            X [numpy.ndarray]: Dataset of shape (N, M) where N is the number of datapoints and M is the number 
                                of features which is the same size as the number of features the model was fit on.

        Returns:
            [numpy.ndarray]: Probability of anomaly.

        Exception:
            If an instance of this class hasn't been fitted to a dataset then an exception is raised.
        """
        if self.model is None:
            raise Exception("You must fit model before predicting.")   
        return self.model.pdf(X)

    def classify(self, X):
        """
        Runs classification using MD method on a dataset.

        Parameters:
            X [numpy.ndarray]: Dataset of shape (N, M) where N is the number of datapoints and M is the number 
                                of features which is the same size as the number of features the model was fit on.

        Returns:
            [numpy.ndarray]: Array of classifications based on epsilon where 1 means anomaly and 0 mean non-anomaly.
        """
        p = self.predict(X)
        return p <= self._epsilon

    def evaluate(self, X, y):
        """
        Evaluates MD method accuracy on a dataset.

        Parameters:
            X [numpy.ndarray]: Dataset of shape (N, M) where N is the number of datapoints and M is the number 
                                of features which is the same size as the number of features the model was fit on.
            y [numpy.ndarray]: A binary ground truth classification vector of size (N).

        Returns:
            [float]: MD method accuracy.
        """
        N_scam = len(np.where(y == 1)[0])
        N_legit = len(y) - N_scam

        y_hats = self.predict(X)
        sorted_idxs = np.argsort(y_hats)

        y_hats = y_hats[sorted_idxs]
        y = y[sorted_idxs]

        y_cls = np.zeros(len(y))

        tp = [np.sum((y_cls == y) & (y_cls == 1))]
        fp = [np.sum((y_cls != y) & (y_cls == 1))]
        tn = [np.sum((y_cls == y) & (y_cls == 0))]
        fn = [np.sum((y_cls != y) & (y_cls == 0))]

        acc = [(tp[0] + tn[0]) / len(y)]
        s_acc = [tp[0] / N_scam]
        l_acc = [tn[0] / N_legit]
        prc = [tp[0] / (tp[0] + fp[0]) if tp[0] + fp[0] != 0 else 0.0]
        rec = [tp[0] / (tp[0] + fn[0]) if tp[0] + fn[0] != 0 else 0.0]
        f1s = [2 * prc[0] * rec[0] / (prc[0] + rec[0]) if prc[0] + rec[0] != 0 else 0.0]

        for i, eps in enumerate(y_hats):
            y_cls[i] = 1

            if y_cls[i] == y[i]:
                tp.append(tp[-1] + 1)
                fn.append(fn[-1] - 1)

                tn.append(tn[-1])
                fp.append(fp[-1])
            else:
                tn.append(tn[-1] - 1)
                fp.append(fp[-1] + 1)

                tp.append(tp[-1])
                fn.append(fn[-1])

            s_acc.append(tp[-1] / N_scam)
            l_acc.append(tn[-1] / N_legit)

            acc.append((tp[-1] + tn[-1]) / len(y))
            prc.append(tp[-1] / (tp[-1] + fp[-1]) if tp[-1] + fp[-1] != 0 else 0.0)
            rec.append(tp[-1] / (tp[-1] + fn[-1]) if tp[-1] + fn[-1] != 0 else 0.0)
            f1s.append(2 * prc[-1] * rec[-1] / (prc[-1] + rec[-1]) if prc[-1] + rec[-1] != 0 else 0.0)

        results = {
            "epsilon": np.hstack((np.array([0]),y_hats)),
            "accuracy": np.array(acc),
            "legit_accuracy": np.array(l_acc),
            "scam_accuracy": np.array(s_acc),
            "precision": np.array(prc),
            "recall": np.array(rec),
            "f1-score": np.array(f1s),
            "true_postive": np.array(tp),
            "false_postive": np.array(fp),
            "true_negative": np.array(tn),
            "false_negative": np.array(fn)
        }

        return results