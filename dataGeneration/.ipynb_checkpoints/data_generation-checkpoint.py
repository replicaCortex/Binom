from scipy.stats import norm, binom, poisson
import numpy as np


def poisson_pmf(k, lambda_):
    """[TODO:description]

    Args:
        k ([TODO:parameter]): [TODO:description]
        lambda_ ([TODO:parameter]): [TODO:description]

    Returns:
        [TODO:return]
    """
    return poisson.pmf(k, lambda_)


def moivre_pmf(k, n: int, p: float, correction=True) -> np.ndarray:
    """[TODO:description]

    Args:
        k ([TODO:parameter]): [TODO:description]
        n ([TODO:parameter]): [TODO:description]
        p ([TODO:parameter]): [TODO:description]
        correction ([TODO:parameter]): [TODO:description]

    Returns:
        [TODO:return]
    """
    mu = n * p
    sigma = np.sqrt(n * p * (1 - p))
    k = np.asarray(k)

    if sigma == 0:
        return np.where(k == mu, 1.0, 0.0)

    if correction:
        lower = (k - 0.5 - mu) / sigma
        upper = (k + 0.5 - mu) / sigma

    else:
        lower = (k - mu) / sigma
        upper = (k + 1 - mu) / sigma

    probs = norm.cdf(upper) - norm.cdf(lower)
    probs = np.where((k < 0) | (k > n), 0.0, probs)

    return probs


def binom_pmf(k: np.ndarray, n: int, p: float) -> np.ndarray:
    """[TODO:description]

    Args:
        k ([TODO:parameter]): [TODO:description]
        n ([TODO:parameter]): [TODO:description]
        p ([TODO:parameter]): [TODO:description]

    Returns:
        [TODO:return]
    """
    return binom.pmf(k, n, p)
