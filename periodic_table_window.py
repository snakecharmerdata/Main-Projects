"""
Main window for the 3D Periodic Table Viewer application.
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QComboBox, QPushButton, QLabel, QSlider, QGroupBox,
                            QTextEdit, QSizePolicy)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont

from element_3d_view import Element3DView
from element_data_adapter import ELEMENT_DATA
from element_descriptions import get_element_description

class PeriodicTableWindow(QMainWindow):
    """Main window class for the 3D Periodic Table application"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Periodic Table Viewer")
        self.setMinimumSize(1000, 700)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        
        # Create 3D view widget
        self.element_view = Element3DView()
        main_layout.addWidget(self.element_view, 3)
        
        # Create sidebar for controls
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)
        main_layout.addWidget(sidebar, 1)
        
        # Element selector
        selector_group = QGroupBox("Element Selection")
        selector_layout = QVBoxLayout(selector_group)
        
        self.element_selector = QComboBox()
        for atomic_num, element in sorted(ELEMENT_DATA.items()):
            self.element_selector.addItem(f"{atomic_num}. {element['symbol']} - {element['name']}")
        self.element_selector.setCurrentIndex(0)
        self.element_selector.currentIndexChanged.connect(self.on_element_changed)
        
        selector_layout.addWidget(self.element_selector)
        sidebar_layout.addWidget(selector_group)
        
        # Element information
        info_group = QGroupBox("Element Information")
        info_layout = QVBoxLayout(info_group)
        
        self.element_name = QLabel()
        self.element_name.setFont(QFont("Arial", 14, QFont.Bold))
        self.element_symbol = QLabel()
        self.element_symbol.setFont(QFont("Arial", 18, QFont.Bold))
        self.atomic_number = QLabel()
        self.atomic_weight = QLabel()
        self.category = QLabel()
        self.electron_config = QLabel()
        self.electron_config.setWordWrap(True)
        
        info_layout.addWidget(self.element_name)
        info_layout.addWidget(self.element_symbol)
        info_layout.addWidget(self.atomic_number)
        info_layout.addWidget(self.atomic_weight)
        info_layout.addWidget(self.category)
        info_layout.addWidget(self.electron_config)
        
        sidebar_layout.addWidget(info_group)
        
        # Element description area
        description_group = QGroupBox("Element Description")
        description_layout = QVBoxLayout(description_group)
        
        self.element_description = QTextEdit()
        self.element_description.setReadOnly(True)
        self.element_description.setFont(QFont("Arial", 10))
        self.element_description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        description_layout.addWidget(self.element_description)
        sidebar_layout.addWidget(description_group)
        
        # View controls
        view_group = QGroupBox("View Controls")
        view_layout = QVBoxLayout(view_group)
        
        # Rotation sliders
        x_rotation_layout = QHBoxLayout()
        x_rotation_layout.addWidget(QLabel("X Rotation:"))
        self.x_rotation = QSlider(Qt.Horizontal)
        self.x_rotation.setRange(0, 360)
        self.x_rotation.setValue(30)
        self.x_rotation.valueChanged.connect(self.element_view.set_x_rotation)
        x_rotation_layout.addWidget(self.x_rotation)
        view_layout.addLayout(x_rotation_layout)
        
        y_rotation_layout = QHBoxLayout()
        y_rotation_layout.addWidget(QLabel("Y Rotation:"))
        self.y_rotation = QSlider(Qt.Horizontal)
        self.y_rotation.setRange(0, 360)
        self.y_rotation.setValue(30)
        self.y_rotation.valueChanged.connect(self.element_view.set_y_rotation)
        y_rotation_layout.addWidget(self.y_rotation)
        view_layout.addLayout(y_rotation_layout)
        
        z_rotation_layout = QHBoxLayout()
        z_rotation_layout.addWidget(QLabel("Z Rotation:"))
        self.z_rotation = QSlider(Qt.Horizontal)
        self.z_rotation.setRange(0, 360)
        self.z_rotation.setValue(0)
        self.z_rotation.valueChanged.connect(self.element_view.set_z_rotation)
        z_rotation_layout.addWidget(self.z_rotation)
        view_layout.addLayout(z_rotation_layout)
        
        # Zoom slider
        zoom_layout = QHBoxLayout()
        zoom_layout.addWidget(QLabel("Zoom:"))
        self.zoom = QSlider(Qt.Horizontal)
        self.zoom.setRange(10, 200)
        self.zoom.setValue(100)
        self.zoom.valueChanged.connect(lambda z: self.element_view.set_zoom(z/100))
        zoom_layout.addWidget(self.zoom)
        view_layout.addLayout(zoom_layout)
        
        sidebar_layout.addWidget(view_group)
        
        # Auto-rotation toggle
        self.auto_rotate = QPushButton("Start Auto-Rotation")
        self.auto_rotate.setCheckable(True)
        self.auto_rotate.toggled.connect(self.toggle_auto_rotation)
        sidebar_layout.addWidget(self.auto_rotate)
        
        # Reset view button
        self.reset_view = QPushButton("Reset View")
        self.reset_view.clicked.connect(self.reset_view_settings)
        sidebar_layout.addWidget(self.reset_view)
        
        # Spacer to push everything up
        sidebar_layout.addStretch()
        
        # Initialize with the first element
        self.on_element_changed(0)
    
    def on_element_changed(self, index):
        """Handle element selection change"""
        atomic_num = index + 1
        element = ELEMENT_DATA.get(atomic_num)
        if element:
            self.element_name.setText(f"Name: {element['name']}")
            self.element_symbol.setText(f"Symbol: {element['symbol']}")
            self.atomic_number.setText(f"Atomic Number: {atomic_num}")
            self.atomic_weight.setText(f"Atomic Weight: {element['mass']} u")
            self.category.setText(f"Category: {element['category']}")
            self.electron_config.setText(f"Electron Config: {element.get('electron_configuration', 'N/A')}")
            
            # Update the element description
            description = get_element_description(atomic_num)
            self.element_description.setText(description)
            
            # Update 3D view with new element
            self.element_view.set_element(atomic_num)
    
    def toggle_auto_rotation(self, enabled):
        """Toggle automatic rotation"""
        if enabled:
            self.auto_rotate.setText("Stop Auto-Rotation")
            self.element_view.start_auto_rotation()
        else:
            self.auto_rotate.setText("Start Auto-Rotation")
            self.element_view.stop_auto_rotation()
    
    def reset_view_settings(self):
        """Reset view to default settings"""
        self.x_rotation.setValue(30)
        self.y_rotation.setValue(30)
        self.z_rotation.setValue(0)
        self.zoom.setValue(100)
        self.element_view.reset_view()
