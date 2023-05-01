# =======================================================================================================
# Table of Contents START
# =======================================================================================================

'''
1. Orientation
2. Imports
3. visual1
4. visual2
5. visual3
6. visual4
7. visual5
8. visual6
9. stat1
10. stat2
11. stat3
12. baseline
13. models
14. models_best
15. acquire
16. prepare
17. wrangle
'''

# =======================================================================================================
# Table of Contents END
# Table of Contents TO Orientation
# Orientation START
# =======================================================================================================

'''
The purpose of this file is to create functions in order to expedite and maintain cleanliness
of the final_report.ipynb
'''

# =======================================================================================================
# Orientation END
# Orientation TO Imports
# Imports START
# =======================================================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from scipy import stats
from sklearn.tree import DecisionTreeClassifier as DTC
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.metrics import classification_report, accuracy_score, recall_score
import wrangle as w
import explore as e

# =======================================================================================================
# Imports END
# Imports TO visual1
# visual1 START
# =======================================================================================================

def visual1():
    '''
    Gets the 1st visual for the 'final_report.ipynb'...

    INPUT:
    NONE

    OUTPUT:
    Displays 1st visual
    '''
    mpl.style.use('bmh')
    full = w.prepare_mass_shooters()
    year_counts = full.year.value_counts().sort_index()
    plt.plot(year_counts.index, year_counts.values, label='Mass Shooter Incidents')
    sns.regplot(data=year_counts, x=year_counts.index, y=year_counts.values, scatter=False, ci=0, label='Trend Line')
    plt.title('Mass Shooter Incidents By Year')
    plt.xlabel('Year')
    plt.ylabel('Count of Mass Shootings')
    plt.legend()
    plt.show()

# =======================================================================================================
# visual1 END
# visual1 TO visual2
# visual2 START
# =======================================================================================================

def visual2():
    '''
    Gets the 2nd visual for the 'final_report.ipynb'...

    INPUT:
    NONE

    OUTPUT:
    Displays 2nd visual
    '''
    mpl.style.use('bmh')
    full = w.prepare_mass_shooters()
    removed_outlier = full[full.agg_casualties != 927]
    casualties_wo_outlier = removed_outlier.groupby('year')['agg_casualties'].mean()
    casualties_w_outlier = full.groupby('year')['agg_casualties'].mean()
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
    axs[0].plot(casualties_wo_outlier.index, casualties_wo_outlier.values, label='Annual Casualties')
    axs[0].set_title('Avg. Casualties By Year (Without Outlier)')
    axs[0].set_xlabel('Year')
    axs[0].set_ylabel('Avg. Casualties')
    sns.regplot(data=casualties_wo_outlier, x=casualties_wo_outlier.index, y=casualties_wo_outlier.values, scatter=False, ci=0, label='Trend Line', ax=axs[0])
    axs[0].legend()
    axs[1].plot(casualties_w_outlier.index, casualties_w_outlier.values, label='Annual Casualties')
    axs[1].set_title('Avg. Casualties By Year (With Outlier)')
    axs[1].set_xlabel('Year')
    axs[1].set_ylabel('Avg. Casualties')
    sns.regplot(data=casualties_w_outlier, x=casualties_w_outlier.index, y=casualties_w_outlier.values, scatter=False, ci=0, label='Trend Line', ax=axs[1])
    axs[1].legend()
    plt.subplots_adjust(wspace=0.3)
    plt.show()

# =======================================================================================================
# visual2 END
# visual2 TO visual3
# visual3 START
# =======================================================================================================

def visual3():
    '''
    Gets the 3rd visual for the 'final_report.ipynb'...

    INPUT:
    NONE

    OUTPUT:
    Displays 3rd visual
    '''
    mpl.style.use('ggplot')
    full = w.prepare_mass_shooters()
    sns.histplot(data=full, x='shooter_volatility')
    plt.title('Distribution of Shooter Volatility')
    plt.gca().set_xticklabels(['High Volatility (Casualties > 10)', 'Low Volatility (Casualties <= 10)'])
    plt.show()

# =======================================================================================================
# visual3 END
# visual3 TO visual4
# visual4 START
# =======================================================================================================

