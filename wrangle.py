# =======================================================================================================
# Table of Contents START
# =======================================================================================================

'''
1. Orientation
2. Imports
3. acquire_mass_shooters
4. prepare_mass_shooters
5. wrangle_mass_shooters
6. split
7. scale
8. sample_dataframe
9. remove_outliers
10. drop_nullpct
11. check_nulls
12. unaggregated_mass_shooters
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
# acquire_mass_shooters TO prepare_mass_shooters
# prepare_mass_shooters START
# =======================================================================================================

def prepare_mass_shooters():
    '''
    Takes in the vanilla mass_shooters dataframe and returns a cleaned version that is ready 
    for exploration and further analysis

    INPUT:
    NONE

    OUTPUT:
    .csv = ONLY IF FILE NONEXISTANT
    prepped_mass_shooters = pandas dataframe of the prepared mass_shooters dataframe
    '''
    if os.path.exists('mass_shooters.csv'):
        prepped_mass_shooters = pd.read_csv('mass_shooters.csv', index_col=0)
        return prepped_mass_shooters
    else:
        mass_shooters = acquire_mass_shooters()
        mass_shooters = mass_shooters.drop(mass_shooters[mass_shooters['Case #'] == '145, 146'].index)
        drop_perpetratorname_cols = [
            'Shooter Last Name',
            'Shooter First Name'
            ]
        drop_date_cols = [
            'Full Date'
            ]
        drop_location_cols = [
            'Street Number',
            'Street Name',
            'Zip Code',
            'Latitude',
            'Longitude',
            'State Code',
            'Region',
            'Metro/Micro Statistical Area Type',
            'Location',
            'Insider or Outsider',
            'Workplace Shooting',
            'Multiple Locations',
            'Other Location',
            'Armed Person on Scene',
            'Specify Armed Person'
            ]
        drop_victim_cols = [
            'Family Member Victim',
            'Romantic Partner Victim',
            'Kidnapping or Hostage Situation'
            ]
        drop_weapons_cols = [
            'Total Firearms Brought to the Scene',
            'Other Weapons or Gear',
            'Specify Other Weapons or Gear',
            ]
        drop_resolutionofcase_cols = [
            'On-Scene Outcome',
            'Who Killed Shooter On Scene',
            'Attempt to Flee',
            'Insanity Defense',
            'Criminal Sentence'
            ]
        mass_shooters = mass_shooters.drop(columns=drop_perpetratorname_cols)
        mass_shooters = mass_shooters.drop(columns=drop_date_cols)
        mass_shooters = mass_shooters.drop(columns=drop_location_cols)
        mass_shooters = mass_shooters.drop(columns=drop_victim_cols)
        mass_shooters = mass_shooters.drop(columns=drop_weapons_cols)
        mass_shooters = mass_shooters.drop(columns=drop_resolutionofcase_cols)
        mass_shooters, drop_null_pct_dict = drop_nullpct(mass_shooters, 0.20)
        has_nulls = check_nulls(mass_shooters)
        mass_shooters['Signs of Crisis Expanded'] = mass_shooters['Signs of Crisis Expanded'].fillna('None')
        for col in has_nulls:
            mass_shooters[col] = mass_shooters[col].fillna(mass_shooters[col].mode()[0])
        for col in mass_shooters.columns:
            if mass_shooters[col].dtype == 'object':
                if mass_shooters[col].apply(lambda x: isinstance(x, str) and x.isspace()).any():
                    mass_shooters[col].replace(r'^\s*$', np.nan, regex=True, inplace=True)
                    mass_shooters[col].fillna(mass_shooters[col].mode()[0], inplace=True)
        mass_shooters['Case #'] = mass_shooters['Case #'].astype(int)
        mass_shooters['Day'] = np.where(mass_shooters['Day'] == '19-20', 19, mass_shooters['Day'])
        mass_shooters['Day'] = mass_shooters['Day'].astype(int)
        mass_shooters['Race'] = np.where(mass_shooters['Race'] == 'Moroccan', 6, mass_shooters['Race'])
        mass_shooters['Race'] = np.where(mass_shooters['Race'] == 'Bosnian', 7, mass_shooters['Race'])
        mass_shooters['Race'] = mass_shooters['Race'].astype(int)
        mass_shooters['Criminal Record'] = np.where(mass_shooters['Criminal Record'] == '1`', 1, mass_shooters['Criminal Record'])
        mass_shooters['Criminal Record'] = mass_shooters['Criminal Record'].astype(int)
        mass_shooters['Gender'] = np.where(mass_shooters['Gender'] == 3.0, 0, mass_shooters['Gender'])
        mass_shooters['Children'] = np.where(mass_shooters['Children'] == 5.0, 0, mass_shooters['Children'])
        mass_shooters['History of Domestic Abuse'] = np.where(mass_shooters['History of Domestic Abuse'] == 3.0, 2, mass_shooters['History of Domestic Abuse'])
        for col in mass_shooters.select_dtypes(include=float).columns.to_list():
            mass_shooters[col] = mass_shooters[col].astype(int)
        mass_shooters['adult_trauma_no_evidence'] = np.where(mass_shooters['Adult Trauma'].astype(str).str.contains('0'), 1, 0)
        mass_shooters['adult_trauma_death_of_parent'] = np.where(mass_shooters['Adult Trauma'].astype(str).str.contains('1'), 1, 0)
        mass_shooters['adult_trauma_death_or_loss_of_child'] = np.where(mass_shooters['Adult Trauma'].astype(str).str.contains('2'), 1, 0)
        mass_shooters['adult_trauma_death_of_family_member_causing_significant_distress'] = np.where(mass_shooters['Adult Trauma'].astype(str).str.contains('3'), 1, 0)
        mass_shooters['adult_trauma_from_war'] = np.where(mass_shooters['Adult Trauma'].astype(str).str.contains('4'), 1, 0)
        mass_shooters['adult_trauma_accident'] = np.where(mass_shooters['Adult Trauma'].astype(str).str.contains('5'), 1, 0)
        mass_shooters['adult_trauma_other'] = np.where(mass_shooters['Adult Trauma'].astype(str).str.contains('6'), 1, 0)
        mass_shooters['voluntary_or_mandatory_counseling_na'] = np.where(mass_shooters['Voluntary or Mandatory Counseling'].astype(str).str.contains('0'), 1, 0)
        mass_shooters['voluntary_or_mandatory_counseling_voluntary'] = np.where(mass_shooters['Voluntary or Mandatory Counseling'].astype(str).str.contains('1'), 1, 0)
        mass_shooters['voluntary_or_mandatory_counseling_involuntary'] = np.where(mass_shooters['Voluntary or Mandatory Counseling'].astype(str).str.contains('2'), 1, 0)
        mass_shooters['mental_illness_no_evidence'] = np.where(mass_shooters['Mental Illness'].astype(str).str.contains('0'), 1, 0)
        mass_shooters['mental_illness_mood_disorder'] = np.where(mass_shooters['Mental Illness'].astype(str).str.contains('1'), 1, 0)
        mass_shooters['mental_illness_thought_disorder'] = np.where(mass_shooters['Mental Illness'].astype(str).str.contains('2'), 1, 0)
        mass_shooters['mental_illness_other_psychiatric_disorder'] = np.where(mass_shooters['Mental Illness'].astype(str).str.contains('3'), 1, 0)
        mass_shooters['mental_illness_indication_but_no_diagnosis'] = np.where(mass_shooters['Mental Illness'].astype(str).str.contains('4'), 1, 0)
        mass_shooters['known_family_mental_health_history_no_evidence'] = np.where(mass_shooters['Known Family Mental Health History'].astype(str).str.contains('0'), 1, 0)
        mass_shooters['known_family_mental_health_history_parents'] = np.where(mass_shooters['Known Family Mental Health History'].astype(str).str.contains('1'), 1, 0)
        mass_shooters['known_family_mental_health_history_other_relative'] = np.where(mass_shooters['Known Family Mental Health History'].astype(str).str.contains('2'), 1, 0)
        mass_shooters['part_i_crimes_no_evidence'] = np.where(mass_shooters['Part I Crimes'].astype(str).str.contains('0'), 1, 0)
        mass_shooters['part_i_crimes_homicide'] = np.where(mass_shooters['Part I Crimes'].astype(str).str.contains('1'), 1, 0)
        mass_shooters['part_i_crimes_forcible_rape'] = np.where(mass_shooters['Part I Crimes'].astype(str).str.contains('2'), 1, 0)
        mass_shooters['part_i_crimes_robbery'] = np.where(mass_shooters['Part I Crimes'].astype(str).str.contains('3'), 1, 0)
        mass_shooters['part_i_crimes_aggravated_assault'] = np.where(mass_shooters['Part I Crimes'].astype(str).str.contains('4'), 1, 0)
        mass_shooters['part_i_crimes_burglary'] = np.where(mass_shooters['Part I Crimes'].astype(str).str.contains('5'), 1, 0)
        mass_shooters['part_i_crimes_larceny_theft'] = np.where(mass_shooters['Part I Crimes'].astype(str).str.contains('6'), 1, 0)
        mass_shooters['part_i_crimes_motor_vehicle_theft'] = np.where(mass_shooters['Part I Crimes'].astype(str).str.contains('7'), 1, 0)
        mass_shooters['part_i_crimes_arson'] = np.where(mass_shooters['Part I Crimes'].astype(str).str.contains('8'), 1, 0)
        mass_shooters['part_ii_crimes_no_evidence'] = np.where(mass_shooters['Part II Crimes'].astype(str).str.contains('0'), 1, 0)
        mass_shooters['part_ii_crimes_simple_assault'] = np.where(mass_shooters['Part II Crimes'].astype(str).str.contains('1'), 1, 0)
        mass_shooters['part_ii_crimes_fraud_forgery_embezzlement'] = np.where(mass_shooters['Part II Crimes'].astype(str).str.contains('2'), 1, 0)
        mass_shooters['part_ii_crimes_stolen_property'] = np.where(mass_shooters['Part II Crimes'].astype(str).str.contains('3'), 1, 0)
        mass_shooters['part_ii_crimes_vandalism'] = np.where(mass_shooters['Part II Crimes'].astype(str).str.contains('4'), 1, 0)
        mass_shooters['part_ii_crimes_weapons_offenses'] = np.where(mass_shooters['Part II Crimes'].astype(str).str.contains('5'), 1, 0)
        mass_shooters['part_ii_crimes_prostitution'] = np.where(mass_shooters['Part II Crimes'].astype(str).str.contains('6'), 1, 0)
        mass_shooters['part_ii_crimes_drugs'] = np.where(mass_shooters['Part II Crimes'].astype(str).str.contains('7'), 1, 0)
        mass_shooters['part_ii_crimes_dui'] = np.where(mass_shooters['Part II Crimes'].astype(str).str.contains('8'), 1, 0)
        mass_shooters['part_ii_crimes_other'] = np.where(mass_shooters['Part II Crimes'].astype(str).str.contains('9'), 1, 0)
        mass_shooters['domestic_abuse_specified_na'] = np.where(mass_shooters['Domestic Abuse Specified'].astype(str).str.contains('0'), 1, 0)
        mass_shooters['domestic_abuse_specified_non_sexual'] = np.where(mass_shooters['Domestic Abuse Specified'].astype(str).str.contains('1'), 1, 0)
        mass_shooters['domestic_abuse_specified_sexual_violence'] = np.where(mass_shooters['Domestic Abuse Specified'].astype(str).str.contains('2'), 1, 0)
        mass_shooters['domestic_abuse_specified_threats_coercive_control'] = np.where(mass_shooters['Domestic Abuse Specified'].astype(str).str.contains('3'), 1, 0)
        mass_shooters['domestic_abuse_specified_threats_with_deadly_weapon'] = np.where(mass_shooters['Domestic Abuse Specified'].astype(str).str.contains('4'), 1, 0)
        mass_shooters['recent_or_ongoing_stressor_no_evidence'] = np.where(mass_shooters['Recent or Ongoing Stressor'].astype(str).str.contains('0'), 1, 0)
        mass_shooters['recent_or_ongoing_stressor_recent_breakup'] = np.where(mass_shooters['Recent or Ongoing Stressor'].astype(str).str.contains('1'), 1, 0)
        mass_shooters['recent_or_ongoing_stressor_employment'] = np.where(mass_shooters['Recent or Ongoing Stressor'].astype(str).str.contains('2'), 1, 0)
        mass_shooters['recent_or_ongoing_stressor_economic_stressor'] = np.where(mass_shooters['Recent or Ongoing Stressor'].astype(str).str.contains('3'), 1, 0)
        mass_shooters['recent_or_ongoing_stressor_family_issue'] = np.where(mass_shooters['Recent or Ongoing Stressor'].astype(str).str.contains('4'), 1, 0)
        mass_shooters['recent_or_ongoing_stressor_legal_issue'] = np.where(mass_shooters['Recent or Ongoing Stressor'].astype(str).str.contains('5'), 1, 0)
        mass_shooters['recent_or_ongoing_stressor_other'] = np.where(mass_shooters['Recent or Ongoing Stressor'].astype(str).str.contains('6'), 1, 0)
        mass_shooters['substance_use_no_evidence'] = np.where(mass_shooters['Substance Use'].astype(str).str.contains('0'), 1, 0)
        mass_shooters['substance_use_alcohol'] = np.where(mass_shooters['Substance Use'].astype(str).str.contains('1'), 1, 0)
        mass_shooters['substance_use_marijuana'] = np.where(mass_shooters['Substance Use'].astype(str).str.contains('2'), 1, 0)
        mass_shooters['substance_use_other_drugs'] = np.where(mass_shooters['Substance Use'].astype(str).str.contains('3'), 1, 0)
        mass_shooters['known_prejudices_no_evidence'] = np.where(mass_shooters['Known Prejudices\xa0'].astype(str).str.contains('0'), 1, 0)
        mass_shooters['known_prejudices_racism'] = np.where(mass_shooters['Known Prejudices\xa0'].astype(str).str.contains('1'), 1, 0)
        mass_shooters['known_prejudices_misogyny'] = np.where(mass_shooters['Known Prejudices\xa0'].astype(str).str.contains('2'), 1, 0)
        mass_shooters['known_prejudices_homophobia'] = np.where(mass_shooters['Known Prejudices\xa0'].astype(str).str.contains('3'), 1, 0)
        mass_shooters['known_prejudices_religious_hatred'] = np.where(mass_shooters['Known Prejudices\xa0'].astype(str).str.contains('4'), 1, 0)
        mass_shooters['urban'] = np.where(mass_shooters['Urban/Suburban/Rural'] == 0, 1, 0)
        mass_shooters['suburban'] = np.where(mass_shooters['Urban/Suburban/Rural'] == 1, 1, 0)
        mass_shooters['rural'] = np.where(mass_shooters['Urban/Suburban/Rural'] == 2, 1, 0)
        mass_shooters['race_white'] = np.where(mass_shooters['Race'] == 0, 1, 0)
        mass_shooters['race_black'] = np.where(mass_shooters['Race'] == 1, 1, 0)
        mass_shooters['race_hispanic'] = np.where(mass_shooters['Race'] == 2, 1, 0)
        mass_shooters['race_asian'] = np.where(mass_shooters['Race'] == 3, 1, 0)
        mass_shooters['race_middle_eastern'] = np.where(mass_shooters['Race'] == 4, 1, 0)
        mass_shooters['race_native_american'] = np.where(mass_shooters['Race'] == 5, 1, 0)
        mass_shooters['race_moroccan'] = np.where(mass_shooters['Race'] == 6, 1, 0)
        mass_shooters['race_bosnian'] = np.where(mass_shooters['Race'] == 7, 1, 0)
        mass_shooters['relationship_status_single'] = np.where(mass_shooters['Relationship Status'] == 0, 1, 0)
        mass_shooters['relationship_status_boyfriend_girlfriend'] = np.where(mass_shooters['Relationship Status'] == 1, 1, 0)
        mass_shooters['relationship_status_married'] = np.where(mass_shooters['Relationship Status'] == 2, 1, 0)
        mass_shooters['relationship_status_divorce_separated'] = np.where(mass_shooters['Relationship Status'] == 3, 1, 0)
        mass_shooters['employment_type_blue_collar'] = np.where(mass_shooters['Employment Type\xa0'] == 0, 1, 0)
        mass_shooters['employment_type_white_collar'] = np.where(mass_shooters['Employment Type\xa0'] == 1, 1, 0)
        mass_shooters['employment_type_in_between'] = np.where(mass_shooters['Employment Type\xa0'] == 2, 1, 0)
        mass_shooters['military_service_no'] = np.where(mass_shooters['Military Service'] == 0, 1, 0)
        mass_shooters['military_service_yes'] = np.where(mass_shooters['Military Service'] == 1, 1, 0)
        mass_shooters['military_service_joined_but_did_not_complete_training'] = np.where(mass_shooters['Military Service'] == 2, 1, 0)
        mass_shooters['community_involvement_no_evidence'] = np.where(mass_shooters['Community Involvement'] == 0, 1, 0)
        mass_shooters['community_involvement_somewhat'] = np.where(mass_shooters['Community Involvement'] == 1, 1, 0)
        mass_shooters['community_involvement_heavily_involved'] = np.where(mass_shooters['Community Involvement'] == 2, 1, 0)
        mass_shooters['community_involvement_formerly_involved'] = np.where(mass_shooters['Community Involvement'] == 3, 1, 0)
        mass_shooters['highest_level_of_justice_system_involvement_na'] = np.where(mass_shooters['Highest Level of Justice System Involvement'] == 0, 1, 0)
        mass_shooters['highest_level_of_justice_system_involvement_suspected'] = np.where(mass_shooters['Highest Level of Justice System Involvement'] == 1, 1, 0)
        mass_shooters['highest_level_of_justice_system_involvement_arrested'] = np.where(mass_shooters['Highest Level of Justice System Involvement'] == 2, 1, 0)
        mass_shooters['highest_level_of_justice_system_involvement_charged'] = np.where(mass_shooters['Highest Level of Justice System Involvement'] == 3, 1, 0)
        mass_shooters['highest_level_of_justice_system_involvement_convicted'] = np.where(mass_shooters['Highest Level of Justice System Involvement'] == 4, 1, 0)
        mass_shooters['history_of_physical_altercations_na'] = np.where(mass_shooters['History of Physical Altercations'] == 0, 1, 0)
        mass_shooters['history_of_physical_altercations_yes'] = np.where(mass_shooters['History of Physical Altercations'] == 1, 1, 0)
        mass_shooters['history_of_physical_altercations_attacked_inanimate_objects_during_arguments'] = np.where(mass_shooters['History of Physical Altercations'] == 2, 1, 0)
        mass_shooters['history_of_domestic_abuse_na'] = np.where(mass_shooters['History of Domestic Abuse'] == 0, 1, 0)
        mass_shooters['history_of_domestic_abuse_abused_romantic_partner'] = np.where(mass_shooters['History of Domestic Abuse'] == 1, 1, 0)
        mass_shooters['history_of_domestic_abuse_abused_other_family'] = np.where(mass_shooters['History of Domestic Abuse'] == 2, 1, 0)
        mass_shooters['known_hate_group_or_chat_room_affiliation_no_evidence'] = np.where(mass_shooters['Known Hate Group or Chat Room Affiliation'] == 0, 1, 0)
        mass_shooters['known_hate_group_or_chat_room_affiliation_hate_group'] = np.where(mass_shooters['Known Hate Group or Chat Room Affiliation'] == 1, 1, 0)
        mass_shooters['known_hate_group_or_chat_room_affiliation_other_radical_group'] = np.where(mass_shooters['Known Hate Group or Chat Room Affiliation'] == 2, 1, 0)
        mass_shooters['known_hate_group_or_chat_room_affiliation_inspired_by_hate_group_but_no_connection'] = np.where(mass_shooters['Known Hate Group or Chat Room Affiliation'] == 3, 1, 0)
        mass_shooters['known_hate_group_or_chat_room_affiliation_website_or_chat'] = np.where(mass_shooters['Known Hate Group or Chat Room Affiliation'] == 4, 1, 0)
        mass_shooters['violent_video_games_no_evidence'] = np.where(mass_shooters['Violent Video Games'] == 0, 1, 0)
        mass_shooters['violent_video_games_yes'] = np.where(mass_shooters['Violent Video Games'] == 1, 1, 0)
        mass_shooters['violent_video_games_played_unspecified'] = np.where(mass_shooters['Violent Video Games'] == 2, 1, 0)
        mass_shooters['violent_video_games_na'] = np.where(mass_shooters['Violent Video Games'] == 3, 1, 0)
        mass_shooters['timeline_of_signs_of_crisis_days_before'] = np.where(mass_shooters['Timeline of Signs of Crisis'] == 0, 1, 0)
        mass_shooters['timeline_of_signs_of_crisis_weeks_before'] = np.where(mass_shooters['Timeline of Signs of Crisis'] == 1, 1, 0)
        mass_shooters['timeline_of_signs_of_crisis_months_before'] = np.where(mass_shooters['Timeline of Signs of Crisis'] == 2, 1, 0)
        mass_shooters['timeline_of_signs_of_crisis_years_before'] = np.where(mass_shooters['Timeline of Signs of Crisis'] == 3, 1, 0)
        mass_shooters['suicidality_no_evidence'] = np.where(mass_shooters['Suicidality'] == 0, 1, 0)
        mass_shooters['suicidality_yes_prior_to_shooting'] = np.where(mass_shooters['Suicidality'] == 1, 1, 0)
        mass_shooters['suicidality_intended_to_die_in_shooting_no_prior'] = np.where(mass_shooters['Suicidality'] == 2, 1, 0)
        mass_shooters['voluntary_or_involuntary_hospitalization_na'] = np.where(mass_shooters['Voluntary or Involuntary Hospitalization'] == 0, 1, 0)
        mass_shooters['voluntary_or_involuntary_hospitalization_voluntary'] = np.where(mass_shooters['Voluntary or Involuntary Hospitalization'] == 1, 1, 0)
        mass_shooters['voluntary_or_involuntary_hospitalization_involuntary'] = np.where(mass_shooters['Voluntary or Involuntary Hospitalization'] == 2, 1, 0)
        mass_shooters['motive_racism_xenophobia_no_evidence'] = np.where(mass_shooters['Motive: Racism/Xenophobia'] == 0, 1, 0)
        mass_shooters['motive_racism_xenophobia_targeting_color'] = np.where(mass_shooters['Motive: Racism/Xenophobia'] == 1, 1, 0)
        mass_shooters['motive_racism_xenophobia_targeting_white'] = np.where(mass_shooters['Motive: Racism/Xenophobia'] == 2, 1, 0)
        mass_shooters['motive_religious_hate_no_evidence'] = np.where(mass_shooters['Motive: Religious Hate'] == 0, 1, 0)
        mass_shooters['motive_religious_hate_antisemitism'] = np.where(mass_shooters['Motive: Religious Hate'] == 1, 1, 0)
        mass_shooters['motive_religious_hate_islamophobia'] = np.where(mass_shooters['Motive: Religious Hate'] == 2, 1, 0)
        mass_shooters['motive_religious_hate_angry_with_christianity_or_god'] = np.where(mass_shooters['Motive: Religious Hate'] == 3, 1, 0)
        mass_shooters['motive_other_no_evidence'] = np.where(mass_shooters['Motive: Other\xa0'] == 0, 1, 0)
        mass_shooters['motive_other_yes'] = np.where(mass_shooters['Motive: Other\xa0'] == 1, 1, 0)
        mass_shooters['motive_other_generalized_anger'] = np.where(mass_shooters['Motive: Other\xa0'] == 2, 1, 0)
        mass_shooters['role_of_psychosis_in_the_shooting_no_evidence'] = np.where(mass_shooters['Role of Psychosis in the Shooting'] == 0, 1, 0)
        mass_shooters['role_of_psychosis_in_the_shooting_minor_role'] = np.where(mass_shooters['Role of Psychosis in the Shooting'] == 1, 1, 0)
        mass_shooters['role_of_psychosis_in_the_shooting_moderate_role'] = np.where(mass_shooters['Role of Psychosis in the Shooting'] == 2, 1, 0)
        mass_shooters['role_of_psychosis_in_the_shooting_major_role'] = np.where(mass_shooters['Role of Psychosis in the Shooting'] == 3, 1, 0)
        mass_shooters['social_media_use_no_evidence'] = np.where(mass_shooters['Social Media Use\xa0'] == 0, 1, 0)
        mass_shooters['social_media_use_yes'] = np.where(mass_shooters['Social Media Use\xa0'] == 1, 1, 0)
        mass_shooters['social_media_use_na'] = np.where(mass_shooters['Social Media Use\xa0'] == 2, 1, 0)
        mass_shooters['pop_culture_connection_no_evidence'] = np.where(mass_shooters['Pop Culture Connection'] == 0, 1, 0)
        mass_shooters['pop_culture_connection_explicit_reference'] = np.where(mass_shooters['Pop Culture Connection'] == 1, 1, 0)
        mass_shooters['pop_culture_connection_tangential_reference'] = np.where(mass_shooters['Pop Culture Connection'] == 2, 1, 0)
        mass_shooters['firearm_proficiency_no_experience'] = np.where(mass_shooters['Firearm Proficiency'] == 0, 1, 0)
        mass_shooters['firearm_proficiency_some_experience'] = np.where(mass_shooters['Firearm Proficiency'] == 1, 1, 0)
        mass_shooters['firearm_proficiency_more_experienced'] = np.where(mass_shooters['Firearm Proficiency'] == 2, 1, 0)
        mass_shooters['firearm_proficiency_very_experienced'] = np.where(mass_shooters['Firearm Proficiency'] == 3, 1, 0)
        signs_of_crisis_cols = [
            'Signs of Being in Crisis',
            'Inability to Perform Daily Tasks',
            'Notably Depressed Mood',
            'Unusually Calm or Happy',
            'Rapid Mood Swings',
            'Increased Agitation',
            'Abusive Behavior',
            'Isolation',
            'Losing Touch with Reality',
            'Paranoia'
            ]
        motivation_hatred_cols = [
            'Motive: Misogyny',
            'Motive: Homophobia'
            ]
        motivation_personal_cols = [
            'Motive: Employment Issue',
            'Motive: Economic Issue',
            'Motive: Legal Issue',
            'Motive: Relationship Issue',
            'Motive: Interpersonal Conflict\xa0',
            'Motive: Fame-Seeking'
            ]
        social_cols = [
            'Leakage\xa0',
            'Interest in Past Mass Violence',
            'Relationship with Other Shooting(s)',
            'Planning',
            'Performance'
            ]
        trauma_cols = [
            'Bullied',
            'Raised by Single Parent',
            'Parental Divorce / Separation',
            'Parental Death in Childhood',
            'Parental Suicide',
            'Childhood Trauma',
            'Physically Abused',
            'Sexually Abused',
            'Emotionally Abused',
            'Neglected',
            'Mother Violent Treatment',
            'Parental Substance Abuse',
            'Parent Criminal Record',
            'Family Member Incarcerated',
            'adult_trauma_death_of_parent',
            'adult_trauma_death_or_loss_of_child',
            'adult_trauma_death_of_family_member_causing_significant_distress',
            'adult_trauma_from_war',
            'adult_trauma_accident',
            'adult_trauma_other'
            ]
        health_cols = [
            'Prior Hospitalization',
            'Prior Counseling',
            'Psychiatric Medication',
            'FASD (Fetal Alcohol Spectrum Disorder)',
            'Autism Spectrum',
            'Health Issues',
            'Head Injury / Possible TBI',
            'voluntary_or_mandatory_counseling_voluntary',
            'voluntary_or_mandatory_counseling_involuntary',
            'mental_illness_mood_disorder',
            'mental_illness_thought_disorder',
            'mental_illness_other_psychiatric_disorder',
            'mental_illness_indication_but_no_diagnosis'
            ]
        background_cols = [
            'Immigrant',
            'Sexual Orientation',
            'known_family_mental_health_history_parents',
            'known_family_mental_health_history_other_relative'
            ]
        crime_cols = [
            'Known to Police or FBI',
            'Criminal Record',
            'History of Animal Abuse',
            'History of Sexual Offenses',
            'Gang Affiliation',
            'Terror Group Affiliation',
            'Bully',
            'part_i_crimes_homicide',
            'part_i_crimes_forcible_rape',
            'part_i_crimes_robbery',
            'part_i_crimes_aggravated_assault',
            'part_i_crimes_burglary',
            'part_i_crimes_larceny_theft',
            'part_i_crimes_motor_vehicle_theft',
            'part_i_crimes_arson',
            'part_ii_crimes_simple_assault',
            'part_ii_crimes_fraud_forgery_embezzlement',
            'part_ii_crimes_stolen_property',
            'part_ii_crimes_vandalism',
            'part_ii_crimes_weapons_offenses',
            'part_ii_crimes_prostitution',
            'part_ii_crimes_drugs',
            'part_ii_crimes_dui',
            'part_ii_crimes_other',
            'domestic_abuse_specified_non_sexual',
            'domestic_abuse_specified_sexual_violence',
            'domestic_abuse_specified_threats_coercive_control',
            'domestic_abuse_specified_threats_with_deadly_weapon',
            'highest_level_of_justice_system_involvement_suspected',
            'highest_level_of_justice_system_involvement_arrested',
            'highest_level_of_justice_system_involvement_charged',
            'highest_level_of_justice_system_involvement_convicted'
            ]
        stress_cols = [
            'Employment Status',
            'recent_or_ongoing_stressor_recent_breakup',
            'recent_or_ongoing_stressor_employment',
            'recent_or_ongoing_stressor_economic_stressor',
            'recent_or_ongoing_stressor_family_issue',
            'recent_or_ongoing_stressor_legal_issue',
            'recent_or_ongoing_stressor_other',
            'history_of_physical_altercations_yes',
            'history_of_physical_altercations_attacked_inanimate_objects_during_arguments'
            ]
        substance_abuse_cols = [
            'substance_use_alcohol',
            'substance_use_marijuana',
            'substance_use_other_drugs'
            ]
        prejudice_cols = [
            'known_prejudices_racism',
            'known_prejudices_misogyny',
            'known_prejudices_homophobia',
            'known_prejudices_religious_hatred'
            ]
        grand_total_cols = [
            'Signs of Being in Crisis',
            'Inability to Perform Daily Tasks',
            'Notably Depressed Mood',
            'Unusually Calm or Happy',
            'Rapid Mood Swings',
            'Increased Agitation',
            'Abusive Behavior',
            'Isolation',
            'Losing Touch with Reality',
            'Paranoia',
            'Motive: Misogyny',
            'Motive: Homophobia',
            'Motive: Employment Issue',
            'Motive: Economic Issue',
            'Motive: Legal Issue',
            'Motive: Relationship Issue',
            'Motive: Interpersonal Conflict\xa0',
            'Motive: Fame-Seeking',
            'Leakage\xa0',
            'Interest in Past Mass Violence',
            'Relationship with Other Shooting(s)',
            'Planning',
            'Performance',
            'Bullied',
            'Raised by Single Parent',
            'Parental Divorce / Separation',
            'Parental Death in Childhood',
            'Parental Suicide',
            'Childhood Trauma',
            'Physically Abused',
            'Sexually Abused',
            'Emotionally Abused',
            'Neglected',
            'Mother Violent Treatment',
            'Parental Substance Abuse',
            'Parent Criminal Record',
            'Family Member Incarcerated',
            'adult_trauma_death_of_parent',
            'adult_trauma_death_or_loss_of_child',
            'adult_trauma_death_of_family_member_causing_significant_distress',
            'adult_trauma_from_war',
            'adult_trauma_accident',
            'adult_trauma_other',
            'Prior Hospitalization',
            'Prior Counseling',
            'Psychiatric Medication',
            'FASD (Fetal Alcohol Spectrum Disorder)',
            'Autism Spectrum',
            'Health Issues',
            'Head Injury / Possible TBI',
            'voluntary_or_mandatory_counseling_voluntary',
            'voluntary_or_mandatory_counseling_involuntary',
            'mental_illness_mood_disorder',
            'mental_illness_thought_disorder',
            'mental_illness_other_psychiatric_disorder',
            'mental_illness_indication_but_no_diagnosis',
            'Interest in Firearms',
            'Immigrant',
            'Sexual Orientation',
            'known_family_mental_health_history_parents',
            'known_family_mental_health_history_other_relative',
            'Known to Police or FBI',
            'Criminal Record',
            'History of Animal Abuse',
            'History of Sexual Offenses',
            'Gang Affiliation',
            'Terror Group Affiliation',
            'Bully',
            'part_i_crimes_homicide',
            'part_i_crimes_forcible_rape',
            'part_i_crimes_robbery',
            'part_i_crimes_aggravated_assault',
            'part_i_crimes_burglary',
            'part_i_crimes_larceny_theft',
            'part_i_crimes_motor_vehicle_theft',
            'part_i_crimes_arson',
            'part_ii_crimes_simple_assault',
            'part_ii_crimes_fraud_forgery_embezzlement',
            'part_ii_crimes_stolen_property',
            'part_ii_crimes_vandalism',
            'part_ii_crimes_weapons_offenses',
            'part_ii_crimes_prostitution',
            'part_ii_crimes_drugs',
            'part_ii_crimes_dui',
            'part_ii_crimes_other',
            'domestic_abuse_specified_non_sexual',
            'domestic_abuse_specified_sexual_violence',
            'domestic_abuse_specified_threats_coercive_control',
            'domestic_abuse_specified_threats_with_deadly_weapon',
            'highest_level_of_justice_system_involvement_suspected',
            'highest_level_of_justice_system_involvement_arrested',
            'highest_level_of_justice_system_involvement_charged',
            'highest_level_of_justice_system_involvement_convicted',
            'Employment Status',
            'recent_or_ongoing_stressor_recent_breakup',
            'recent_or_ongoing_stressor_employment',
            'recent_or_ongoing_stressor_economic_stressor',
            'recent_or_ongoing_stressor_family_issue',
            'recent_or_ongoing_stressor_legal_issue',
            'recent_or_ongoing_stressor_other',
            'history_of_physical_altercations_yes',
            'history_of_physical_altercations_attacked_inanimate_objects_during_arguments',
            'substance_use_alcohol',
            'substance_use_marijuana',
            'substance_use_other_drugs',
            'known_prejudices_racism',
            'known_prejudices_misogyny',
            'known_prejudices_homophobia',
            'known_prejudices_religious_hatred'
            ]
        casualties_col = [
            'Number Killed',
            'Number Injured'
        ]
        mass_shooters['agg_signs_of_crisis'] = mass_shooters[signs_of_crisis_cols].mean(axis=1).round(3)
        mass_shooters['agg_motivation_hatred'] = mass_shooters[motivation_hatred_cols].mean(axis=1).round(3)
        mass_shooters['agg_motivation_personal'] = mass_shooters[motivation_personal_cols].mean(axis=1).round(3)
        mass_shooters['agg_social'] = mass_shooters[social_cols].mean(axis=1).round(3)
        mass_shooters['agg_trauma'] = mass_shooters[trauma_cols].mean(axis=1).round(3)
        mass_shooters['agg_health'] = mass_shooters[health_cols].mean(axis=1).round(3)
        mass_shooters['agg_background'] = mass_shooters[background_cols].mean(axis=1).round(3)
        mass_shooters['agg_crime'] = mass_shooters[crime_cols].mean(axis=1).round(3)
        mass_shooters['agg_stress'] = mass_shooters[stress_cols].mean(axis=1).round(3)
        mass_shooters['agg_substance_abuse'] = mass_shooters[substance_abuse_cols].mean(axis=1).round(3)
        mass_shooters['agg_prejudice'] = mass_shooters[prejudice_cols].mean(axis=1).round(3)
        mass_shooters['agg_grand_total'] = mass_shooters[grand_total_cols].mean(axis=1).round(3)
        mass_shooters['agg_casualties'] = mass_shooters[casualties_col].sum(axis=1)
        mass_shooters.columns = mass_shooters.columns.str.replace('\xa0', '')
        mass_shooters.columns = mass_shooters.columns.str.replace('(', '')
        mass_shooters.columns = mass_shooters.columns.str.replace(')', '')
        mass_shooters.columns = mass_shooters.columns.str.replace('/', '')
        mass_shooters.columns = mass_shooters.columns.str.replace(':', '')
        mass_shooters.columns = mass_shooters.columns.str.replace('\s+', '_', regex=True)
        mass_shooters.columns = mass_shooters.columns.str.replace('#', 'id')
        mass_shooters.columns = mass_shooters.columns.str.lower()
        mass_shooters['shooter_volatility'] = np.where(mass_shooters.agg_casualties > 10, 'High Volatility', 'Low Volatility')
        prepped_mass_shooters = mass_shooters
        prepped_mass_shooters.to_csv('mass_shooters.csv')
        return prepped_mass_shooters

# =======================================================================================================
# prepare_mass_shooters END
# prepare_mass_shooters TO wrangle_mass_shooters
# wrangle_mass_shooters START
# =======================================================================================================

def wrangle_mass_shooters():
    '''
    Function that acquires, prepares, and splits the mass_shooters dataframe for use as well as 
    creating a csv.

    INPUT:
    NONE

    OUTPUT:
    .csv = ONLY IF FILE NONEXISTANT
    train = pandas dataframe of training set for mass_shooter data
    validate = pandas dataframe of validation set for mass_shooter data
    test = pandas dataframe of testing set for mass_shooter data
    '''
    if os.path.exists('mass_shooters.csv'):
        mass_shooters = pd.read_csv('mass_shooters.csv', index_col=0)
        train, validate, test = split(mass_shooters, stratify='shooter_volatility')
        return train, validate, test
    else:
        mass_shooters = prepare_mass_shooters()
        mass_shooters.to_csv('mass_shooters.csv')
        train, validate, test = split(mass_shooters, stratify='shooter_volatility')
        return train, validate, test
    
# =======================================================================================================
# wrangle_mass_shooters END
# wrangle_mass_shooters TO split
# split START
# =======================================================================================================

def split(df, stratify=None):
    '''
    Takes a dataframe and splits the data into a train, validate and test datasets

    INPUT:
    df = pandas dataframe to be split into
    stratify = Splits data with specific columns in consideration

    OUTPUT:
    train = pandas dataframe with 70% of original dataframe
    validate = pandas dataframe with 20% of original dataframe
    test = pandas dataframe with 10% of original dataframe
    '''
    train_val, test = train_test_split(df, train_size=0.9, random_state=1349, stratify=df[stratify])
    train, validate = train_test_split(train_val, train_size=0.778, random_state=1349, stratify=train_val[stratify])
    return train, validate, test


# =======================================================================================================
# split END
# split TO scale
# scale START
# =======================================================================================================

def scale(train, validate, test, cols, scaler):
    '''
    Takes in a train, validate, test dataframe and returns the dataframes scaled with the scaler
    of your choice

    INPUT:
    train = pandas dataframe that is meant for training your machine learning model
    validate = pandas dataframe that is meant for validating your machine learning model
    test = pandas dataframe that is meant for testing your machine learning model
    cols = List of column names that you want to be scaled
    scaler = Scaler that you want to scale columns with like 'MinMaxScaler()', 'StandardScaler()', etc.

    OUTPUT:
    new_train = pandas dataframe of scaled version of inputted train dataframe
    new_validate = pandas dataframe of scaled version of inputted validate dataframe
    new_test = pandas dataframe of scaled version of inputted test dataframe
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
    Remove outliers from a dataframe based on a list of columns using the tukey method and then
    returns a single dataframe with the outliers removed

    INPUT:
    df = pandas dataframe
    col_list = List of columns that you want outliers removed
    k = Defines range for fences, default/normal is 1.5

    OUTPUT:
    df = pandas dataframe with outliers removed
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
# remove_outliers TO drop_nullpct
# drop_nullpct START
# =======================================================================================================

