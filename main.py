#!/usr/bin/env python3
"""
3D Periodic Table Viewer
A GUI application to display and explore elements of the periodic table in 3D.
"""
import sys
from PyQt5.QtWidgets import QApplication
from periodic_table_window import PeriodicTableWindow

def main():
    """Main entry point for the application"""
    app = QApplication(sys.argv)
    window = PeriodicTableWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()