def visual4():
    '''
    Gets the 4th visual for the 'final_report.ipynb'...

    INPUT:
    NONE

    OUTPUT:
    Displays 4th visual
    '''
    mpl.style.use('bmh')
    full = w.prepare_mass_shooters()
    removed_outlier = full[full.agg_casualties != 927]
    removed_outlier['agg_crime'] = removed_outlier['agg_crime'] * 32
    sns.regplot(data=removed_outlier, x='agg_crime', y='agg_casualties', ci=0, line_kws={'color' : 'red'})
    plt.title('Shooter Crime History vs. Casualties')
    plt.xlabel('Number of Significant Crimes Convicted Out of 32 Types')
    plt.ylabel('Casualties')
    plt.show()

# =======================================================================================================
# visual4 END
# visual4 TO visual5
# visual5 START
# =======================================================================================================

def visual5():
    '''
    Gets the 5th visual for the 'final_report.ipynb'...

    INPUT:
    NONE

    OUTPUT:
    Displays 5th visual
    '''
    mpl.style.use('bmh')
    full = w.prepare_mass_shooters()
    removed_outlier = full[full.agg_casualties != 927]
    removed_outlier['agg_trauma'] = removed_outlier['agg_trauma'] * 20
    sns.regplot(data=removed_outlier, x='agg_trauma', y='agg_casualties', ci=0, line_kws={'color' : 'red'})
    plt.title('Shooter Trauma History vs. Casualties')
    plt.xlabel('Number of Significant Traumatic Events Out of 20 Types')
    plt.ylabel('Casualties')
    plt.show()

# =======================================================================================================
# visual5 END
# visual5 TO visual6
# visual6 START
# =======================================================================================================

def visual6():
    '''
    Gets the 6th visual for the 'final_report.ipynb'...

    INPUT:
    NONE

    OUTPUT:
    Displays 6th visual
    '''
    mpl.style.use('bmh')
    full = w.prepare_mass_shooters()
    removed_outlier = full[full.agg_casualties != 927]
    removed_outlier['agg_grand_total'] = removed_outlier['agg_grand_total'] * 109
    sns.regplot(data=removed_outlier, x='agg_grand_total', y='agg_casualties', ci=0, line_kws={'color' : 'red'})
    plt.title('Shooter Abnormalities vs. Casualties')
    plt.xlabel('Number of Abnormalities of 109 Types')
    plt.ylabel('Casualties')
    plt.show()

# =======================================================================================================
# visual6 END
# visual6 TO stat1
# stat1 START
# =======================================================================================================

def stat1():
    '''
    Gets the 1st statistic for the 4th visual for the 'final_report.ipynb'...

    INPUT:
    NONE

    OUTPUT:
    Displays 1st statistic for the 4th visual
    '''
    full = w.prepare_mass_shooters()
    removed_outlier = full[full.agg_casualties != 927]
    removed_outlier['agg_crime'] = removed_outlier['agg_crime'] * 32
    target_binary = np.where(removed_outlier.shooter_volatility == 'High Volatility', 1, 0)
    target_mean = sum(target_binary) / removed_outlier.shape[0]
    non_target_mean = removed_outlier.agg_crime.mean()
    stat, p = stats.ttest_ind_from_stats(mean1=target_mean, std1=1, nobs1=removed_outlier.shape[0],
                            mean2=non_target_mean, std2=1, nobs2=removed_outlier.shape[0],
                            equal_var=False)
    if p < 0.05:
        print(f'\033[32m========== REJECT NULL HYPOTHESIS! ==========\033[0m')
        print(f'\033[35mStatistic:\033[0m {stat:.4f}')
        print(f'\033[35mP-Value:\033[0m {p:.4f}')
    else:
        print(f'\033[31m========== ACCEPT NULL HYPOTHESIS! ==========\033[0m')
        print(f'\033[35mStatistic:\033[0m {stat:.4f}')
        print(f'\033[35mP-Value:\033[0m {p:.4f}')

# =======================================================================================================
# stat1 END
# stat1 TO stat2
# stat2 START
# =======================================================================================================

