import csv
import sys
from PyQt6.QtWidgets import QApplication
from constants import ACCIDENT_DATE, POLICE_FORCE, LOCAL_AUTHORITY_DISTRICT
from ui import MyWindow

FILENAME_IN = 'Road_Accident_Data.csv'

def open_file(file_in, skip_header=True):
    print(f'Opening file: {file_in}')
    data = []
    try:
        with open(file_in, encoding='utf-8-sig', mode='r') as file:
            reader = csv.reader(file)
            if skip_header:
                next(reader, None)
            data = [tuple(row) for row in reader]
    except FileNotFoundError:
        print(f'File {file_in} does not exist')
        sys.exit(1)
    except Exception as e:
        print(f'Opening file {file_in} failed: {e}')
        sys.exit(1)
    return data

def getYears(data):
    return sorted({row[ACCIDENT_DATE].split("-")[2] for row in data})

def getPolice(data):
    return sorted({row[POLICE_FORCE] for row in data})

def getLocalAuthority(data):
    return sorted({row[LOCAL_AUTHORITY_DISTRICT] for row in data})

if __name__ == "__main__":
    data = open_file(FILENAME_IN)
    print(f"Number of rows: {len(data)}")

    years = getYears(data)
    police = getPolice(data)
    localAuthorities = getLocalAuthority(data)

    app = QApplication(sys.argv)
    window = MyWindow(years, police, localAuthorities, data)
    window.showFullScreen()
    sys.exit(app.exec())