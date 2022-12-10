import numpy as np
import pandas as pd


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


# stage 1
def count_stats(array) -> pd.Series:
    statistics_fun = {'expectation': expectation,
                      'dispersion': dispersion,
                      'standard_deviation': stand_dev,
                      'coefficient_of_variation': coeff_var}

    stats = pd.Series(index=['expectation',
                             'dispersion',
                             'standard_deviation',
                             'coefficient_of_variation'])

    array = np.array(array)
    for stat in statistics_fun:
        stats.at[stat] = round(statistics_fun[stat](array), 2)

    return stats