def stat2():
    '''
    Gets the 2nd statistic for the 5th visual for the 'final_report.ipynb'...

    INPUT:
    NONE

    OUTPUT:
    Displays 2nd statistic for the 5th visual
    '''
    full = w.prepare_mass_shooters()
    removed_outlier = full[full.agg_casualties != 927]
    removed_outlier['agg_trauma'] = removed_outlier['agg_trauma'] * 20
    target_binary = np.where(removed_outlier.shooter_volatility == 'High Volatility', 1, 0)
    target_mean = sum(target_binary) / removed_outlier.shape[0]
    non_target_mean = removed_outlier.agg_trauma.mean()
    stat, p = stats.ttest_ind_from_stats(mean1=target_mean, std1=1, nobs1=removed_outlier.shape[0],
                            mean2=non_target_mean, std2=1, nobs2=removed_outlier.shape[0],
                            equal_var=False)
    if p < 0.05:
        print(f'\033[32m========== REJECT NULL HYPOTHESIS! ==========\033[0m')
        print(f'\033[35mStatistic:\033[0m {stat:.4f}')
        print(f'\033[35mP-Value:\033[0m {p:.4f}')
    else:
        print(f'\033[31m========== ACCEPT NULL HYPOTHESIS! ==========\033[0m')
        print(f'\033[35mStatistic:\033[0m {stat:.4f}')
        print(f'\033[35mP-Value:\033[0m {p:.4f}')

# =======================================================================================================
# stat2 END
# stat2 TO stat3
# stat3 START
# =======================================================================================================

def stat3():
    '''
    Gets the 3rd statistic for the 6th visual for the 'final_report.ipynb'...

    INPUT:
    NONE

    OUTPUT:
    Displays 3rd statistic for the 6th visual
    '''
    full = w.prepare_mass_shooters()
    removed_outlier = full[full.agg_casualties != 927]
    removed_outlier['agg_grand_total'] = removed_outlier['agg_grand_total'] * 109
    target_binary = np.where(removed_outlier.shooter_volatility == 'High Volatility', 1, 0)
    target_mean = sum(target_binary) / removed_outlier.shape[0]
    non_target_mean = removed_outlier.agg_grand_total.mean()
    stat, p = stats.ttest_ind_from_stats(mean1=target_mean, std1=1, nobs1=removed_outlier.shape[0],
                            mean2=non_target_mean, std2=1, nobs2=removed_outlier.shape[0],
                            equal_var=False)
    if p < 0.05:
        print(f'\033[32m========== REJECT NULL HYPOTHESIS! ==========\033[0m')
        print(f'\033[35mStatistic:\033[0m {stat:.4f}')
        print(f'\033[35mP-Value:\033[0m {p:.4f}')
    else:
        print(f'\033[31m========== ACCEPT NULL HYPOTHESIS! ==========\033[0m')
        print(f'\033[35mStatistic:\033[0m {stat:.4f}')
        print(f'\033[35mP-Value:\033[0m {p:.4f}')

# =======================================================================================================
# stat3 END
# stat3 TO baseline
# baseline START
# =======================================================================================================

def baseline():
    '''
    Returns a pandas dataframe with the baseline model for the 'final_report.ipynb'...

    INPUT:
    NONE

    OUTPUT:
    baseline_model = pandas dataframe with only the baseline model
    '''
    train, validate, test = w.wrangle_mass_shooters()
    models_dict = {
    'model_name' : [],
    'model_type' : [],
    'model_descriptor' : [],
    'accuracy_train' : [],
    'accuracy_val' : [],
    'accuracy_diff' : [],
    'recall_variable' : [],
    'recall_train' : [],
    'recall_val' : [],
    'recall_diff' : []
    }
    baseline_train = round((train.shooter_volatility == train.shooter_volatility.mode()[0]).sum() / train.shape[0], 3)
    baseline_val = round((validate.shooter_volatility == validate.shooter_volatility.mode()[0]).sum() / validate.shape[0], 3)
    models_dict['model_name'].append('Baseline')
    models_dict['model_type'].append('Baseline')
    models_dict['model_descriptor'].append('Mode = Low Volatility')
    models_dict['accuracy_train'].append(baseline_train)
    models_dict['accuracy_val'].append(baseline_val)
    models_dict['accuracy_diff'].append(baseline_val - baseline_train)
    models_dict['recall_variable'].append('High Volatility')
    models_dict['recall_train'].append(0.000)
    models_dict['recall_val'].append(0.000)
    models_dict['recall_diff'].append(0.000)
    baseline_model = pd.DataFrame(models_dict)
    return baseline_model

# =======================================================================================================
# baseline END
# baseline TO models
# models START
# =======================================================================================================

