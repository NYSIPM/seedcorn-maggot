"""
Seedcorn Maggot Models

This script generates heat unit accumulations for Delia platura (Meigens), seedcorn maggot, using different published degree day models. See README.md for references and model specifications.

Author: Dan Olmstead
Version: 0.0.0
Last modified: 2022-10-18
"""
import pandas as pd
import requests as r
import json
import datetime as dt

pd.set_option('display.max_rows', None)

class Inputs:
        def __init__(self):
            self.coordinatesCsv = input('Provide full path to coordinates CSV file (C:\...): ')
            self.outputDirectory = input('Specify the output folder (C:\...): ')
            self.newaStartDate = input('Enter a start date biofix for NEWA modeling (Jan 1 recommended; YYYY-MM-DD): ')
            self.ohioStartDate = input('Enter an oviposition biofix date for Ohio model output (YYYY-MM-DD): ')
            self.endDate = input('Enter a single end date for the NEWA and Ohio models (YYYY-MM-DD): ')

def GetInputs():
    return Inputs()

input = GetInputs()

coordinatesCsv = input.coordinatesCsv
outputDirectory = input.outputDirectory
newaStartDate = input.newaStartDate
ohioStartDate = input.ohioStartDate
endDate = input.endDate


coordinatesList = pd.read_csv(coordinatesCsv)


def GetNewaOutput():
    """
    Calculate daily heat units and cumulative heat units using 'NEWA' model specifications provided in README.md
    """
    # Specify the model constants
    THRESHOLD_LOWER = 3.9
    HEAT_UNITS_BIOFIX_TO_ADULT = 254
    # Create an empty dataframe
    raw = pd.DataFrame()
    # For item in 'coordinateList':
    for i, row in coordinatesList.iterrows():
        # Form the request
        sdate = str(newaStartDate)
        edate = str(endDate)
        lon = str(row[2])
        lat = str(row[1])
        grid = '21' # PRISM data
        elems = 'maxt,mint'
        url = 'http://data.rcc-acis.org/GridData?'
        params = 'params={"sdate":"' + sdate + '","edate":"' + edate + '","loc":"' + lon + ',' + lat + '","grid":"' + grid + '","elems":"' + elems + '"}'
        packet = url + params
        # Query RCC-ACIS for daily max and min temperatures
        req = r.get(packet)
        data = json.loads(req.text)
        df = pd.json_normalize(data, 'data')
        df.columns = ['date','maxtF','mintF']
        df['id'] = row[0]
        df['id'] = df['id'].astype(str)
        df = df[['id','date','maxtF','mintF']]
        # Convert temperature values from Fahrenheit to Celcius
        df['maxtC'] = ( df['maxtF'] - 32 ) * ( 5 / 9 )
        df['mintC'] = ( df['mintF'] - 32 ) * ( 5 / 9 )
        # Tabulate daily heat units
        def HeatUnits(a):
            if ( ( ( a['maxtC'] + a['mintC']) / 2 ) - THRESHOLD_LOWER ) >= 0:
                return ( ( ( a['maxtC'] + a['mintC']) / 2 ) - THRESHOLD_LOWER )
            elif ( ( ( a['maxtC'] + a['mintC']) / 2 ) - THRESHOLD_LOWER ) < 0:
                return 0
        df['heatUnits'] = df.apply(lambda a: HeatUnits(a), axis=1)
        # Tabulate cumulative heat units
        df['accum'] = df['heatUnits'].cumsum()
        df = df.round({'maxtC': 1, 'mintC': 1, 'heatUnits': 1, 'accum': 1})
        # Flag the date of adult emergence
        df['accum-1'] = df['accum'].shift(1)
        def DateOfFirstAdultEmergence(a):
            if a['accum'] > HEAT_UNITS_BIOFIX_TO_ADULT and a['accum-1'] < HEAT_UNITS_BIOFIX_TO_ADULT:
                return 1
            elif a['accum'] > HEAT_UNITS_BIOFIX_TO_ADULT:
                return 0
            elif a['accum'] < HEAT_UNITS_BIOFIX_TO_ADULT:
                return 0
        df['firstAdults'] = df.apply(lambda a: DateOfFirstAdultEmergence(a), axis=1)
        raw = raw.append(df)
    raw = raw.loc[raw['firstAdults'] == 1 ]
    raw = raw.drop(['maxtF','mintF','maxtC','mintC','heatUnits','accum','accum-1','firstAdults'], axis=1)
    raw = raw.rename(columns={'date': 'newaDate'})
    newaOutput = raw
    return newaOutput


