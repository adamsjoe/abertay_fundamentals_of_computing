import csv
import os
import sys

# constants
FILENAME_IN = 'Road_Accident_Data.csv'

# file constants
ACCIDENT_INDEX = 0
ACCIDENT_DATE = 1
DAY_OF_WEEK = 2
JUNCTION_CONTROL = 3
JUNCTION_DETAIL = 4
ACCIDENT_SEVERITY = 5
LATITUDE = 6
LIGHT_CONDITIONS = 7
LOCAL_AUTHORITY_DISTRICT = 8
CARRIAGEWAY_HAZARDS = 9
LONGITUDE = 10
NUMBER_OF_CASUALTIES = 11
NUMBER_OF_VEHICLES = 12
POLICE_FORCE = 13
ROAD_SURFACE_CONDITIONS = 14
ROAD_TYPE = 15
SPEED_LIMIT = 16
TIME = 17
URBAN_OR_RURAL_AREA = 18
WEATHER_CONDITIONS = 19
VEHICLE_TYPE = 20


def open_file(file_in, skip_header=True):
    print(f'Opening file: {file_in}')

    # setup a variable to hold the data
    data = ''

    try:
        with open(file_in, encoding='utf-8-sig', mode='r') as file:
            reader = csv.reader(file)
            if skip_header is True:
                # if skip_header is true, skip to the next line
                next(reader, None)
            # make each row in the input file into a tuple and add this to a list to be returned
            data = [tuple(row) for row in reader]
    # handle file not founds
    except FileNotFoundError:
        print(f'File {file_in} does not exist')
        sys.exit(1)
    # catch any other errors
    except:
        print(f'Opening file {file_in} failed.  No further information available')
        sys.exit(1)
    # return data
    return data


def getYears(dataIn):
    tmpYears = {row[ACCIDENT_DATE].split("-")[2] for row in data}
    return sorted(tmpYears)


# entry point
data = open_file(FILENAME_IN)
print(data[1])
print(f"Number of rows: {len(data)}")

# work out how many years of data we have - use a set to ensure we have unique values
years = getYears(data)
print("Unique years:", years)
