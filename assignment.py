import csv
import sys
from PyQt6.QtWidgets import QApplication
from constants import ACCIDENT_DATE, POLICE_FORCE, LOCAL_AUTHORITY_DISTRICT
from ui import MyWindow

FILENAME_IN = 'Road_Accident_Data.csv'

def open_file(file_in, skip_header=True):
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
        print(f'Failed to open file {file_in}: {e}')
        sys.exit(1)
    return data

def get_years(data):
    return sorted({row[ACCIDENT_DATE].split("-")[2] for row in data})

if __name__ == "__main__":
    data = open_file(FILENAME_IN)
    years = get_years(data)

    app = QApplication(sys.argv)
    window = MyWindow(years, data)
    window.showFullScreen()
    sys.exit(app.exec())