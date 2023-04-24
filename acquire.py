# =======================================================================================================
# Table of Contents START
# =======================================================================================================

'''
1. Orientation
2. Imports
3. acquire_mass_shooters
'''

# =======================================================================================================
# Table of Contents END
# Table of Contents TO Orientation
# Orientation START
# =======================================================================================================

'''
The purpose of this file is to acquire the untouched (raw) data of the U.S. mass shooters...
'''

# =======================================================================================================
# Orientation END
# Orientation TO Imports
# Imports START
# =======================================================================================================

import numpy as np
import pandas as pd

# =======================================================================================================
# Imports END
# Imports TO acquire_mass_shooters
# acquire_mass_shooters START
# =======================================================================================================

def acquire_mass_shooters():
    '''
    Obtains the vanilla version of the mass_shooters.xlsx
    
    IMPORTANT: RAW DATA CANNOT BE GIVEN OUT FREELY THEREFORE YOU MUST REQUEST ACCESS TO
    THE DATABASE VIA VIOLENCE PROJECT

    INPUT:
    NONE

    OUTPUT:
    mass_shooters = pandas dataframe of mass shooters
    '''
    mass_shooters = pd.read_excel('mass_shooters.xlsx', sheet_name='Full Database', header=1)
    return mass_shooters

# =======================================================================================================
# acquire_store END
# =======================================================================================================