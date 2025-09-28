from PyQt6.QtWidgets import (
    QWidget, QGridLayout, QLabel, QComboBox, QPushButton,
    QMainWindow, QMessageBox
)
from PyQt6.QtGui import QKeyEvent, QAction
from PyQt6.QtCore import Qt
from constants import ACCIDENT_DATE, POLICE_FORCE, LOCAL_AUTHORITY_DISTRICT

class MyWindow(QMainWindow):
    def __init__(self, years, police, localAuthorities, data):
        super().__init__()
        self.setWindowTitle("My Python Assignment")
        self.years = years
        self.policeForces = police
        self.localAuthorities = localAuthorities
        self.data = data
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout()

        # Year dropdown
        self.year_label = QLabel("Year:")
        self.year_combo = QComboBox()
        self.year_combo.addItems([str(year) for year in self.years])

        # Police dropdown
        self.police_label = QLabel("Police Force:")
        self.police_combo = QComboBox()
        self.police_combo.addItems([str(p) for p in self.policeForces])

        # Local Authority dropdown
        self.local_label = QLabel("Local Authority:")
        self.local_combo = QComboBox()
        self.local_combo.addItems([str(l) for l in self.localAuthorities])

        # Show results button
        self.show_button = QPushButton("Show Results")
        self.show_button.clicked.connect(self.show_results)

        # Add widgets to layout (single row)
        layout.addWidget(self.year_label, 0, 0)
        layout.addWidget(self.year_combo, 0, 1)
        layout.addWidget(self.police_label, 0, 2)
        layout.addWidget(self.police_combo, 0, 3)
        layout.addWidget(self.local_label, 0, 4)
        layout.addWidget(self.local_combo, 0, 5)
        layout.addWidget(self.show_button, 0, 6)

        central_widget.setLayout(layout)

        # Menu
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

        print(f"Found {len(filtered)} matching accidents")
        for row in filtered[:5]:  # print first 5 rows
            print(row)

    def show_about(self):
        QMessageBox.information(self, "About", "Data Selector v1.0\nCreated with PyQt6")