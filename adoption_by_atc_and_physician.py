import pandas as pd
import numpy as np
import json
import csv

first_adoption = json.load(open('first_adoption.json'))
adoptions = json.load(open('mean_time_adoptions.json'))
df = pd.read_csv('13-April-2017-subset.csv')
df = df.sort_values(by=['sv_phy_num', 'pur_date'])
physicians = list(set(df.sv_phy_num))
headers  = ['id', 'first_prescription', 'last_prescription', 'no_prescriptions', 'time_to_first_prescription', 'first_prescription_branded', 
            'no_prescriptions_branded', 'time_to_adopt_prescription_branded', 'first_prescription_generic', 'no_prescriptions_generic', 
            'time_to_adopt_prescription_generic', 'first_prescription_01', 'first_prescription_branded_01', 'first_prescription_generic_01', 'no_prescriptions_01', 
            'no_prescriptions_branded_01', 'no_prescriptions_generic_01', 'time_to_adopt_prescription_01', 'time_to_adopt_prescription_branded_01', 
            'time_to_adopt_prescription_generic_01', 'type_of_adopter_01', 'type_of_adopter_branded_01', 'type_of_adopter_generic_01',
            'first_prescription_02', 'first_prescription_branded_02', 'first_prescription_generic_02', 'no_prescriptions_02', 
            'no_prescriptions_branded_02', 'no_prescriptions_generic_02', 'time_to_adopt_prescription_02', 'time_to_adopt_prescription_branded_02', 
            'time_to_adopt_prescription_generic_02', 'type_of_adopter_02', 'type_of_adopter_branded_02', 'type_of_adopter_generic_02',
            'first_prescription_03', 'first_prescription_branded_03', 'first_prescription_generic_03', 'no_prescriptions_03', 
            'no_prescriptions_branded_03', 'no_prescriptions_generic_03', 'time_to_adopt_prescription_03', 'time_to_adopt_prescription_branded_03', 
            'time_to_adopt_prescription_generic_03', 'type_of_adopter_03', 'type_of_adopter_branded_03', 'type_of_adopter_generic_03',
            'first_prescription_04', 'first_prescription_branded_04', 'first_prescription_generic_04', 'no_prescriptions_04', 
            'no_prescriptions_branded_04', 'no_prescriptions_generic_04', 'time_to_adopt_prescription_04', 'time_to_adopt_prescription_branded_04', 
            'time_to_adopt_prescription_generic_04', 'type_of_adopter_04', 'type_of_adopter_branded_04', 'type_of_adopter_generic_04',
            'first_prescription_05', 'first_prescription_branded_05', 'first_prescription_generic_05', 'no_prescriptions_05', 
            'no_prescriptions_branded_05', 'no_prescriptions_generic_05', 'time_to_adopt_prescription_05', 'time_to_adopt_prescription_branded_05', 
            'time_to_adopt_prescription_generic_05', 'type_of_adopter_05', 'type_of_adopter_branded_05', 'type_of_adopter_generic_05',
            'first_prescription_07', 'first_prescription_branded_07', 'first_prescription_generic_07', 'no_prescriptions_07', 
            'no_prescriptions_branded_07', 'no_prescriptions_generic_07', 'time_to_adopt_prescription_07', 'time_to_adopt_prescription_branded_07', 
            'time_to_adopt_prescription_generic_07', 'type_of_adopter_07', 'type_of_adopter_branded_07', 'type_of_adopter_generic_07']

def type_of_adopter_fn(atc, time_to_prescription, branded = None):
    atc_code = atc[-2:]

    if branded == None:
        keys_label = atc_code
    else:
        keys_label = branded + '_' + str(atc_code)

    mean =  adoptions[keys_label]['mean']
    std =  adoptions[keys_label]['std']

    if (time_to_prescription < (mean - 2 * std)):
        return 1
    elif (time_to_prescription >= (mean - 2 * std)) and (time_to_prescription < (mean - std)):
        return 2
    elif (time_to_prescription >= (mean - std)) and (time_to_prescription < mean):
        return 3
    elif (time_to_prescription >= (mean)) and (time_to_prescription < (mean + std)):
        return 4
    elif (time_to_prescription >= (mean + std)) and (time_to_prescription < (mean + 2 * std)):
        return 5
    else:
        return 6

