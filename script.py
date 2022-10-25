"""
Seedcorn Maggot Models

This script generates heat unit accumulations for Delia platura (Meigens), seedcorn maggot, using different published degree day models. See README.md for references and model specifications.

Author: Dan Olmstead
Version: 0.0.0
Last modified: 2022-10-18
"""
from doctest import OutputChecker
import pandas as pd
import requests as r
import json
import datetime as dt

pd.set_option('display.max_rows', None)

class Inputs:
        def __init__(self):
            self.coordinatesCsv = input('\nINPUT COORDINATES LOCATION\nProvide full path to coordinates CSV file (C:\...): ')
            self.outputDirectory = input('\nOUTPUT FILES LOCATION\nSpecify the output folder (C:\...): ')
            self.startDateTimeOne = input('\nTIME PERIOD ONE MEAN TEMPERATURE\nEnter a start date for time period 1 mean tempature: (YYYY-MM-DD): ')
            self.endDateTimeOne = input('Enter an end date for time period 1 mean tempature: (YYYY-MM-DD): ')
            self.startDateTimeTwo = input('\nTIME PERIOD TWO MEAN TEMPERATURE\nEnter a start date for time period 2 mean tempature: (YYYY-MM-DD): ')
            self.endDateTimeTwo = input('Enter a end date for time period 2 mean tempature: (YYYY-MM-DD): ')
            self.newaStartDate = input('\nNEWA MODEL\nEnter a start date biofix for NEWA modeling (Jan 1 recommended; YYYY-MM-DD): ')
            self.ohioStartDate = input('\nOHIO MODEL\nEnter an oviposition biofix date for Ohio model output (YYYY-MM-DD): ')
            self.endDate = input('\nMODEL TERMINATION\nEnter a single end date for the NEWA and Ohio models (YYYY-MM-DD): ')

def GetInputs():
    return Inputs()

input = GetInputs()

coordinatesCsv = input.coordinatesCsv
outputDirectory = input.outputDirectory
startDateTimeOne = input.startDateTimeOne
endDateTimeOne = input.endDateTimeOne
startDateTimeTwo = input.startDateTimeTwo
endDateTimeTwo = input.endDateTimeTwo
newaStartDate = input.newaStartDate
ohioStartDate = input.ohioStartDate
endDate = input.endDate


coordinatesList = pd.read_csv(coordinatesCsv)


def TimeOneTempSummary():
    """
    Calculate weekly average temperature for first specified time period.
    """
    # For item in 'coordinateList':
    output = pd.DataFrame()
    for i, row in coordinatesList.iterrows():
        # Form the request
        sdate = str(startDateTimeOne)
        edate = str(endDateTimeOne)
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
        output = pd.concat([output,df], ignore_index=True)
    max = output.groupby('id')['maxtC'].max()
    min = output.groupby('id')['mintC'].min()
    meanTemps1 = pd.merge(max,min, on='id')
    meanTemps1['week 17 mean'] = ( meanTemps1['maxtC'] + meanTemps1['mintC'] ) / 2
    meanTemps1 = meanTemps1.drop(['maxtC','mintC'], axis=1)
    meanTemps1 = meanTemps1.round({'week 17 mean': 1})
    # print('TIME ONE MEAN TEMPS C:')
    # print(meanTemps1)
    return meanTemps1


def TimeTwoTempSummary():
    """
    Calculate weekly average temperature for first specified time period.
    """
    # For item in 'coordinateList':
    output = pd.DataFrame()
    for i, row in coordinatesList.iterrows():
        # Form the request
        sdate = str(startDateTimeTwo)
        edate = str(endDateTimeTwo)
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
        output = pd.concat([output,df], ignore_index=True)
    max = output.groupby('id')['maxtC'].max()
    min = output.groupby('id')['mintC'].min()
    meanTemps2 = pd.merge(max,min, on='id')
    meanTemps2['week 18 mean'] = ( meanTemps2['maxtC'] + meanTemps2['mintC'] ) / 2
    meanTemps2 = meanTemps2.drop(['maxtC','mintC'], axis=1)
    meanTemps2 = meanTemps2.round({'week 18 mean': 1})
    return meanTemps2

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
        raw = pd.concat([raw,df], ignore_index=True)
        # raw = raw.append(df)
    # Export heat unit calcs
    csv = raw.drop(['accum-1','firstAdults'], axis=1)
    now = dt.datetime.now().strftime("%Y%m%d%H%M%S")
    csv.to_csv(outputDirectory + '\\newa_model_heat_units_' + now + '.csv', index=False)
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
    daily = pd.DataFrame()
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
        raw = pd.concat([raw,df], ignore_index=True)
    # Export heat unit calcs
    csv = raw.drop(['accum-1','firstAdults'], axis=1)
    now = dt.datetime.now().strftime("%Y%m%d%H%M%S")
    raw.to_csv(outputDirectory + '\\ohio_model_heat_units_' + now + '.csv', index=False)
    raw = raw.loc[raw['firstAdults'] == 1 ]
    raw = raw.drop(['maxtF','mintF','maxtC','mintC','heatUnits','accum','accum-1','firstAdults'], axis=1)
    raw = raw.rename(columns={'date': 'ohioDate'})
    ohioOutput = raw
    return ohioOutput


def GetSoilTypes():
    """
    (dataset) Natural Resources Conservation Service (2018). Soil Data Access Web Service. Natural Resources Conservation Service. https://data.nal.usda.gov/dataset/soil-data-access-web-service. Accessed 2022-10-24
    """
    pass


def CompileResults():
    """
    Produce a single CSV file that reports both NEWA and Ohio model output for each location. 
    """
    time1 = TimeOneTempSummary()
    time2 = TimeTwoTempSummary()
    time1Time2 = pd.merge(time1,time2, on='id')
    newa = GetNewaOutput()
    ohio = GetOhioOutput()
    newa = newa.reset_index(drop=True)
    ohio = ohio.reset_index(drop=True)
    compiledResults = newa
    df1 = ohio[['ohioDate']]
    compiledResults = compiledResults.join(df1)
    compiledResults = pd.merge(time1Time2,compiledResults, on='id')
    now = dt.datetime.now().strftime("%Y%m%d%H%M%S")
    compiledResults.to_csv(outputDirectory + '\\scm_compiled_models_mean_temps_soil_types_' + now + '.csv', index=False)
    return compiledResults

print(CompileResults())