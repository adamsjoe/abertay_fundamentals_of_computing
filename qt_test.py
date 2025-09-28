import sys
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QComboBox, QPushButton

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Selector")
        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        # Year
        self.year_label = QLabel("Year:")
        self.year_combo = QComboBox()
        self.year_combo.addItems([str(year) for year in range(2000, 2026)])

        # Police Force
        self.police_label = QLabel("Police Force:")
        self.police_combo = QComboBox()
        self.police_combo.addItems([
            "Metropolitan",
            "City of London",
            "Greater Manchester",
            "West Midlands"
        ])

        # Local Authority
        self.local_label = QLabel("Local Authority:")
        self.local_combo = QComboBox()
        self.local_combo.addItems([
            "Camden",
            "Islington",
            "Hackney",
            "Greenwich"
        ])

        # Show Results Button
        self.show_button = QPushButton("Show Results")
        self.show_button.clicked.connect(self.show_results)

        # Add widgets to grid (row, column)
        layout.addWidget(self.year_label, 0, 0)
        layout.addWidget(self.year_combo, 0, 1)
        layout.addWidget(self.police_label, 0, 2)
        layout.addWidget(self.police_combo, 0, 3)
        layout.addWidget(self.local_label, 0, 4)
        layout.addWidget(self.local_combo, 0, 5)
        layout.addWidget(self.show_button, 0, 6)

        self.setLayout(layout)

    def show_results(self):
        year = self.year_combo.currentText()
        police = self.police_combo.currentText()
        local = self.local_combo.currentText()
        print(f"Year: {year}, Police Force: {police}, Local Authority: {local}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.showFullScreen()  # <-- full screen mode
    sys.exit(app.exec())