def drop_nullpct(df, percent_cutoff):
    '''
    Takes in a dataframe and a percent_cutoff of nulls to drop a column on
    and returns the new dataframe and a dictionary of dropped columns and their pct...
    
    INPUT:
    df = pandas dataframe
    percent_cutoff = Null percent cutoff amount
    
    OUTPUT:
    new_df = pandas dataframe with dropped columns
    drop_null_pct_dict = dict of column names dropped and pcts
    '''
    drop_null_pct_dict = {
        'column_name' : [],
        'percent_null' : []
    }
    for col in df:
        pct = df[col].isna().sum() / df.shape[0]
        if pct > 0.20:
            df = df.drop(columns=col)
            drop_null_pct_dict['column_name'].append(col)
            drop_null_pct_dict['percent_null'].append(pct)
    new_df = df
    return new_df, drop_null_pct_dict

# =======================================================================================================
# drop_nullpct END
# drop_nullpct TO check_nulls
# check_nulls START
# =======================================================================================================

def check_nulls(df):
    '''
    Takes a dataframe and returns a list of columns that has at least one null value
    
    INPUT:
    df = pandas dataframe
    
    OUTPUT:
    has_nulls = List of column names with at least one null
    '''
    has_nulls = []
    for col in df:
        nulls = df[col].isna().sum()
        if nulls > 0:
            has_nulls.append(col)
    return has_nulls