def models():
    '''
    Returns a pandas dataframe with a sample of models created during the modeling process
    for the 'final_report.ipynb'...

    INPUT:
    NONE

    OUTPUT:
    models = pandas dataframe with 20 models for demonstration
    '''
    train, validate, test = w.wrangle_mass_shooters()
    models_dict = {
    'model_name' : [],
    'model_type' : [],
    'model_descriptor' : [],
    'accuracy_train' : [],
    'accuracy_val' : [],
    'accuracy_diff' : [],
    'recall_variable' : [],
    'recall_train' : [],
    'recall_val' : [],
    'recall_diff' : []
    }
    baseline_train = round((train.shooter_volatility == train.shooter_volatility.mode()[0]).sum() / train.shape[0], 3)
    baseline_val = round((validate.shooter_volatility == validate.shooter_volatility.mode()[0]).sum() / validate.shape[0], 3)
    models_dict['model_name'].append('Baseline')
    models_dict['model_type'].append('Baseline')
    models_dict['model_descriptor'].append('Mode = Low Volatility')
    models_dict['accuracy_train'].append(baseline_train)
    models_dict['accuracy_val'].append(baseline_val)
    models_dict['accuracy_diff'].append(baseline_val - baseline_train)
    models_dict['recall_variable'].append('High Volatility')
    models_dict['recall_train'].append(0.000)
    models_dict['recall_val'].append(0.000)
    models_dict['recall_diff'].append(0.000)
    zero_high, zero_low, one_high, one_low = e.binary_list()
    zero_all = zero_high + zero_low
    one_all = one_high + one_low
    high_only = zero_high + one_high
    low_only = zero_low + one_low
    all_binary = zero_all + one_all
    agg_list = e.agg_list()
    agg_list = [name for name in agg_list if name != 'agg_casualties']
    dictionary_list = {
    'zero_high' : zero_high,
    'zero_low' : zero_low,
    'one_high' : one_high,
    'one_low' : one_low,
    'zero_all' : zero_all,
    'one_all' : one_all,
    'high_only' : high_only,
    'low_only' : low_only,
    'all_binary' : all_binary,
    'agg_list' : agg_list
    }
    n = 0
    for list in dictionary_list:
        dtc = DTC(max_depth=3, random_state=1349, ccp_alpha=0.02)
        dtc.fit(train[dictionary_list[list]], train.shooter_volatility)
        train_preds = dtc.predict(train[dictionary_list[list]])
        val_preds = dtc.predict(validate[dictionary_list[list]])
        train_accuracy = round(accuracy_score(train.shooter_volatility, train_preds), 3)
        val_accuracy = round(accuracy_score(validate.shooter_volatility, val_preds), 3)
        accuracy_diff = val_accuracy - train_accuracy
        train_recall = round(recall_score(train.shooter_volatility, train_preds, pos_label='High Volatility'), 3)
        val_recall = round(recall_score(validate.shooter_volatility, val_preds, pos_label='High Volatility'), 3)
        recall_diff = val_recall - train_recall
        n += 1
        models_dict['model_name'].append(f'DTC{n}')
        models_dict['model_type'].append('Decision Tree Classifier')
        models_dict['model_descriptor'].append(list)
        models_dict['accuracy_train'].append(train_accuracy)
        models_dict['accuracy_val'].append(val_accuracy)
        models_dict['accuracy_diff'].append(accuracy_diff)
        models_dict['recall_variable'].append('High Volatility')
        models_dict['recall_train'].append(train_recall)
        models_dict['recall_val'].append(val_recall)
        models_dict['recall_diff'].append(recall_diff)
    n = 0
    for list in dictionary_list:
        rfc = RFC(max_depth=3, random_state=1349, ccp_alpha=0.02)
        rfc.fit(train[dictionary_list[list]], train.shooter_volatility)
        train_preds = rfc.predict(train[dictionary_list[list]])
        val_preds = rfc.predict(validate[dictionary_list[list]])
        train_accuracy = round(accuracy_score(train.shooter_volatility, train_preds), 3)
        val_accuracy = round(accuracy_score(validate.shooter_volatility, val_preds), 3)
        accuracy_diff = val_accuracy - train_accuracy
        train_recall = round(recall_score(train.shooter_volatility, train_preds, pos_label='High Volatility'), 3)
        val_recall = round(recall_score(validate.shooter_volatility, val_preds, pos_label='High Volatility'), 3)
        recall_diff = val_recall - train_recall
        n += 1
        models_dict['model_name'].append(f'RFC{n}')
        models_dict['model_type'].append('Random Forest Classifier')
        models_dict['model_descriptor'].append(list)
        models_dict['accuracy_train'].append(train_accuracy)
        models_dict['accuracy_val'].append(val_accuracy)
        models_dict['accuracy_diff'].append(accuracy_diff)
        models_dict['recall_variable'].append('High Volatility')
        models_dict['recall_train'].append(train_recall)
        models_dict['recall_val'].append(val_recall)
        models_dict['recall_diff'].append(recall_diff)
    models_dict['model_name'].append('DTC_aggregates2')
    models_dict['model_type'].append('Decision Tree Classifier')
    models_dict['model_descriptor'].append('[agg_stress, agg_trauma, agg_health]')
    models_dict['accuracy_train'].append(0.893)
    models_dict['accuracy_val'].append(0.632)
    models_dict['accuracy_diff'].append(-0.261)
    models_dict['recall_variable'].append('High Volatility')
    models_dict['recall_train'].append(0.812)
    models_dict['recall_val'].append(0.429)
    models_dict['recall_diff'].append(-0.383)
    models_dict['model_name'].append('DTC_aggregates3')
    models_dict['model_type'].append('Decision Tree Classifier')
    models_dict['model_descriptor'].append('[agg_stress, agg_trauma]')
    models_dict['accuracy_train'].append(0.779)
    models_dict['accuracy_val'].append(0.763)
    models_dict['accuracy_diff'].append(-0.016)
    models_dict['recall_variable'].append('High Volatility')
    models_dict['recall_train'].append(0.542)
    models_dict['recall_val'].append(0.5)
    models_dict['recall_diff'].append(-0.042)
    models = pd.DataFrame(models_dict)
    return models

