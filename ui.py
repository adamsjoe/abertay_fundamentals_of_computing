from PyQt6.QtWidgets import (
    QWidget, QGridLayout, QLabel, QComboBox, QPushButton,
    QMainWindow, QMessageBox, QVBoxLayout, QToolTip
)
from PyQt6.QtGui import QKeyEvent, QAction
from PyQt6.QtCore import Qt
from constants import ACCIDENT_DATE, POLICE_FORCE, LOCAL_AUTHORITY_DISTRICT, NUMBER_OF_CASUALTIES, NUMBER_OF_VEHICLES
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from collections import defaultdict
import numpy as np
import calendar

class MyWindow(QMainWindow):
    def __init__(self, years, data):
        super().__init__()
        self.setWindowTitle("My Python Assignment")
        self.data = data
        self.years = years
        self.points_info = []  # store points for tooltips

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QVBoxLayout()
        central_widget.setLayout(self.main_layout)

        # Top controls layout
        controls_layout = QGridLayout()
        self.main_layout.addLayout(controls_layout)

        # Year dropdown
        self.year_label = QLabel("Year:")
        self.year_combo = QComboBox()
        self.year_combo.addItems([str(year) for year in self.years])
        self.year_combo.currentTextChanged.connect(self.on_year_selected)

        # Police dropdown
        self.police_label = QLabel("Police Force:")
        self.police_combo = QComboBox()
        self.police_combo.setEnabled(False)
        self.police_combo.currentTextChanged.connect(self.on_police_selected)

        # Local Authority dropdown
        self.local_label = QLabel("Local Authority:")
        self.local_combo = QComboBox()
        self.local_combo.setEnabled(False)
        self.local_combo.currentTextChanged.connect(self.on_local_selected)

        # Show results button
        self.show_button = QPushButton("Show Results")
        self.show_button.setEnabled(False)
        self.show_button.clicked.connect(self.show_results)

        # Add widgets to grid
        controls_layout.addWidget(self.year_label, 0, 0)
        controls_layout.addWidget(self.year_combo, 0, 1)
        controls_layout.addWidget(self.police_label, 0, 2)
        controls_layout.addWidget(self.police_combo, 0, 3)
        controls_layout.addWidget(self.local_label, 0, 4)
        controls_layout.addWidget(self.local_combo, 0, 5)
        controls_layout.addWidget(self.show_button, 0, 6)

        # Matplotlib canvas
        self.figure = Figure(figsize=(10,5))
        self.canvas = FigureCanvas(self.figure)
        self.main_layout.addWidget(self.canvas)
        self.canvas.mpl_connect("motion_notify_event", self.on_hover)

        # Menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        help_menu = menubar.addMenu("Help")

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    def on_year_selected(self, year):
        self.police_combo.clear()
        self.police_combo.setEnabled(True)
        police_for_year = sorted({
            row[POLICE_FORCE]
            for row in self.data
            if row[ACCIDENT_DATE].split("-")[2] == year
        })
        self.police_combo.addItems(police_for_year)
        self.police_combo.setEnabled(True)

        # If only 1 police, trigger the handler manually
        if len(police_for_year) == 1:
            self.on_police_selected(police_for_year[0])        

        self.local_combo.clear()
        self.local_combo.setEnabled(False)
        self.show_button.setEnabled(False)

    def on_police_selected(self, police):
        year = self.year_combo.currentText()
        self.local_combo.clear()
        self.local_combo.setEnabled(True)
        locals_for_selection = sorted({
            row[LOCAL_AUTHORITY_DISTRICT]
            for row in self.data
            if row[ACCIDENT_DATE].split("-")[2] == year and row[POLICE_FORCE] == police
        })
        self.local_combo.addItems(locals_for_selection)
        self.local_combo.setEnabled(True)

        # If only 1 local authority, trigger the handler manually
        if len(locals_for_selection) == 1:
            self.on_local_selected(locals_for_selection[0])

        self.show_button.setEnabled(False)

    def on_local_selected(self, local):
        self.show_button.setEnabled(bool(local))

    def show_results(self):
        year = self.year_combo.currentText()
        police = self.police_combo.currentText()
        local = self.local_combo.currentText()

        filtered = [
            row for row in self.data
            if row[ACCIDENT_DATE].split("-")[2] == year
            and row[POLICE_FORCE] == police
            and row[LOCAL_AUTHORITY_DISTRICT] == local
        ]

        # Aggregate data by month
        accidents_by_month = defaultdict(int)
        casualties_by_month = defaultdict(int)
        vehicles_by_month = defaultdict(int)

        for row in filtered:
            day, month, _ = row[ACCIDENT_DATE].split("-")
            month = int(month)
            accidents_by_month[month] += 1
            casualties_by_month[month] += int(row[NUMBER_OF_CASUALTIES])
            vehicles_by_month[month] += int(row[NUMBER_OF_VEHICLES])

        months = list(range(1,13))
        accidents = [accidents_by_month[m] for m in months]
        casualties = [casualties_by_month[m] for m in months]
        vehicles = [vehicles_by_month[m] for m in months]

        # Plot
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        self.acc_line, = ax.plot(months, accidents, label="Accidents", marker='o')
        self.cas_line, = ax.plot(months, casualties, label="Casualties", marker='s')
        self.veh_line, = ax.plot(months, vehicles, label="Vehicles", marker='^')

        ax.set_xlabel("Month")
        ax.set_ylabel("Count")
        ax.set_title(f"Year {year} - {police} - {local}")

        months = list(range(1, 13))
        month_labels = [calendar.month_abbr[m] for m in months]

        ax.set_xticks(months)
        ax.set_xticklabels(month_labels)

        ax.legend()
        ax.grid(True)
        self.canvas.draw()

        # store points for tooltip
        self.points_info = []
        for line, label, values in [(self.acc_line, "Accidents", accidents),
                                    (self.cas_line, "Casualties", casualties),
                                    (self.veh_line, "Vehicles", vehicles)]:
            xdata = line.get_xdata()
            ydata = line.get_ydata()
            for x, y in zip(xdata, ydata):
                self.points_info.append((x, y, label))

    def on_hover(self, event):
        if event.xdata is None or event.ydata is None:
            return
        # threshold distance in data units
        threshold = 0.3
        for x, y, label in self.points_info:
            if abs(event.xdata - x) < threshold and abs(event.ydata - y) < threshold:
                QToolTip.showText(self.mapToGlobal(self.canvas.pos()),
                                  f"{label}: {y} (Month {int(x)})")
                return
        QToolTip.hideText()

    def show_about(self):
        message = QMessageBox(self)
        message.setWindowTitle("About This App")
        message.setText("<b>Fundamentals of Computing - Assignment</b><br /><b>Name</b>: Joseph Adams<br /><b>Student ID:</b>2411484")
        message.setIcon(QMessageBox.Icon.Information)
        message.exec()
        
        