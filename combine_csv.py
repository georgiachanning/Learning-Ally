#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from difflib import get_close_matches
import pandas
from parameters import Parameters


def main():
    program_args = Parameters.parse_parameters()
    df1 = pandas.read_csv('/Users/georgiachanning/LA/CAdistricts_and_schools.csv')
    df2 = pandas.read_csv('/Users/georgiachanning/LA/all_output.csv')
    outfile = '/Users/georgiachanning/LA/integrated_output.csv'
    Georgia_schools = df2['School']
    
    df3 = df1
    columns = ['AVID', 'Disabilities', 'Dyslexia mentioned',
       'Gen Ed', 'Orton-Gillingham', 'Other', 'Reading Specialist',
       'Resource Specialist', 'Socioeconomically Disadvantaged']
    for column in columns:
        df3.insert(len(df3.columns), column, "NaN")
        
    Georgia_school_names = []
    mds_to_name = {}
    could_not_match = []
    for name in Georgia_schools:
        if isinstance(name, str):
            Georgia_school_names.append(name)
    
    close_matches = {}
    building_codes = df1['MDS_Building_ID']
    LA_school = df1['Building_Name']
    
    for school in Georgia_school_names:
        print(school)
        close_matches[school] = get_close_matches(school, LA_school)
        if len(close_matches[school]) == 0:
            could_not_match.append(school)
            continue
        
        closest_match = close_matches[school][0]
        index = list(LA_school).index(closest_match)
        mds_to_name[school] = building_codes[index]
        for column in columns:
            value = df2.at[Georgia_school_names.index(school), column]
            df3.at[index, column] = value
            
    df3.to_csv(outfile)
    
    return

if __name__ == '__main__':
    main()