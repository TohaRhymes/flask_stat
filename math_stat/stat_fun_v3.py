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


def count_q_t1_t2(t, var):
    q = 2 / (1 + var ** 2) * 0.7
    t1 = (1 + np.sqrt((1 - q) * (var ** 2 - 1) / (2 * q))) * t
    t2 = (1 - np.sqrt(q * (var ** 2 - 1) / (2 * (1 - q)))) * t
    return q, t1, t2


def hyperexp(t, var, n) -> np.array:
    q, t1, t2 = count_q_t1_t2(t, var)
    dist1 = ss.expon(scale=t1).rvs(size=n)
    dist2 = ss.expon(scale=t2).rvs(size=n)
    d1_d2 = ss.uniform.rvs(size=n) < q
    array = np.concatenate([dist1[d1_d2], dist2[~d1_d2]])
    np.random.shuffle(array)
    return array


def exp(t, var, n) -> np.array:
    return ss.expon(scale=t).rvs(size=n)


def erlang(t, var, n) -> np.array:
    return ss.expon(scale=t).rvs(size=n) + ss.expon(scale=t).rvs(size=n)


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


def generate(stats: dict, n: int) -> np.array:
    t = stats["expectation"]
    var = stats["coefficient_of_variation"]

    if var > 1:
        return hyperexp(t, var, n)
    elif var < 1:
        return erlang(t, var, n)
    else:
        return exp(t, var, n)
