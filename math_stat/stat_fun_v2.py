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


# stage 1->2
def count_stats(array) -> pd.Series:
    statistics_fun = {'Expectation': expectation,
                      'Dispersion': dispersion,
                      'Standard deviation': stand_dev,
                      'Coefficient of variation': coeff_var}

    stats = pd.Series(index=['Expectation',
                             'Confidence interval (0.9)',
                             'Confidence interval (0.95)',
                             'Confidence interval (0.99)',
                             'Dispersion',
                             'Standard deviation',
                             'Coefficient of variation'])

    array = np.array(array)
    for stat in statistics_fun:
        stats.at[stat] = round(statistics_fun[stat](array), 2)
    stats.at['Confidence interval (0.9)'] = conf_int(array, p=0.9)
    stats.at['Confidence interval (0.95)'] = conf_int(array, p=0.95)
    stats.at['Confidence interval (0.99)'] = conf_int(array, p=0.99)

    return stats