# =======================================================================================================
# check_nulls END
# check_nulls TO unaggregated_mass_shooters
# unaggregated_mass_shooters START
# =======================================================================================================

def unaggregated_mass_shooters():
    '''
    THIS IS FOR POST-EXPLORATORY PURPOSES AND NOT THE INITAL AS SHOWN IN THE PROJECT
    Takes the vanilla dataframe and performs necessary preparatory functions WITHOUT the aggregation
    creation and column name editing

    INPUT:
    NONE

    OUTPUT:
    unaggregated_mass_shooters = Pandas dataframe with ONLY necessary data preparation
    '''
    mass_shooters = acquire_mass_shooters()
    mass_shooters = mass_shooters.drop(mass_shooters[mass_shooters['Case #'] == '145, 146'].index)
    drop_perpetratorname_cols = [
        'Shooter Last Name',
        'Shooter First Name'
        ]
    drop_date_cols = [
        'Full Date'
        ]
    drop_location_cols = [
        'Street Number',
        'Street Name',
        'Zip Code',
        'Latitude',
        'Longitude',
        'State Code',
        'Region',
        'Metro/Micro Statistical Area Type',
        'Location',
        'Insider or Outsider',
        'Workplace Shooting',
        'Multiple Locations',
        'Other Location',
        'Armed Person on Scene',
        'Specify Armed Person'
        ]
    drop_victim_cols = [
        'Family Member Victim',
        'Romantic Partner Victim',
        'Kidnapping or Hostage Situation'
        ]
    drop_weapons_cols = [
        'Total Firearms Brought to the Scene',
        'Other Weapons or Gear',
        'Specify Other Weapons or Gear',
        ]
    drop_resolutionofcase_cols = [
        'On-Scene Outcome',
        'Who Killed Shooter On Scene',
        'Attempt to Flee',
        'Insanity Defense',
        'Criminal Sentence'
        ]
    mass_shooters = mass_shooters.drop(columns=drop_perpetratorname_cols)
    mass_shooters = mass_shooters.drop(columns=drop_date_cols)
    mass_shooters = mass_shooters.drop(columns=drop_location_cols)
    mass_shooters = mass_shooters.drop(columns=drop_victim_cols)
    mass_shooters = mass_shooters.drop(columns=drop_weapons_cols)
    mass_shooters = mass_shooters.drop(columns=drop_resolutionofcase_cols)
    mass_shooters, drop_null_pct_dict = drop_nullpct(mass_shooters, 0.20)
    has_nulls = check_nulls(mass_shooters)
    mass_shooters['Signs of Crisis Expanded'] = mass_shooters['Signs of Crisis Expanded'].fillna('None')
    for col in has_nulls:
        mass_shooters[col] = mass_shooters[col].fillna(mass_shooters[col].mode()[0])
    for col in mass_shooters.columns:
        if mass_shooters[col].dtype == 'object':
            if mass_shooters[col].apply(lambda x: isinstance(x, str) and x.isspace()).any():
                mass_shooters[col].replace(r'^\s*$', np.nan, regex=True, inplace=True)
                mass_shooters[col].fillna(mass_shooters[col].mode()[0], inplace=True)
    mass_shooters['Case #'] = mass_shooters['Case #'].astype(int)
    mass_shooters['Day'] = np.where(mass_shooters['Day'] == '19-20', 19, mass_shooters['Day'])
    mass_shooters['Day'] = mass_shooters['Day'].astype(int)
    mass_shooters['Race'] = np.where(mass_shooters['Race'] == 'Moroccan', 6, mass_shooters['Race'])
    mass_shooters['Race'] = np.where(mass_shooters['Race'] == 'Bosnian', 7, mass_shooters['Race'])
    mass_shooters['Race'] = mass_shooters['Race'].astype(int)
    mass_shooters['Criminal Record'] = np.where(mass_shooters['Criminal Record'] == '1`', 1, mass_shooters['Criminal Record'])
    mass_shooters['Criminal Record'] = mass_shooters['Criminal Record'].astype(int)
    mass_shooters['Gender'] = np.where(mass_shooters['Gender'] == 3.0, 0, mass_shooters['Gender'])
    mass_shooters['Children'] = np.where(mass_shooters['Children'] == 5.0, 0, mass_shooters['Children'])
    mass_shooters['History of Domestic Abuse'] = np.where(mass_shooters['History of Domestic Abuse'] == 3.0, 2, mass_shooters['History of Domestic Abuse'])
    for col in mass_shooters.select_dtypes(include=float).columns.to_list():
        mass_shooters[col] = mass_shooters[col].astype(int)
    mass_shooters['adult_trauma_no_evidence'] = np.where(mass_shooters['Adult Trauma'].astype(str).str.contains('0'), 1, 0)
    mass_shooters['adult_trauma_death_of_parent'] = np.where(mass_shooters['Adult Trauma'].astype(str).str.contains('1'), 1, 0)
    mass_shooters['adult_trauma_death_or_loss_of_child'] = np.where(mass_shooters['Adult Trauma'].astype(str).str.contains('2'), 1, 0)
    mass_shooters['adult_trauma_death_of_family_member_causing_significant_distress'] = np.where(mass_shooters['Adult Trauma'].astype(str).str.contains('3'), 1, 0)
    mass_shooters['adult_trauma_from_war'] = np.where(mass_shooters['Adult Trauma'].astype(str).str.contains('4'), 1, 0)
    mass_shooters['adult_trauma_accident'] = np.where(mass_shooters['Adult Trauma'].astype(str).str.contains('5'), 1, 0)
    mass_shooters['adult_trauma_other'] = np.where(mass_shooters['Adult Trauma'].astype(str).str.contains('6'), 1, 0)
    mass_shooters['voluntary_or_mandatory_counseling_na'] = np.where(mass_shooters['Voluntary or Mandatory Counseling'].astype(str).str.contains('0'), 1, 0)
    mass_shooters['voluntary_or_mandatory_counseling_voluntary'] = np.where(mass_shooters['Voluntary or Mandatory Counseling'].astype(str).str.contains('1'), 1, 0)
    mass_shooters['voluntary_or_mandatory_counseling_involuntary'] = np.where(mass_shooters['Voluntary or Mandatory Counseling'].astype(str).str.contains('2'), 1, 0)
    mass_shooters['mental_illness_no_evidence'] = np.where(mass_shooters['Mental Illness'].astype(str).str.contains('0'), 1, 0)
    mass_shooters['mental_illness_mood_disorder'] = np.where(mass_shooters['Mental Illness'].astype(str).str.contains('1'), 1, 0)
    mass_shooters['mental_illness_thought_disorder'] = np.where(mass_shooters['Mental Illness'].astype(str).str.contains('2'), 1, 0)
    mass_shooters['mental_illness_other_psychiatric_disorder'] = np.where(mass_shooters['Mental Illness'].astype(str).str.contains('3'), 1, 0)
    mass_shooters['mental_illness_indication_but_no_diagnosis'] = np.where(mass_shooters['Mental Illness'].astype(str).str.contains('4'), 1, 0)
    mass_shooters['known_family_mental_health_history_no_evidence'] = np.where(mass_shooters['Known Family Mental Health History'].astype(str).str.contains('0'), 1, 0)
    mass_shooters['known_family_mental_health_history_parents'] = np.where(mass_shooters['Known Family Mental Health History'].astype(str).str.contains('1'), 1, 0)
    mass_shooters['known_family_mental_health_history_other_relative'] = np.where(mass_shooters['Known Family Mental Health History'].astype(str).str.contains('2'), 1, 0)
    mass_shooters['part_i_crimes_no_evidence'] = np.where(mass_shooters['Part I Crimes'].astype(str).str.contains('0'), 1, 0)
    mass_shooters['part_i_crimes_homicide'] = np.where(mass_shooters['Part I Crimes'].astype(str).str.contains('1'), 1, 0)
    mass_shooters['part_i_crimes_forcible_rape'] = np.where(mass_shooters['Part I Crimes'].astype(str).str.contains('2'), 1, 0)
    mass_shooters['part_i_crimes_robbery'] = np.where(mass_shooters['Part I Crimes'].astype(str).str.contains('3'), 1, 0)
    mass_shooters['part_i_crimes_aggravated_assault'] = np.where(mass_shooters['Part I Crimes'].astype(str).str.contains('4'), 1, 0)
    mass_shooters['part_i_crimes_burglary'] = np.where(mass_shooters['Part I Crimes'].astype(str).str.contains('5'), 1, 0)
    mass_shooters['part_i_crimes_larceny_theft'] = np.where(mass_shooters['Part I Crimes'].astype(str).str.contains('6'), 1, 0)
    mass_shooters['part_i_crimes_motor_vehicle_theft'] = np.where(mass_shooters['Part I Crimes'].astype(str).str.contains('7'), 1, 0)
    mass_shooters['part_i_crimes_arson'] = np.where(mass_shooters['Part I Crimes'].astype(str).str.contains('8'), 1, 0)
    mass_shooters['part_ii_crimes_no_evidence'] = np.where(mass_shooters['Part II Crimes'].astype(str).str.contains('0'), 1, 0)
    mass_shooters['part_ii_crimes_simple_assault'] = np.where(mass_shooters['Part II Crimes'].astype(str).str.contains('1'), 1, 0)
    mass_shooters['part_ii_crimes_fraud_forgery_embezzlement'] = np.where(mass_shooters['Part II Crimes'].astype(str).str.contains('2'), 1, 0)
    mass_shooters['part_ii_crimes_stolen_property'] = np.where(mass_shooters['Part II Crimes'].astype(str).str.contains('3'), 1, 0)
    mass_shooters['part_ii_crimes_vandalism'] = np.where(mass_shooters['Part II Crimes'].astype(str).str.contains('4'), 1, 0)
    mass_shooters['part_ii_crimes_weapons_offenses'] = np.where(mass_shooters['Part II Crimes'].astype(str).str.contains('5'), 1, 0)
    mass_shooters['part_ii_crimes_prostitution'] = np.where(mass_shooters['Part II Crimes'].astype(str).str.contains('6'), 1, 0)
    mass_shooters['part_ii_crimes_drugs'] = np.where(mass_shooters['Part II Crimes'].astype(str).str.contains('7'), 1, 0)
    mass_shooters['part_ii_crimes_dui'] = np.where(mass_shooters['Part II Crimes'].astype(str).str.contains('8'), 1, 0)
    mass_shooters['part_ii_crimes_other'] = np.where(mass_shooters['Part II Crimes'].astype(str).str.contains('9'), 1, 0)
    mass_shooters['domestic_abuse_specified_na'] = np.where(mass_shooters['Domestic Abuse Specified'].astype(str).str.contains('0'), 1, 0)
    mass_shooters['domestic_abuse_specified_non_sexual'] = np.where(mass_shooters['Domestic Abuse Specified'].astype(str).str.contains('1'), 1, 0)
    mass_shooters['domestic_abuse_specified_sexual_violence'] = np.where(mass_shooters['Domestic Abuse Specified'].astype(str).str.contains('2'), 1, 0)
    mass_shooters['domestic_abuse_specified_threats_coercive_control'] = np.where(mass_shooters['Domestic Abuse Specified'].astype(str).str.contains('3'), 1, 0)
    mass_shooters['domestic_abuse_specified_threats_with_deadly_weapon'] = np.where(mass_shooters['Domestic Abuse Specified'].astype(str).str.contains('4'), 1, 0)
    mass_shooters['recent_or_ongoing_stressor_no_evidence'] = np.where(mass_shooters['Recent or Ongoing Stressor'].astype(str).str.contains('0'), 1, 0)
    mass_shooters['recent_or_ongoing_stressor_recent_breakup'] = np.where(mass_shooters['Recent or Ongoing Stressor'].astype(str).str.contains('1'), 1, 0)
    mass_shooters['recent_or_ongoing_stressor_employment'] = np.where(mass_shooters['Recent or Ongoing Stressor'].astype(str).str.contains('2'), 1, 0)
    mass_shooters['recent_or_ongoing_stressor_economic_stressor'] = np.where(mass_shooters['Recent or Ongoing Stressor'].astype(str).str.contains('3'), 1, 0)
    mass_shooters['recent_or_ongoing_stressor_family_issue'] = np.where(mass_shooters['Recent or Ongoing Stressor'].astype(str).str.contains('4'), 1, 0)
    mass_shooters['recent_or_ongoing_stressor_legal_issue'] = np.where(mass_shooters['Recent or Ongoing Stressor'].astype(str).str.contains('5'), 1, 0)
    mass_shooters['recent_or_ongoing_stressor_other'] = np.where(mass_shooters['Recent or Ongoing Stressor'].astype(str).str.contains('6'), 1, 0)
    mass_shooters['substance_use_no_evidence'] = np.where(mass_shooters['Substance Use'].astype(str).str.contains('0'), 1, 0)
    mass_shooters['substance_use_alcohol'] = np.where(mass_shooters['Substance Use'].astype(str).str.contains('1'), 1, 0)
    mass_shooters['substance_use_marijuana'] = np.where(mass_shooters['Substance Use'].astype(str).str.contains('2'), 1, 0)
    mass_shooters['substance_use_other_drugs'] = np.where(mass_shooters['Substance Use'].astype(str).str.contains('3'), 1, 0)
    mass_shooters['known_prejudices_no_evidence'] = np.where(mass_shooters['Known Prejudices\xa0'].astype(str).str.contains('0'), 1, 0)
    mass_shooters['known_prejudices_racism'] = np.where(mass_shooters['Known Prejudices\xa0'].astype(str).str.contains('1'), 1, 0)
    mass_shooters['known_prejudices_misogyny'] = np.where(mass_shooters['Known Prejudices\xa0'].astype(str).str.contains('2'), 1, 0)
    mass_shooters['known_prejudices_homophobia'] = np.where(mass_shooters['Known Prejudices\xa0'].astype(str).str.contains('3'), 1, 0)
    mass_shooters['known_prejudices_religious_hatred'] = np.where(mass_shooters['Known Prejudices\xa0'].astype(str).str.contains('4'), 1, 0)
    mass_shooters['urban'] = np.where(mass_shooters['Urban/Suburban/Rural'] == 0, 1, 0)
    mass_shooters['suburban'] = np.where(mass_shooters['Urban/Suburban/Rural'] == 1, 1, 0)
    mass_shooters['rural'] = np.where(mass_shooters['Urban/Suburban/Rural'] == 2, 1, 0)
    mass_shooters['race_white'] = np.where(mass_shooters['Race'] == 0, 1, 0)
    mass_shooters['race_black'] = np.where(mass_shooters['Race'] == 1, 1, 0)
    mass_shooters['race_hispanic'] = np.where(mass_shooters['Race'] == 2, 1, 0)
    mass_shooters['race_asian'] = np.where(mass_shooters['Race'] == 3, 1, 0)
    mass_shooters['race_middle_eastern'] = np.where(mass_shooters['Race'] == 4, 1, 0)
    mass_shooters['race_native_american'] = np.where(mass_shooters['Race'] == 5, 1, 0)
    mass_shooters['race_moroccan'] = np.where(mass_shooters['Race'] == 6, 1, 0)
    mass_shooters['race_bosnian'] = np.where(mass_shooters['Race'] == 7, 1, 0)
    mass_shooters['relationship_status_single'] = np.where(mass_shooters['Relationship Status'] == 0, 1, 0)
    mass_shooters['relationship_status_boyfriend_girlfriend'] = np.where(mass_shooters['Relationship Status'] == 1, 1, 0)
    mass_shooters['relationship_status_married'] = np.where(mass_shooters['Relationship Status'] == 2, 1, 0)
    mass_shooters['relationship_status_divorce_separated'] = np.where(mass_shooters['Relationship Status'] == 3, 1, 0)
    mass_shooters['employment_type_blue_collar'] = np.where(mass_shooters['Employment Type\xa0'] == 0, 1, 0)
    mass_shooters['employment_type_white_collar'] = np.where(mass_shooters['Employment Type\xa0'] == 1, 1, 0)
    mass_shooters['employment_type_in_between'] = np.where(mass_shooters['Employment Type\xa0'] == 2, 1, 0)
    mass_shooters['military_service_no'] = np.where(mass_shooters['Military Service'] == 0, 1, 0)
    mass_shooters['military_service_yes'] = np.where(mass_shooters['Military Service'] == 1, 1, 0)
    mass_shooters['military_service_joined_but_did_not_complete_training'] = np.where(mass_shooters['Military Service'] == 2, 1, 0)
    mass_shooters['community_involvement_no_evidence'] = np.where(mass_shooters['Community Involvement'] == 0, 1, 0)
    mass_shooters['community_involvement_somewhat'] = np.where(mass_shooters['Community Involvement'] == 1, 1, 0)
    mass_shooters['community_involvement_heavily_involved'] = np.where(mass_shooters['Community Involvement'] == 2, 1, 0)
    mass_shooters['community_involvement_formerly_involved'] = np.where(mass_shooters['Community Involvement'] == 3, 1, 0)
    mass_shooters['highest_level_of_justice_system_involvement_na'] = np.where(mass_shooters['Highest Level of Justice System Involvement'] == 0, 1, 0)
    mass_shooters['highest_level_of_justice_system_involvement_suspected'] = np.where(mass_shooters['Highest Level of Justice System Involvement'] == 1, 1, 0)
    mass_shooters['highest_level_of_justice_system_involvement_arrested'] = np.where(mass_shooters['Highest Level of Justice System Involvement'] == 2, 1, 0)
    mass_shooters['highest_level_of_justice_system_involvement_charged'] = np.where(mass_shooters['Highest Level of Justice System Involvement'] == 3, 1, 0)
    mass_shooters['highest_level_of_justice_system_involvement_convicted'] = np.where(mass_shooters['Highest Level of Justice System Involvement'] == 4, 1, 0)
    mass_shooters['history_of_physical_altercations_na'] = np.where(mass_shooters['History of Physical Altercations'] == 0, 1, 0)
    mass_shooters['history_of_physical_altercations_yes'] = np.where(mass_shooters['History of Physical Altercations'] == 1, 1, 0)
    mass_shooters['history_of_physical_altercations_attacked_inanimate_objects_during_arguments'] = np.where(mass_shooters['History of Physical Altercations'] == 2, 1, 0)
    mass_shooters['history_of_domestic_abuse_na'] = np.where(mass_shooters['History of Domestic Abuse'] == 0, 1, 0)
    mass_shooters['history_of_domestic_abuse_abused_romantic_partner'] = np.where(mass_shooters['History of Domestic Abuse'] == 1, 1, 0)
    mass_shooters['history_of_domestic_abuse_abused_other_family'] = np.where(mass_shooters['History of Domestic Abuse'] == 2, 1, 0)
    mass_shooters['known_hate_group_or_chat_room_affiliation_no_evidence'] = np.where(mass_shooters['Known Hate Group or Chat Room Affiliation'] == 0, 1, 0)
    mass_shooters['known_hate_group_or_chat_room_affiliation_hate_group'] = np.where(mass_shooters['Known Hate Group or Chat Room Affiliation'] == 1, 1, 0)
    mass_shooters['known_hate_group_or_chat_room_affiliation_other_radical_group'] = np.where(mass_shooters['Known Hate Group or Chat Room Affiliation'] == 2, 1, 0)
    mass_shooters['known_hate_group_or_chat_room_affiliation_inspired_by_hate_group_but_no_connection'] = np.where(mass_shooters['Known Hate Group or Chat Room Affiliation'] == 3, 1, 0)
    mass_shooters['known_hate_group_or_chat_room_affiliation_website_or_chat'] = np.where(mass_shooters['Known Hate Group or Chat Room Affiliation'] == 4, 1, 0)
    mass_shooters['violent_video_games_no_evidence'] = np.where(mass_shooters['Violent Video Games'] == 0, 1, 0)
    mass_shooters['violent_video_games_yes'] = np.where(mass_shooters['Violent Video Games'] == 1, 1, 0)
    mass_shooters['violent_video_games_played_unspecified'] = np.where(mass_shooters['Violent Video Games'] == 2, 1, 0)
    mass_shooters['violent_video_games_na'] = np.where(mass_shooters['Violent Video Games'] == 3, 1, 0)
    mass_shooters['timeline_of_signs_of_crisis_days_before'] = np.where(mass_shooters['Timeline of Signs of Crisis'] == 0, 1, 0)
    mass_shooters['timeline_of_signs_of_crisis_weeks_before'] = np.where(mass_shooters['Timeline of Signs of Crisis'] == 1, 1, 0)
    mass_shooters['timeline_of_signs_of_crisis_months_before'] = np.where(mass_shooters['Timeline of Signs of Crisis'] == 2, 1, 0)
    mass_shooters['timeline_of_signs_of_crisis_years_before'] = np.where(mass_shooters['Timeline of Signs of Crisis'] == 3, 1, 0)
    mass_shooters['suicidality_no_evidence'] = np.where(mass_shooters['Suicidality'] == 0, 1, 0)
    mass_shooters['suicidality_yes_prior_to_shooting'] = np.where(mass_shooters['Suicidality'] == 1, 1, 0)
    mass_shooters['suicidality_intended_to_die_in_shooting_no_prior'] = np.where(mass_shooters['Suicidality'] == 2, 1, 0)
    mass_shooters['voluntary_or_involuntary_hospitalization_na'] = np.where(mass_shooters['Voluntary or Involuntary Hospitalization'] == 0, 1, 0)
    mass_shooters['voluntary_or_involuntary_hospitalization_voluntary'] = np.where(mass_shooters['Voluntary or Involuntary Hospitalization'] == 1, 1, 0)
    mass_shooters['voluntary_or_involuntary_hospitalization_involuntary'] = np.where(mass_shooters['Voluntary or Involuntary Hospitalization'] == 2, 1, 0)
    mass_shooters['motive_racism_xenophobia_no_evidence'] = np.where(mass_shooters['Motive: Racism/Xenophobia'] == 0, 1, 0)
    mass_shooters['motive_racism_xenophobia_targeting_color'] = np.where(mass_shooters['Motive: Racism/Xenophobia'] == 1, 1, 0)
    mass_shooters['motive_racism_xenophobia_targeting_white'] = np.where(mass_shooters['Motive: Racism/Xenophobia'] == 2, 1, 0)
    mass_shooters['motive_religious_hate_no_evidence'] = np.where(mass_shooters['Motive: Religious Hate'] == 0, 1, 0)
    mass_shooters['motive_religious_hate_antisemitism'] = np.where(mass_shooters['Motive: Religious Hate'] == 1, 1, 0)
    mass_shooters['motive_religious_hate_islamophobia'] = np.where(mass_shooters['Motive: Religious Hate'] == 2, 1, 0)
    mass_shooters['motive_religious_hate_angry_with_christianity_or_god'] = np.where(mass_shooters['Motive: Religious Hate'] == 3, 1, 0)
    mass_shooters['motive_other_no_evidence'] = np.where(mass_shooters['Motive: Other\xa0'] == 0, 1, 0)
    mass_shooters['motive_other_yes'] = np.where(mass_shooters['Motive: Other\xa0'] == 1, 1, 0)
    mass_shooters['motive_other_generalized_anger'] = np.where(mass_shooters['Motive: Other\xa0'] == 2, 1, 0)
    mass_shooters['role_of_psychosis_in_the_shooting_no_evidence'] = np.where(mass_shooters['Role of Psychosis in the Shooting'] == 0, 1, 0)
    mass_shooters['role_of_psychosis_in_the_shooting_minor_role'] = np.where(mass_shooters['Role of Psychosis in the Shooting'] == 1, 1, 0)
    mass_shooters['role_of_psychosis_in_the_shooting_moderate_role'] = np.where(mass_shooters['Role of Psychosis in the Shooting'] == 2, 1, 0)
    mass_shooters['role_of_psychosis_in_the_shooting_major_role'] = np.where(mass_shooters['Role of Psychosis in the Shooting'] == 3, 1, 0)
    mass_shooters['social_media_use_no_evidence'] = np.where(mass_shooters['Social Media Use\xa0'] == 0, 1, 0)
    mass_shooters['social_media_use_yes'] = np.where(mass_shooters['Social Media Use\xa0'] == 1, 1, 0)
    mass_shooters['social_media_use_na'] = np.where(mass_shooters['Social Media Use\xa0'] == 2, 1, 0)
    mass_shooters['pop_culture_connection_no_evidence'] = np.where(mass_shooters['Pop Culture Connection'] == 0, 1, 0)
    mass_shooters['pop_culture_connection_explicit_reference'] = np.where(mass_shooters['Pop Culture Connection'] == 1, 1, 0)
    mass_shooters['pop_culture_connection_tangential_reference'] = np.where(mass_shooters['Pop Culture Connection'] == 2, 1, 0)
    mass_shooters['firearm_proficiency_no_experience'] = np.where(mass_shooters['Firearm Proficiency'] == 0, 1, 0)
    mass_shooters['firearm_proficiency_some_experience'] = np.where(mass_shooters['Firearm Proficiency'] == 1, 1, 0)
    mass_shooters['firearm_proficiency_more_experienced'] = np.where(mass_shooters['Firearm Proficiency'] == 2, 1, 0)
    mass_shooters['firearm_proficiency_very_experienced'] = np.where(mass_shooters['Firearm Proficiency'] == 3, 1, 0)
    casualties_col = [
    'Number Killed',
    'Number Injured'
    ]
    mass_shooters['agg_casualties'] = mass_shooters[casualties_col].sum(axis=1)
    mass_shooters['shooter_volatility'] = np.where(mass_shooters.agg_casualties > 10, 'High Volatility', 'Low Volatility')
    unaggregated_mass_shooters = mass_shooters
    return unaggregated_mass_shooters

# =======================================================================================================
# unaggregated_mass_shooters END
# =======================================================================================================