import csv
import os
import sys

# constants
FILENAME_IN = 'Road_Accident_Data.csv'

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

# entry point
data = open_file(FILENAME_IN)
print(data[1])
print(f"Number of rows: {len(data)}")