def GetOhioOutput():
    """
    Calculate daily heat units and cumulative heat units using 'Ohio' model specifications provided in README.md
    """
    # Specify the model constants
    THRESHOLD_LOWER = 3.9
    HEAT_UNITS_BIOFIX_TO_ADULT = 400
    # Create an empty dataframe
    raw = pd.DataFrame()
    # For item in 'coordinateList':
    for i, row in coordinatesList.iterrows():
        # Form the request
        sdate = str(ohioStartDate)
        edate = str(endDate)
        lon = str(row[2])
        lat = str(row[1])
        grid = '21' # PRISM data
        elems = 'maxt,mint'
        url = 'http://data.rcc-acis.org/GridData?'
        params = 'params={"sdate":"' + sdate + '","edate":"' + edate + '","loc":"' + lon + ',' + lat + '","grid":"' + grid + '","elems":"' + elems + '"}'
        packet = url + params
        # Query RCC-ACIS for daily max and min temperatures
        req = r.get(packet)
        data = json.loads(req.text)
        df = pd.json_normalize(data, 'data')
        df.columns = ['date','maxtF','mintF']
        df['id'] = row[0]
        df['id'] = df['id'].astype(str)
        df = df[['id','date','maxtF','mintF']]
        # Convert temperature values from Fahrenheit to Celcius
        df['maxtC'] = ( df['maxtF'] - 32 ) * ( 5 / 9 )
        df['mintC'] = ( df['mintF'] - 32 ) * ( 5 / 9 )
        # Tabulate daily heat units
        def HeatUnits(a):
            if ( ( ( a['maxtC'] + a['mintC']) / 2 ) - THRESHOLD_LOWER ) >= 0:
                return ( ( ( a['maxtC'] + a['mintC']) / 2 ) - THRESHOLD_LOWER )
            elif ( ( ( a['maxtC'] + a['mintC']) / 2 ) - THRESHOLD_LOWER ) < 0:
                return 0
        df['heatUnits'] = df.apply(lambda a: HeatUnits(a), axis=1)
        # Tabulate cumulative heat units
        df['accum'] = df['heatUnits'].cumsum()
        df = df.round({'maxtC': 1, 'mintC': 1, 'heatUnits': 1, 'accum': 1})
        # Flag the date of adult emergence
        df['accum-1'] = df['accum'].shift(1)
        def DateOfFirstAdultEmergence(a):
            if a['accum'] >= HEAT_UNITS_BIOFIX_TO_ADULT and a['accum-1'] < HEAT_UNITS_BIOFIX_TO_ADULT:
                return 1
            elif a['accum'] > HEAT_UNITS_BIOFIX_TO_ADULT:
                return 0
            elif a['accum'] < HEAT_UNITS_BIOFIX_TO_ADULT:
                return 0
        df['firstAdults'] = df.apply(lambda a: DateOfFirstAdultEmergence(a), axis=1)
        raw = raw.append(df)
    raw = raw.loc[raw['firstAdults'] == 1 ]
    raw = raw.drop(['maxtF','mintF','maxtC','mintC','heatUnits','accum','accum-1','firstAdults'], axis=1)
    raw = raw.rename(columns={'date': 'ohioDate'})
    ohioOutput = raw
    return ohioOutput

def CompileResults():
    """
    Produce a single CSV file that reports both NEWA and Ohio model output for each location. 
    """
    newa = GetNewaOutput()
    ohio = GetOhioOutput()
    newa = newa.reset_index(drop=True)
    ohio = ohio.reset_index(drop=True)
    compiledResults = newa
    df1 = ohio[['ohioDate']]
    compiledResults = compiledResults.join(df1)
    now = dt.datetime.now().strftime("%Y%m%d%H%M%S")
    compiledResults.to_csv(outputDirectory + '\\scm_compiled_model_emergence_dates_' + now + '.csv', index=False)
    return compiledResults

print(CompileResults())