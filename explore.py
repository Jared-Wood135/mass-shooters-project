# =======================================================================================================
# Table of Contents START
# =======================================================================================================

'''
1. Orientation
2. Imports
3. binary_list
4. agg_list
'''

# =======================================================================================================
# Table of Contents END
# Table of Contents TO Orientation
# Orientation START
# =======================================================================================================

'''
The purpose of this file is to create functions for specific findings from the 'explore.ipynb' file
to use in the 'model.ipynb' file...
'''

# =======================================================================================================
# Orientation END
# Orientation TO Imports
# Imports START
# =======================================================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import wrangle as w

# =======================================================================================================
# Imports END
# Imports TO binary_list
# binary_list START
# =======================================================================================================

def binary_list():
    '''
    Obtains the 4 unique binary lists that passed filters in order to be used in modeling...

    INPUT:
    NONE

    OUTPUT:
    strong_zeros_high_ratio_col = List of column names that have a 70%+ ratio for zero, highvolatility values
    strong_zeros_low_ratio_col = List of column names that have a 70%+ ratio for zero, lowvolatility values
    strong_ones_high_ratio_col = List of column names that have a 70%+ ratio for one, highvolatility values
    strong_ones_low_ratio_col = List of column names that have a 70%+ ratio for one, lowvolatility values
    '''
    mass_shooters = w.prepare_mass_shooters()
    binary_cols = []
    for col in mass_shooters.columns:
        if mass_shooters[col].nunique() == 2:
            binary_cols.append(col)
    binary_cols_passed_stats = []
    alpha = 0.05
    for col in binary_cols:
        contingency_table = pd.crosstab(mass_shooters.shooter_volatility, mass_shooters[col])
        stat, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        if p_value < alpha:
            binary_cols_passed_stats.append(col)
    strong_zeros_high_ratio_col = []
    strong_zeros_low_ratio_col = []
    strong_ones_high_ratio_col = []
    strong_ones_low_ratio_col = []
    for col in binary_cols_passed_stats:
        total_zeros = (mass_shooters[col] == 0).sum()
        total_ones = (mass_shooters[col] == 1).sum()
        total_zeros_high = ((mass_shooters[col] == 0) & (mass_shooters.shooter_volatility == 'High Volatility')).sum()
        total_zeros_low = ((mass_shooters[col] == 0) & (mass_shooters.shooter_volatility == 'Low Volatility')).sum()
        total_ones_high = ((mass_shooters[col] == 1) & (mass_shooters.shooter_volatility == 'High Volatility')).sum()
        total_ones_low = ((mass_shooters[col] == 1) & (mass_shooters.shooter_volatility == 'Low Volatility')).sum()
        ratio_zeros_high = total_zeros_high / total_zeros
        ratio_zeros_low = total_zeros_low / total_zeros
        ratio_ones_high = total_ones_high / total_ones
        ratio_ones_low = total_ones_low / total_ones
        if ratio_zeros_high >= 0.7:
            strong_zeros_high_ratio_col.append(col)
        elif ratio_zeros_low >= 0.7:
            strong_zeros_low_ratio_col.append(col)
        elif ratio_ones_high >= 0.7:
            strong_ones_high_ratio_col.append(col)
        elif ratio_ones_low >= 0.7:
            strong_ones_low_ratio_col.append(col)
    return strong_zeros_high_ratio_col, strong_zeros_low_ratio_col, strong_ones_high_ratio_col, strong_ones_low_ratio_col

# =======================================================================================================
# binary_list END
# binary_list TO agg_list
# agg_list START
# =======================================================================================================

def agg_list():
    '''
    Obtains the aggregate list that passed filters in order to be used in modeling...

    INPUT:
    NONE

    OUTPUT:
    agg_cols_passed_stats = List of column names that passed exploratory filters for significance
    '''
    mass_shooters = w.prepare_mass_shooters()
    agg_cols = [col for col in mass_shooters.columns if col.startswith('agg')]
    agg_cols_passed_stats = []
    alpha = 0.05
    for col in agg_cols:
        target_binary = np.where(mass_shooters.shooter_volatility == 'High Volatility', 1, 0)
        target_mean = sum(target_binary) / mass_shooters.shape[0]
        non_target_mean = mass_shooters[col].mean()
        stat, p = stats.ttest_ind_from_stats(mean1=target_mean, std1=1, nobs1=mass_shooters.shape[0],
                                mean2=non_target_mean, std2=1, nobs2=mass_shooters.shape[0],
                                equal_var=False)
        if p < alpha:
            agg_cols_passed_stats.append(col)
    return agg_cols_passed_stats

# =======================================================================================================
# agg_list END
# =======================================================================================================