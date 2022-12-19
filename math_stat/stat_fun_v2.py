import numpy as np
import pandas as pd
import scipy.stats as ss


# stage 1
def expectation(a):
    return a.sum() / len(a)


# stage 1
def dispersion(a):
    n = len(a)
    return (expectation(a * a) - (expectation(a)) ** 2) * n / (n - 1)


# stage 1
def coeff_var(a):
    return stand_dev(a) / expectation(a)


# stage 1
def stand_dev(a):
    return np.sqrt(dispersion(a))


# stage 2
def conf_int(a, p=0.9):
    t_p = ss.norm.ppf((1 + p) / 2)
    sigma_m = np.sqrt(dispersion(a) / len(a))
    eps = sigma_m * t_p
    return round(eps, 2)


def get_shifted(a, k):
    n = len(a)
    return a[:n - k], a[k:]


def cov_n(X, Y):
    E_x = expectation(X)
    E_y = expectation(Y)
    return ((X - E_x) * (Y - E_y)).sum()


def correlation(X, Y):
    return round(cov_n(X, Y) / np.sqrt(cov_n(X, X) * cov_n(Y, Y)), 4)


def auto_corr_analyse(array, ks):
    return correlation(*get_shifted(array, ks))


def count_stats(array: np.array, confidence: float = None, autocorr: float = None) -> dict:
    statistics_fun = {'expectation': expectation,
                      'dispersion': dispersion,
                      'standard_deviation': stand_dev,
                      'coefficient_of_variation': coeff_var}

    stats = pd.Series(index=['expectation',
                             'dispersion',
                             'standard_deviation',
                             'coefficient_of_variation'])

    array = array
    for stat in statistics_fun:
        stats.at[stat] = round(statistics_fun[stat](array), 2)
    if confidence:
        stats.at['confidence_interval'] = conf_int(array, p=0.9)
    if autocorr:
        stats.at['autocorrelation_coefficient'] = auto_corr_analyse(array, autocorr)
    return stats.to_dict()