def generate_atc_data(atc):
    try:
        sample_atc = sample[sample.atc == atc]
        indices_sample_atc = list(sample_atc.index)
        first_prescription = sample_atc.pur_date[indices_sample_atc[0]]
        no_prescriptions = len(indices_sample_atc)
        time_to_adopt_prescription = (pd.to_datetime(first_prescription) - pd.to_datetime(first_adoption['first_prescription'])).days
        type_of_adopter = type_of_adopter_fn(atc, time_to_adopt_prescription)

        try:
            sample_branded_atc = sample_atc[sample_atc.generic == 0]
            indices_branded_atc = list(sample_branded_atc.index)
            first_prescription_branded = sample_branded_atc.pur_date[indices_branded_atc[0]]
            no_prescriptions_branded = len(indices_branded_atc)
            time_to_adopt_prescription_branded = (pd.to_datetime(first_prescription_branded) - pd.to_datetime(first_adoption['first_prescription_branded'])).days
            type_of_adopter_branded = type_of_adopter_fn(atc, time_to_adopt_prescription_branded, 'branded')

        except:
            first_prescription_branded = ''
            no_prescriptions_branded = ''
            time_to_adopt_prescription_branded = ''
            type_of_adopter_branded = ''

        try:
            sample_generic_atc = sample_atc[sample_atc.generic == 1]
            indices_generic_atc = list(sample_generic_atc.index)
            first_prescription_generic = sample_generic_atc.pur_date[indices_generic_atc[0]]
            no_prescriptions_generic = len(indices_generic_atc)
            time_to_adopt_prescription_generic = (pd.to_datetime(first_prescription_generic) - pd.to_datetime(first_adoption['first_prescription_generic'])).days
            type_of_adopter_generic = type_of_adopter_fn(atc, time_to_adopt_prescription_generic, 'generic')

        except:
            first_prescription_generic = ''
            no_prescriptions_generic = ''
            time_to_adopt_prescription_generic = ''
            type_of_adopter_generic = ''

    except:
        first_prescription = ''
        first_prescription_branded = ''
        first_prescription_generic = ''
        no_prescriptions = ''
        no_prescriptions_branded = ''
        no_prescriptions_generic = ''
        time_to_adopt_prescription = ''
        time_to_adopt_prescription_branded = ''
        time_to_adopt_prescription_generic = ''
        type_of_adopter = ''
        type_of_adopter_branded = ''
        type_of_adopter_generic = ''

    return [first_prescription, first_prescription_branded, first_prescription_generic, no_prescriptions, no_prescriptions_branded, no_prescriptions_generic, time_to_adopt_prescription, time_to_adopt_prescription_branded, time_to_adopt_prescription_generic, type_of_adopter, type_of_adopter_branded, type_of_adopter_generic]

with open('adoptions_by_atc_and_physician_test.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(headers)

    for i in physicians:
        sample = df[df.sv_phy_num == i]
        print i
        indices = list(sample.index)
        first = indices[0]
        last = indices[-1]
        first_prescription = sample.pur_date[first]
        last_prescription = sample.pur_date[last]
        no_prescriptions = len(indices)
        time_to_first_prescription = (pd.to_datetime(first_prescription) - pd.to_datetime(first_adoption['first_prescription'])).days

        try:
            sample_branded = sample[sample.generic == 0]
            indices_branded = list(sample_branded.index)
            first_prescription_branded = sample_branded.pur_date[indices_branded[0]]
            no_prescriptions_branded= len(indices_branded)
            time_to_adopt_prescription_branded = (pd.to_datetime(first_prescription_branded) - pd.to_datetime(first_adoption['first_prescription_branded'])).days

        except:
            first_prescription_branded = ''
            no_prescriptions_branded = ''
            time_to_adopt_prescription_branded = ''

        try:
            sample_generic = sample[sample.generic == 1]
            indices_generic = list(sample_generic.index)
            first_prescription_generic = sample_generic.pur_date[indices_generic[0]]
            no_prescriptions_generic = len(indices_generic)
            time_to_adopt_prescription_generic = (pd.to_datetime(first_prescription_generic) - pd.to_datetime(first_adoption['first_prescription_generic'])).days

        except:
            first_prescription_generic = ''
            no_prescriptions_generic = ''
            time_to_adopt_prescription_generic = ''

        row = [i, first_prescription, last_prescription, no_prescriptions, time_to_first_prescription, first_prescription_branded, no_prescriptions_branded, time_to_adopt_prescription_branded, first_prescription_generic, no_prescriptions_generic, time_to_adopt_prescription_generic]

        atcs = ['C10AA01', 'C10AA02', 'C10AA03', 'C10AA04', 'C10AA05', 'C10AA07']

        for a in atcs:
            atc_row = generate_atc_data(a)
            row.extend(atc_row)

        csvwriter.writerow(row)

