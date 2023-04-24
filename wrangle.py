# =======================================================================================================
# Table of Contents START
# =======================================================================================================

'''
1. Orientation
2. Imports
3. acquire_mass_shooters
4. prepare_superstore
5. wrangle_superstore
6. split
7. scale
8. sample_dataframe
9. remove_outliers
'''

# =======================================================================================================
# Table of Contents END
# Table of Contents TO Orientation
# Orientation START
# =======================================================================================================

'''
The purpose of this file is to create functions for both the acquire & preparation phase of the data
science pipeline or also known as 'wrangling' the data...

Wrangling process is specific to the 'mass_shooters' from the excel data from the non-profit
organization 'The Violence Project'...
'''

# =======================================================================================================
# Orientation END
# Orientation TO Imports
# Imports START
# =======================================================================================================

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import os

# =======================================================================================================
# Imports END
# Imports TO acquire_mass_shooters
# acquire_mass_shooters START
# =======================================================================================================

def acquire_mass_shooters():
    '''
    Obtains the vanilla version of the mass_shooters dataframe

    INPUT:
    NONE

    OUTPUT:
    mass_shooters = pandas dataframe
    '''
    mass_shooters = pd.read_excel('mass_shooters.xlsx', sheet_name='Full Database', header=1)
    return mass_shooters

# =======================================================================================================
# acquire_mass_shooters END
# acquire_mass_shooters TO prepare_superstore
# prepare_superstore START
# =======================================================================================================

def prepare_superstore():
    '''
    Takes in the vanilla superstore dataframes and returns a cleaned version that is ready 
    for exploration and further analysis

    INPUT:
    NONE

    OUTPUT:
    new_superstore = pandas dataframe of the prepared superstore dataframe
    '''
    print('Template')

# =======================================================================================================
# prepare_superstore END
# prepare_superstore TO wrangle_superstore
# wrangle_superstore START
# =======================================================================================================

def wrangle_superstore():
    '''
    Function that acquires, prepares, and splits the superstore dataframe for use as well as 
    creating a csv.

    INPUT:
    NONE

    OUTPUT:
    .csv = ONLY IF FILE NONEXISTANT
    train = pandas dataframe of training set for superstore data
    validate = pandas dataframe of validation set for superstore data
    test = pandas dataframe of testing set for superstore data
    '''
    if os.path.exists('superstore.csv'):
        superstore = pd.read_csv('superstore.csv', index_col=0)
        train, validate, test = split(superstore)
        return train, validate, test
    else:
        superstore = prepare_superstore()
        superstore.to_csv('superstore.csv')
        train, validate, test = split(superstore)
        return train, validate, test
    
# =======================================================================================================
# wrangle_superstore END
# wrangle_superstore TO split
# split START
# =======================================================================================================

def split(df):
    '''
    Takes a dataframe and splits the data into a train, validate and test datasets
    '''
    train_val, test = train_test_split(df, train_size=0.8, random_state=1349)
    train, validate = train_test_split(train_val, train_size=0.7, random_state=1349)
    print(f"train.shape:{train.shape}\nvalidate.shape:{validate.shape}\ntest.shape:{test.shape}")
    return train, validate, test


# =======================================================================================================
# split END
# split TO scale
# scale START
# =======================================================================================================

def scale(train, validate, test, cols, scaler):
    '''
    Takes in a train, validate, test and returns the dataframes,
    but scaled using the 'StandardScaler()'
    '''
    original_train = train.copy()
    original_validate = validate.copy()
    original_test = test.copy()
    scale_cols = cols
    scaler = scaler
    scaler.fit(original_train[scale_cols])
    original_train[scale_cols] = scaler.transform(original_train[scale_cols])
    scaler.fit(original_validate[scale_cols])
    original_validate[scale_cols] = scaler.transform(original_validate[scale_cols])
    scaler.fit(original_test[scale_cols])
    original_test[scale_cols] = scaler.transform(original_test[scale_cols])
    new_train = original_train
    new_validate = original_validate
    new_test = original_test
    return new_train, new_validate, new_test

# =======================================================================================================
# scale END
# scale TO sample_dataframe
# sample_dataframe START
# =======================================================================================================

def sample_dataframe(train, validate, test):
    '''
    Takes train, validate, test dataframes and reduces the shape to no more than 1000 rows by taking
    the percentage of 1000/len(train) then applying that to train, validate, test dataframes.

    INPUT:
    train = Split dataframe for training
    validate = Split dataframe for validation
    test = Split dataframe for testing

    OUTPUT:
    train_sample = Reduced size of original split dataframe of no more than 1000 rows
    validate_sample = Reduced size of original split dataframe of no more than 1000 rows
    test_sample = Reduced size of original split dataframe of no more than 1000 rows
    '''
    ratio = 1000/len(train)
    train_samples = int(ratio * len(train))
    validate_samples = int(ratio * len(validate))
    test_samples = int(ratio * len(test))
    train_sample = train.sample(train_samples)
    validate_sample = validate.sample(validate_samples)
    test_sample = test.sample(test_samples)
    return train_sample, validate_sample, test_sample

# =======================================================================================================
# sample_dataframe END
# sample_dataframe TO remove_outliers
# remove_outliers START
# =======================================================================================================

def remove_outliers(df, col_list, k=1.5):
    '''
    remove outliers from a dataframe based on a list of columns using the tukey method
    returns a single dataframe with outliers removed
    '''
    col_qs = {}
    for col in col_list:
        col_qs[col] = q1, q3 = df[col].quantile([0.25, 0.75])
    for col in col_list:
        iqr = col_qs[col][0.75] - col_qs[col][0.25]
        lower_fence = col_qs[col][0.25] - (k*iqr)
        upper_fence = col_qs[col][0.75] + (k*iqr)
        df = df[(df[col] > lower_fence) & (df[col] < upper_fence)]
    return df

# =======================================================================================================
# remove_outliers END
# =======================================================================================================