# =======================================================================================================
# models END
# models TO models_best
# models_best START
# =======================================================================================================

def models_best():
    '''
    Returns a pandas dataframe with the best model created during the modeling process for the 
    'final_report.ipynb'...

    INPUT:
    NONE

    OUTPUT:
    top_model = pandas dataframe with top model for demonstration
    '''
    best_models_dict = {
    'model_name' : ['Baseline', 'DTC_aggregates2', 'DTC_aggregates3'],
    'model_type' : ['Baseline', 'Decision Tree Classifier', 'Decision Tree Classifier'],
    'model_descriptor' : ['mode == "Low Volatility"', '[agg_stress, agg_trauma, agg_health]', '[agg_stress, agg_trauma]'],
    'accuracy' : [0.632, 0.579, 0.737],
    'recall_pos_label' : ['High Volatility', 'High Volatility', 'High Volatility'],
    'recall' : [0.000, 0.714, 0.571]
    }
    top_model = pd.DataFrame(best_models_dict)
    return top_model

# =======================================================================================================
# models_best END
# models_best TO acquire
# acquire START
# =======================================================================================================

def acquire():
    '''
    Obtains the vanilla mass_shooters dataframe from the 'wrangle.py' file

    INPUT:
    NONE

    OUTPUT:
    mass_shooters = pandas dataframe
    '''
    mass_shooters = w.acquire_mass_shooters()
    return mass_shooters

# =======================================================================================================
# acquire END
# acquire TO prepare
# prepare START
# =======================================================================================================

def prepare():
    '''
    Obtains the prepared mass_shooters dataframe from the 'wrangle.py' file

    INPUT:
    NONE

    OUTPUT:
    prepped_mass_shooters = pandas dataframe
    '''
    prepped_mass_shooters = w.prepare_mass_shooters()
    return prepped_mass_shooters

# =======================================================================================================
# prepare END
# prepare TO wrangle
# wrangle START
# =======================================================================================================

def wrangle():
    '''
    Obtains the splitted mass_shooters dataframe from the 'wrangle.py' file

    INPUT:
    NONE

    OUTPUT:
    train = pandas dataframe with 70% of prepared mass_shooters dataframe
    validate = pandas dataframe with 20% of prepared mass_shooters dataframe
    test = pandas dataframe with 10% of prepared mass_shooters dataframe
    '''
    train, validate, test = w.wrangle_mass_shooters()
    return train, validate, test

# =======================================================================================================
# wrangle END
# =======================================================================================================