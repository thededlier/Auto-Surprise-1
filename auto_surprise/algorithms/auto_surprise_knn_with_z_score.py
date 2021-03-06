from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from surprise import KNNWithZScore
from surprise.model_selection import cross_validate
from auto_surprise.constants import DEFAULT_MAX_EVALS, ACCURACY_METRICS
from auto_surprise.algorithms.spaces import KNN_DEFAULT_SPACE
from auto_surprise.algorithms.base import AlgorithmBase

class AutoSurpriseKNNWithZScore(AlgorithmBase):
    """
    Wrapper for surprise.prediction_algorithms.knns.KNNWithZScore
    """
    def _hyperopt(self, params):
        algo = KNNWithZScore(**params)
        return cross_validate(algo, self._data, measures=ACCURACY_METRICS, cv=self._cv, n_jobs=self._cv_n_jobs, verbose=self._debug)[self._metric].mean()

    def _objective(self, params):
        loss = self._hyperopt(params)
        self._result_logger.append_results(loss)

        return {
            'loss': loss,
            'status': STATUS_OK,
            'hyperparams': params
        }

    def best_hyperparams(self, max_evals):
        best = fmin(
            self._objective,
            KNN_DEFAULT_SPACE,
            algo=self._hpo_algo,
            max_evals=max_evals,
            trials=self.trials
        )

        return best, self.trials
