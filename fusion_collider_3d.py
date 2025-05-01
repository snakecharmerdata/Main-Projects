import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QComboBox, 
                             QSlider, QGroupBox, QGridLayout, QTabWidget,
                             QSplitter, QFrame, QSizePolicy, QTextEdit,
                             QDialog, QScrollArea)
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QColor
# Add import for OpenGL GLUT
from OpenGL.GLUT import *

# Import our custom modules
from physics_engine import NuclearPhysics
from visualization_3d import CollisionVisualizer3D

# CERN particle data: symbol, name, charge, mass, color
CERN_PARTICLES = {
    'p': {'name': 'Proton', 'charge': 1, 'mass': 0.938, 'color': (1.0, 0.3, 0.3)},
    'p̄': {'name': 'Antiproton', 'charge': -1, 'mass': 0.938, 'color': (0.3, 1.0, 0.3)},
    'Pb': {'name': 'Lead Ion', 'charge': 82, 'mass': 207.2, 'color': (0.7, 0.7, 0.7)},
    'e-': {'name': 'Electron', 'charge': -1, 'mass': 0.000511, 'color': (0.2, 0.2, 1.0)},
    'e+': {'name': 'Positron', 'charge': 1, 'mass': 0.000511, 'color': (1.0, 0.2, 0.2)},
}

# Collision types
COLLISION_MODES = {
    'fusion': {'name': 'Nuclear Fusion', 'description': 'Low energy nuclear fusion reactions (keV range)'},
    'pp': {'name': 'Proton-Proton', 'description': 'Standard LHC collision mode (13.6 TeV)'},
    'PbPb': {'name': 'Lead-Lead', 'description': 'Heavy ion collision mode (5.36 TeV/nucleon)'},
    'pPb': {'name': 'Proton-Lead', 'description': 'Asymmetric collision mode (8.16 TeV)'},
    'ee': {'name': 'Electron-Positron', 'description': 'Precision physics (future ILC mode)'}
}

# Periodic table data: symbol, name, atomic number, mass, color
PERIODIC_TABLE = {
    'H': {'name': 'Hydrogen', 'atomic_number': 1, 'mass': 1.008, 'color': (1.0, 1.0, 1.0)},
    'H-2': {'name': 'Deuterium', 'atomic_number': 1, 'neutrons': 1, 'mass': 2.014, 'color': (0.9, 0.9, 1.0)},
    'H-3': {'name': 'Tritium', 'atomic_number': 1, 'neutrons': 2, 'mass': 3.016, 'color': (0.8, 0.8, 1.0)},
    'He': {'name': 'Helium', 'atomic_number': 2, 'mass': 4.0026, 'color': (0.85, 1.0, 1.0)},
    'He-3': {'name': 'Helium-3', 'atomic_number': 2, 'neutrons': 1, 'mass': 3.016, 'color': (0.75, 0.9, 1.0)},
    'Li': {'name': 'Lithium', 'atomic_number': 3, 'mass': 6.94, 'color': (0.8, 0.5, 1.0)},
    'Li-6': {'name': 'Lithium-6', 'atomic_number': 3, 'neutrons': 3, 'mass': 6.015, 'color': (0.7, 0.4, 0.9)},
    'Li-7': {'name': 'Lithium-7', 'atomic_number': 3, 'neutrons': 4, 'mass': 7.016, 'color': (0.65, 0.35, 0.85)},
    'Be': {'name': 'Beryllium', 'atomic_number': 4, 'mass': 9.0122, 'color': (0.76, 1.0, 0.0)},
    'B': {'name': 'Boron', 'atomic_number': 5, 'mass': 10.81, 'color': (1.0, 0.71, 0.71)},
    'B-10': {'name': 'Boron-10', 'atomic_number': 5, 'neutrons': 5, 'mass': 10.013, 'color': (0.9, 0.6, 0.6)},
    'B-11': {'name': 'Boron-11', 'atomic_number': 5, 'neutrons': 6, 'mass': 11.009, 'color': (0.85, 0.55, 0.55)},
    'C': {'name': 'Carbon', 'atomic_number': 6, 'mass': 12.011, 'color': (0.56, 0.56, 0.56)},
    'N': {'name': 'Nitrogen', 'atomic_number': 7, 'mass': 14.007, 'color': (0.19, 0.31, 0.97)},
    'O': {'name': 'Oxygen', 'atomic_number': 8, 'mass': 15.999, 'color': (1.0, 0.05, 0.05)},
    'F': {'name': 'Fluorine', 'atomic_number': 9, 'mass': 18.998, 'color': (0.56, 0.88, 0.31)},
    'Ne': {'name': 'Neon', 'atomic_number': 10, 'mass': 20.180, 'color': (0.7, 0.89, 0.96)},
    'Na': {'name': 'Sodium', 'atomic_number': 11, 'mass': 22.990, 'color': (0.67, 0.36, 0.95)},
    'Mg': {'name': 'Magnesium', 'atomic_number': 12, 'mass': 24.305, 'color': (0.54, 1.0, 0.0)},
    'Al': {'name': 'Aluminum', 'atomic_number': 13, 'mass': 26.982, 'color': (0.75, 0.65, 0.65)},
    'Si': {'name': 'Silicon', 'atomic_number': 14, 'mass': 28.085, 'color': (0.94, 0.78, 0.63)},
    'P': {'name': 'Phosphorus', 'atomic_number': 15, 'mass': 30.974, 'color': (1.0, 0.5, 0.0)},
    'S': {'name': 'Sulfur', 'atomic_number': 16, 'mass': 32.06, 'color': (1.0, 1.0, 0.19)},
    'Cl': {'name': 'Chlorine', 'atomic_number': 17, 'mass': 35.45, 'color': (0.12, 0.94, 0.12)},
    'Ar': {'name': 'Argon', 'atomic_number': 18, 'mass': 39.948, 'color': (0.5, 0.82, 0.89)},
    'K': {'name': 'Potassium', 'atomic_number': 19, 'mass': 39.098, 'color': (0.56, 0.25, 0.83)},
    'Ca': {'name': 'Calcium', 'atomic_number': 20, 'mass': 40.078, 'color': (0.61, 0.9, 0.0)},
    'Fe': {'name': 'Iron', 'atomic_number': 26, 'mass': 55.845, 'color': (0.88, 0.4, 0.2)},
    'U': {'name': 'Uranium', 'atomic_number': 92, 'mass': 238.03, 'color': (0.0, 0.56, 0.0)},
    'U-235': {'name': 'Uranium-235', 'atomic_number': 92, 'neutrons': 143, 'mass': 235.04, 'color': (0.0, 0.46, 0.0)}
}

# Define isotope versions with different neutron counts
ISOTOPES = {
    'H': ['H', 'H-2', 'H-3'],
    'He': ['He', 'He-3'],
    'Li': ['Li', 'Li-6', 'Li-7'],
    'B': ['B', 'B-10', 'B-11'],
    'U': ['U', 'U-235']
}


class FusionCollider3DGUI(QMainWindow):
    """
    Main application window with 3D visualization of fusion collisions
    """
    def __init__(self):
        super().__init__()
        
        print("Initializing FusionCollider3DGUI...")
        
        # Initialize physics engine
        self.physics = NuclearPhysics()
        print("Physics engine initialized")
        
        # Set up UI
        self.init_ui()
        print("UI initialization complete")
        
    def init_ui(self):
        self.setWindowTitle('Advanced Fusion Collider Simulation')
        self.setGeometry(100, 100, 1200, 800)
        print(f"Window geometry set to: {self.geometry().x()}, {self.geometry().y()}, {self.geometry().width()}x{self.geometry().height()}")
        
        # Main layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Split the window into control panel and visualization
        splitter = QSplitter(Qt.Vertical)
        
        # Control panel
        control_panel = self.create_control_panel()
        splitter.addWidget(control_panel)
        
        # Tab widget for different views
        tab_widget = QTabWidget()
        
        # 3D visualization widget
        self.visualizer = CollisionVisualizer3D()
        tab_widget.addTab(self.visualizer, "3D Visualization")
        
        # Reaction data panel
        self.reaction_panel = self.create_reaction_panel()
        tab_widget.addTab(self.reaction_panel, "Reaction Data")
        
        splitter.addWidget(tab_widget)
        
        # Set initial splitter sizes
        splitter.setSizes([200, 600])
        
        # Add splitter to main layout
        main_layout.addWidget(splitter)
        
        # Set the main widget
        self.setCentralWidget(main_widget)
        print("Central widget set")
        
        # Connect signals
        self.visualizer.collision_occurred.connect(self.handle_collision_data)
        print("Signal connections established")
        
    def create_control_panel(self):
        """Create the control panel widget"""
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)
        
        # Collision mode selection
        mode_group = QGroupBox("Collision Mode")
        mode_layout = QVBoxLayout()
        
        self.collision_mode = QComboBox()
        for mode_id, mode_data in COLLISION_MODES.items():
            self.collision_mode.addItem(f"{mode_data['name']} ({mode_id})", mode_id)
        
        self.collision_mode.currentIndexChanged.connect(self.update_collision_mode)
        mode_layout.addWidget(self.collision_mode)
        
        self.mode_description = QLabel(COLLISION_MODES['fusion']['description'])
        mode_layout.addWidget(self.mode_description)
        
        mode_group.setLayout(mode_layout)
        control_layout.addWidget(mode_group)
        
        # Energy scale selection
        energy_layout = QHBoxLayout()
        energy_layout.addWidget(QLabel("Energy Scale:"))
        self.energy_scale = QComboBox()
        self.energy_scale.addItems(["keV", "MeV", "GeV", "TeV"])
        energy_layout.addWidget(self.energy_scale)
        # Connect energy scale change to update function
        self.energy_scale.currentTextChanged.connect(self.update_energy_scale)
        control_layout.addLayout(energy_layout)
        
        # Atom selection group - for fusion mode
        self.atom_group = QGroupBox("Select Atoms")
        atom_layout = QGridLayout()
        
        # First atom
        atom_layout.addWidget(QLabel("First Atom:"), 0, 0)
        self.atom1_element = QComboBox()
        for symbol in sorted(PERIODIC_TABLE.keys()):
            if '-' not in symbol:  # Only show base elements in first dropdown
                self.atom1_element.addItem(f"{symbol} - {PERIODIC_TABLE[symbol]['name']}", symbol)
        atom_layout.addWidget(self.atom1_element, 0, 1)
        
        self.atom1_isotope = QComboBox()
        atom_layout.addWidget(self.atom1_isotope, 0, 2)
        
        # Second atom
        atom_layout.addWidget(QLabel("Second Atom:"), 1, 0)
        self.atom2_element = QComboBox()
        for symbol in sorted(PERIODIC_TABLE.keys()):
            if '-' not in symbol:  # Only show base elements in first dropdown
                self.atom2_element.addItem(f"{symbol} - {PERIODIC_TABLE[symbol]['name']}", symbol)
        atom_layout.addWidget(self.atom2_element, 1, 1)
        
        self.atom2_isotope = QComboBox()
        atom_layout.addWidget(self.atom2_isotope, 1, 2)
        
        # Connect element selection to isotope update
        self.atom1_element.currentIndexChanged.connect(self.update_atom1_isotopes)
        self.atom2_element.currentIndexChanged.connect(self.update_atom2_isotopes)
        
        # Initial isotope population
        self.update_atom1_isotopes()
        self.update_atom2_isotopes()
        
        self.atom_group.setLayout(atom_layout)
        control_layout.addWidget(self.atom_group)
        
        # Collision parameters
        param_group = QGroupBox("Collision Parameters")
        param_layout = QGridLayout()
        
        # Energy slider
        self.energy_param_label = QLabel("Collision Energy (keV):")
        param_layout.addWidget(self.energy_param_label, 0, 0)
        self.energy_slider = QSlider(Qt.Horizontal)
        self.energy_slider.setMinimum(1)
        self.energy_slider.setMaximum(1000)
        self.energy_slider.setValue(100)
        self.energy_slider.setTickPosition(QSlider.TicksBelow)
        self.energy_slider.setTickInterval(100)
        param_layout.addWidget(self.energy_slider, 0, 1)
        
        self.energy_label = QLabel("100 keV")
        param_layout.addWidget(self.energy_label, 0, 2)
        self.energy_slider.valueChanged.connect(self.update_energy_label)
        
        # Approach angle
        param_layout.addWidget(QLabel("Approach Angle (°):"), 1, 0)
        self.angle_slider = QSlider(Qt.Horizontal)
        self.angle_slider.setMinimum(0)
        self.angle_slider.setMaximum(180)
        self.angle_slider.setValue(180)  # Head-on collision
        self.angle_slider.setTickPosition(QSlider.TicksBelow)
        self.angle_slider.setTickInterval(45)
        param_layout.addWidget(self.angle_slider, 1, 1)
        
        self.angle_label = QLabel("180°")
        param_layout.addWidget(self.angle_label, 1, 2)
        self.angle_slider.valueChanged.connect(self.update_angle_label)
        
        param_group.setLayout(param_layout)
        control_layout.addWidget(param_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("Start Collision")
        self.start_button.clicked.connect(self.start_simulation)
        button_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_simulation)
        button_layout.addWidget(self.stop_button)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_simulation)
        button_layout.addWidget(self.reset_button)
        
        # Add Instructions button to the button layout with fixed width
        instructions_button = QPushButton("Instructions")
        instructions_button.clicked.connect(self.show_instructions)
        instructions_button.setFixedWidth(100)  # Set a fixed width that fits the text
        button_layout.addWidget(instructions_button)
        
        control_layout.addLayout(button_layout)
        
        # Particle selection group - for CERN modes
        self.particle_group = QGroupBox("Select Particles")
        particle_layout = QGridLayout()
        
        # First particle
        particle_layout.addWidget(QLabel("First Particle:"), 0, 0)
        self.particle1 = QComboBox()
        for symbol, data in CERN_PARTICLES.items():
            self.particle1.addItem(f"{symbol} - {data['name']}", symbol)
        particle_layout.addWidget(self.particle1, 0, 1)
        
        # Second particle
        particle_layout.addWidget(QLabel("Second Particle:"), 1, 0)
        self.particle2 = QComboBox()
        for symbol, data in CERN_PARTICLES.items():
            self.particle2.addItem(f"{symbol} - {data['name']}", symbol)
        particle_layout.addWidget(self.particle2, 1, 1)
        
        self.particle_group.setLayout(particle_layout)
        control_layout.addWidget(self.particle_group)
        self.particle_group.setVisible(False)  # Hide initially
        
        # Add a spacer at the bottom
        control_layout.addStretch(1)
        
        # Set initial mode
        self.update_collision_mode()
        
        return control_widget
        
    def update_collision_mode(self):
        """Update UI based on selected collision mode"""
        mode_id = self.collision_mode.currentData()
        self.mode_description.setText(COLLISION_MODES[mode_id]['description'])
        
        # Show/hide appropriate controls based on mode
        if mode_id == 'fusion':
            self.atom_group.setVisible(True)
            self.particle_group.setVisible(False)
            self.energy_scale.setCurrentText("keV")
        else:
            self.atom_group.setVisible(False)
            self.particle_group.setVisible(True)
            self.energy_scale.setCurrentText("TeV")
        
    def create_reaction_panel(self):
        """Create the reaction data panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Reaction information
        info_group = QGroupBox("Reaction Information")
        info_layout = QVBoxLayout()
        
        self.reaction_text = QTextEdit()
        self.reaction_text.setReadOnly(True)
        info_layout.addWidget(self.reaction_text)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Particle emissions
        emission_group = QGroupBox("Particle Emissions")
        emission_layout = QVBoxLayout()
        
        self.emission_text = QTextEdit()
        self.emission_text.setReadOnly(True)
        emission_layout.addWidget(self.emission_text)
        
        emission_group.setLayout(emission_layout)
        layout.addWidget(emission_group)
        
        # Energy output
        energy_group = QGroupBox("Energy Output")
        energy_layout = QVBoxLayout()
        
        self.energy_text = QTextEdit()
        self.energy_text.setReadOnly(True)
        energy_layout.addWidget(self.energy_text)
        
        energy_group.setLayout(energy_layout)
        layout.addWidget(energy_group)
        
        return panel
        
    def update_atom1_isotopes(self):
        """Update available isotopes for first atom"""
        element = self.atom1_element.currentData()
        self.atom1_isotope.clear()
        
        if element in ISOTOPES:
            for isotope in ISOTOPES[element]:
                self.atom1_isotope.addItem(f"{isotope} - {PERIODIC_TABLE[isotope]['name']}", isotope)
        else:
            self.atom1_isotope.addItem(f"{element} - {PERIODIC_TABLE[element]['name']}", element)
            
    def update_atom2_isotopes(self):
        """Update available isotopes for second atom"""
        element = self.atom2_element.currentData()
        self.atom2_isotope.clear()
        
        if element in ISOTOPES:
            for isotope in ISOTOPES[element]:
                self.atom2_isotope.addItem(f"{isotope} - {PERIODIC_TABLE[isotope]['name']}", isotope)
        else:
            self.atom2_isotope.addItem(f"{element} - {PERIODIC_TABLE[element]['name']}", element)
            
    def update_energy_scale(self):
        """Update UI elements when energy scale changes"""
        scale = self.energy_scale.currentText()
        
        # Update the parameter label
        self.energy_param_label.setText(f"Collision Energy ({scale}):")
        
        # Update the value label
        value = self.energy_slider.value()
        self.energy_label.setText(f"{value} {scale}")
        
        # Update collision mode if needed
        mode_id = self.collision_mode.currentData()
        if mode_id == 'fusion' and scale != "keV":
            # Fusion typically uses keV, so suggest switching back
            print(f"Note: Fusion reactions typically use keV energy scale")
        elif mode_id != 'fusion' and scale == "keV":
            # CERN collisions typically use higher energies
            print(f"Note: {COLLISION_MODES[mode_id]['name']} typically uses higher energy scales")
    
    def update_energy_label(self):
        """Update the energy label text"""
        value = self.energy_slider.value()
        scale = self.energy_scale.currentText()
        self.energy_label.setText(f"{value} {scale}")
        
    def update_angle_label(self):
        """Update the angle label text"""
        value = self.angle_slider.value()
        self.angle_label.setText(f"{value}°")
        
    def start_simulation(self):
        """Start the collision simulation"""
        print("Starting simulation...")
        
        # Get collision mode
        mode_id = self.collision_mode.currentData()
        
        # Get energy scale
        energy_scale = self.energy_scale.currentText()
        energy_value = self.energy_slider.value()
        
        # Convert energy to appropriate units for calculations
        if energy_scale == "keV":
            energy = energy_value * 1e3  # keV to eV
        elif energy_scale == "MeV":
            energy = energy_value * 1e6  # MeV to eV
        elif energy_scale == "GeV":
            energy = energy_value * 1e9  # GeV to eV
        elif energy_scale == "TeV":
            energy = energy_value * 1e12  # TeV to eV
        
        # Get angle
        angle_deg = self.angle_slider.value()
    
        if mode_id == 'fusion':
            # Fusion mode - use atoms
            isotope1 = self.atom1_isotope.currentData()
            isotope2 = self.atom2_isotope.currentData()
            
            if not isotope1 or not isotope2:
                print("Error: No isotopes selected")
                return
                
            print(f"Selected isotopes: {isotope1} and {isotope2}")
                
            # Get atom data
            atom1_data = PERIODIC_TABLE[isotope1]
            atom2_data = PERIODIC_TABLE[isotope2]
            
            # For fusion, use keV directly
            energy_keV = energy_value if energy_scale == "keV" else energy / 1000
        else:
            # CERN mode - use particles
            particle1 = self.particle1.currentData()
            particle2 = self.particle2.currentData()
            
            if not particle1 or not particle2:
                print("Error: No particles selected")
                return
                
            print(f"Selected particles: {particle1} and {particle2}")
                
            # Get particle data
            atom1_data = CERN_PARTICLES[particle1]
            atom2_data = CERN_PARTICLES[particle2]
            
            # For CERN collisions, use TeV
            energy_keV = energy / 1e9  # Convert to keV for visualization scaling
        
        # Calculate initial velocity based on energy and angle
        angle_rad = np.radians(angle_deg)
        velocity_scale = energy_keV / 100  # Scale factor for visualization
    
        # Set up particles for 3D visualization
        if mode_id == 'fusion':
            # Fusion mode - use atoms
            atoms_3d = [
                {
                    'symbol': isotope1,
                    'atomic_number': atom1_data['atomic_number'],
                    'neutrons': atom1_data.get('neutrons', atom1_data['atomic_number']),
                    'position': [-2.0, 0.0, 0.0],
                    'velocity': [velocity_scale, 0, 0],
                    'color': atom1_data['color']
                },
                {
                    'symbol': isotope2,
                    'atomic_number': atom2_data['atomic_number'],
                    'neutrons': atom2_data.get('neutrons', atom2_data['atomic_number']),
                    'position': [2.0 * np.cos(angle_rad), 0.0, 2.0 * np.sin(angle_rad)],
                    'velocity': [-velocity_scale * np.cos(angle_rad), 0, -velocity_scale * np.sin(angle_rad)],
                    'color': atom2_data['color']
                }
            ]
        else:
            # CERN mode - use particles
            atoms_3d = [
                {
                    'symbol': particle1,
                    'atomic_number': atom1_data['charge'],  # Use charge as atomic_number for visualization
                    'neutrons': 0,  # Elementary particles don't have neutrons
                    'position': [-2.0, 0.0, 0.0],
                    'velocity': [velocity_scale, 0, 0],
                    'color': atom1_data['color']
                },
                {
                    'symbol': particle2,
                    'atomic_number': atom2_data['charge'],  # Use charge as atomic_number for visualization
                    'neutrons': 0,  # Elementary particles don't have neutrons
                    'position': [2.0 * np.cos(angle_rad), 0.0, 2.0 * np.sin(angle_rad)],
                    'velocity': [-velocity_scale * np.cos(angle_rad), 0, -velocity_scale * np.sin(angle_rad)],
                    'color': atom2_data['color']
                }
            ]
        
        # Set atoms in visualizer
        self.visualizer.set_atoms(atoms_3d)
        
        # Clear reaction data
        self.reaction_text.clear()
        self.emission_text.clear()
        self.energy_text.clear()
    
        if mode_id == 'fusion':
            # Show initial fusion reaction equation
            self.reaction_text.append(f"<b>Initial Reaction:</b><br>{isotope1} + {isotope2} → ?<br>")
            self.reaction_text.append(f"<b>Atomic Numbers:</b> {atom1_data['atomic_number']} + {atom2_data['atomic_number']}<br>")
            self.reaction_text.append(f"<b>Masses:</b> {atom1_data['mass']} u + {atom2_data['mass']} u<br>")
            self.reaction_text.append("<br><i>Collision in progress...</i>")
            
            # Calculate theoretical collision probability
            probability = self.physics.fusion_probability(isotope1, isotope2, energy_keV)
            self.energy_text.append(f"<b>Collision Energy:</b> {energy_value} {energy_scale}<br>")
            self.energy_text.append(f"<b>Theoretical Fusion Probability:</b> {probability:.4%}<br>")
        else:
            # Show CERN collision information
            self.reaction_text.append(f"<b>CERN Collision Mode:</b> {COLLISION_MODES[mode_id]['name']}<br>")
            self.reaction_text.append(f"<b>Particles:</b> {particle1} + {particle2}<br>")
            self.reaction_text.append(f"<b>Charges:</b> {atom1_data['charge']} + {atom2_data['charge']}<br>")
            self.reaction_text.append(f"<b>Masses:</b> {atom1_data['mass']} GeV/c² + {atom2_data['mass']} GeV/c²<br>")
            self.reaction_text.append("<br><i>High-energy collision in progress...</i>")
            
            # Energy information for CERN collisions
            self.energy_text.append(f"<b>Collision Energy:</b> {energy_value} {energy_scale}<br>")
            
            # Calculate center-of-mass energy
            m1 = atom1_data['mass']
            m2 = atom2_data['mass']
            cm_energy = np.sqrt(2 * m1 * m2 + 2 * energy_value * (m1 + m2))
            self.energy_text.append(f"<b>Center-of-Mass Energy:</b> {cm_energy:.2f} {energy_scale}<br>")
        
        # Start simulation
        print("Calling visualizer.start_simulation()")
        self.visualizer.start_simulation()
        print("Simulation started")
        
    def stop_simulation(self):
        """Stop the simulation"""
        self.visualizer.stop_simulation()
        
    def reset_simulation(self):
        """Reset the simulation"""
        self.visualizer.reset_simulation()
        self.reaction_text.clear()
        self.emission_text.clear()
        self.energy_text.clear()
        
    def handle_collision_data(self, data):
        """Handle collision data from visualizer"""
        # Get collision mode
        mode_id = self.collision_mode.currentData()
        energy_value = self.energy_slider.value()
        energy_scale = self.energy_scale.currentText()
        
        if mode_id == 'fusion':
            # Get atoms for fusion mode
            isotope1 = self.atom1_isotope.currentData()
            isotope2 = self.atom2_isotope.currentData()
            energy_keV = energy_value if energy_scale == "keV" else energy_value * 1000
            
            # Simulate fusion reaction using physics engine
            reaction = self.physics.simulate_fusion_reaction(isotope1, isotope2, energy_keV)
            
            if reaction['fusion_occurred']:
                # Update reaction information
                self.reaction_text.clear()
                self.reaction_text.append("<b>Fusion Reaction Occurred!</b><br>")
                self.reaction_text.append(f"<b>Reactants:</b> {isotope1} + {isotope2}<br>")
                self.reaction_text.append(f"<b>Products:</b> {', '.join(reaction['products'])}<br>")
                self.reaction_text.append(f"<b>Probability:</b> {reaction['probability']:.4%}<br>")
                
                # Update particle emissions
                self.emission_text.clear()
                self.emission_text.append("<b>Emitted Particles:</b><br>")
                if 'particles' in reaction and reaction['particles']:
                    for particle in reaction['particles']:
                        if particle == 'n':
                            self.emission_text.append("• Neutron (n)<br>")
                        elif particle == 'p':
                            self.emission_text.append("• Proton (p)<br>")
                        elif particle == 'e':
                            self.emission_text.append("• Electron (e-)<br>")
                        elif particle == 'γ':
                            self.emission_text.append("• Gamma Ray (γ)<br>")
                else:
                    self.emission_text.append("<i>No particles emitted</i><br>")
                
                # Update energy output
                self.energy_text.clear()
                self.energy_text.append(f"<b>Energy Released:</b> {reaction['energy_release']:.3f} MeV<br>")
                energy_joules = reaction['energy_release'] * 1.602176634e-13  # MeV to joules
                self.energy_text.append(f"<b>Energy in Joules:</b> {energy_joules:.3e} J<br>")
                
                # Calculate equivalent energy
                tnt_equivalent = energy_joules / 4.184e9  # Joules to tons of TNT
                self.energy_text.append(f"<b>TNT Equivalent:</b> {tnt_equivalent:.3e} tons<br>")
                
            else:
                # No fusion occurred
                self.reaction_text.clear()
                self.reaction_text.append("<b>No Fusion Reaction Occurred</b><br>")
                self.reaction_text.append("<i>The atoms collided but did not fuse due to insufficient energy or other factors.</i><br>")
                self.reaction_text.append(f"<b>Probability:</b> {reaction['probability']:.4%}<br>")
        else:
            # CERN mode - high energy collision
            particle1 = self.particle1.currentData()
            particle2 = self.particle2.currentData()
            
            # Check if this is a high-energy collision data from visualizer
            if isinstance(data, dict) and 'high_energy' in data:
                # Use the data directly from the visualizer
                self.update_cern_collision_display(data, particle1, particle2, energy_value, energy_scale, mode_id)
            else:
                # Simulate high-energy collision
                reaction = self.simulate_cern_collision(particle1, particle2, energy_value, energy_scale, mode_id)
                self.update_cern_collision_display(reaction, particle1, particle2, energy_value, energy_scale, mode_id)
            
    def update_cern_collision_display(self, result, particle1, particle2, energy_value, energy_scale, mode_id):
        """Update the display with CERN collision results"""
        # Update reaction information
        self.reaction_text.clear()
        self.reaction_text.append(f"<b>High-Energy Collision Results:</b><br>")
        self.reaction_text.append(f"<b>Collision Type:</b> {COLLISION_MODES[mode_id]['name']}<br>")
        self.reaction_text.append(f"<b>Particles:</b> {particle1} + {particle2}<br>")
        self.reaction_text.append(f"<b>Energy:</b> {energy_value} {energy_scale}<br>")
        
        if 'products' in result:
            products = result['products'] if isinstance(result['products'], list) else [result['products']]
            self.reaction_text.append(f"<b>Main Products:</b> {', '.join(products)}<br>")
        
        # Update particle emissions
        self.emission_text.clear()
        self.emission_text.append("<b>Detected Particles:</b><br>")
        
        if 'particles' in result and result['particles']:
            for particle in result['particles']:
                self.emission_text.append(f"• {particle}<br>")
        else:
            self.emission_text.append("<i>Particle data not available</i><br>")
        
        # Update energy output
        self.energy_text.clear()
        self.energy_text.append(f"<b>Total Energy:</b> {energy_value} {energy_scale}<br>")
        
        if 'energy_release' in result:
            self.energy_text.append(f"<b>Energy Converted:</b> {result['energy_release']:.2f} {energy_scale}<br>")
        
        # Calculate luminosity (simplified)
        luminosity = 1e34  # typical LHC luminosity in cm^-2 s^-1
        if mode_id == 'PbPb':
            luminosity = 1e27
        elif mode_id == 'pPb':
            luminosity = 1e29
            
        self.energy_text.append(f"<b>Luminosity:</b> {luminosity:.1e} cm⁻² s⁻¹<br>")
        
    def show_instructions(self):
        """Show application instructions in a dialog"""
        instructions = QDialog(self)
        instructions.setWindowTitle("Application Instructions")
        instructions.setMinimumSize(600, 500)
        
        layout = QVBoxLayout(instructions)
        
        # Create a scroll area for the instructions
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        # Create content widget
        content = QWidget()
        content_layout = QVBoxLayout(content)
        
        # Add instructions text
        instruction_text = QTextEdit()
        instruction_text.setReadOnly(True)
        instruction_text.setHtml("""
        <h2>Fusion Collider Simulation Instructions</h2>
        
        <h3>Overview</h3>
        <p>This application simulates particle collisions, including nuclear fusion reactions and high-energy particle collisions similar to those at CERN. You can configure various parameters to see how they affect collision outcomes.</p>
        
        <h3>Getting Started</h3>
        <ol>
            <li><b>Select a Collision Mode</b> from the dropdown menu at the top:
                <ul>
                    <li><b>Nuclear Fusion</b> - Simulates low-energy fusion reactions between isotopes</li>
                    <li><b>Proton-Proton</b> - Simulates LHC-style high-energy collisions</li>
                    <li><b>Lead-Lead</b> - Simulates heavy ion collisions</li>
                    <li><b>Proton-Lead</b> - Simulates asymmetric collisions</li>
                    <li><b>Electron-Positron</b> - Simulates precision physics collisions</li>
                </ul>
            </li>
            <li><b>Set the Energy Scale</b> appropriate for your collision type:
                <ul>
                    <li><b>keV</b> - For fusion reactions</li>
                    <li><b>MeV</b> - For nuclear physics</li>
                    <li><b>GeV/TeV</b> - For high-energy particle physics</li>
                </ul>
            </li>
        </ol>
        
        <h3>For Fusion Mode</h3>
        <ol>
            <li>Select your desired isotopes from the <b>Select Atoms</b> section</li>
            <li>Adjust the <b>Collision Energy</b> using the slider</li>
            <li>Set the <b>Approach Angle</b> (180° is a head-on collision)</li>
            <li>Click <b>Start Collision</b> to begin the simulation</li>
        </ol>
        
        <h3>For CERN Collision Modes</h3>
        <ol>
            <li>Select particles from the <b>Select Particles</b> section</li>
            <li>Set appropriate energy levels (typically in TeV)</li>
            <li>Adjust the approach angle as needed</li>
            <li>Click <b>Start Collision</b> to begin</li>
        </ol>
        
        <h3>Controls</h3>
        <ul>
            <li><b>Start Collision</b> - Begins the simulation with current parameters</li>
            <li><b>Stop</b> - Pauses the current simulation</li>
            <li><b>Reset</b> - Clears all results and returns to initial state</li>
        </ul>
        
        <h3>Viewing Results</h3>
        <p>Results are displayed in two tabs:</p>
        <ul>
            <li><b>3D Visualization</b> - Shows the collision in 3D space</li>
            <li><b>Reaction Data</b> - Shows detailed information about:
                <ul>
                    <li>Reaction formula and participants</li>
                    <li>Emitted particles</li>
                    <li>Energy released or consumed</li>
                </ul>
            </li>
        </ul>
        
        <h3>Tips</h3>
        <ul>
            <li>Deuterium-Tritium fusion occurs most easily - try it first!</li>
            <li>Higher energies generally increase fusion probability</li>
            <li>The 3D view can be rotated by dragging with the mouse</li>
            <li>Experiment with different isotope combinations to see various results</li>
        </ul>
        """)
        
        content_layout.addWidget(instruction_text)
        scroll.setWidget(content)
        
        layout.addWidget(scroll)
        
        # Add close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(instructions.accept)
        layout.addWidget(close_button)
        
        # Show the dialog
        instructions.exec_()
        
    def simulate_cern_collision(self, particle1, particle2, energy_value, energy_scale, mode_id):
        """Simulate a high-energy CERN-like collision"""
        # This is a simplified simulation for CERN-like collisions
        result = {
            'collision_occurred': True,
            'probability': 0.0,
            'products': [],
            'particles': [],
            'energy_release': 0.0
        }
        
        # Different collision types produce different results
        if mode_id == 'pp':
            # Proton-proton collision
            result['probability'] = 0.8
            result['products'] = ['Various hadrons', 'Leptons']
            result['particles'] = ['π+', 'π-', 'π0', 'K+', 'K-', 'p', 'p̄', 'n', 'n̄', 'e-', 'e+', 'μ-', 'μ+', 'γ']
            result['energy_release'] = energy_value * 0.1  # 10% of collision energy
            
        elif mode_id == 'PbPb':
            # Lead-lead collision (heavy ion)
            result['probability'] = 0.95
            result['products'] = ['Quark-Gluon Plasma', 'Hadrons']
            result['particles'] = ['π+', 'π-', 'π0', 'K+', 'K-', 'p', 'p̄', 'n', 'n̄', 'Λ', 'Λ̄', 'γ']
            result['energy_release'] = energy_value * 0.3  # 30% of collision energy
            
        elif mode_id == 'pPb':
            # Proton-lead collision
            result['probability'] = 0.9
            result['products'] = ['Hadrons', 'Nuclear Fragments']
            result['particles'] = ['π+', 'π-', 'π0', 'K+', 'K-', 'p', 'p̄', 'n', 'n̄', 'γ']
            result['energy_release'] = energy_value * 0.2  # 20% of collision energy
            
        elif mode_id == 'ee':
            # Electron-positron collision
            result['probability'] = 0.99
            result['products'] = ['Z boson', 'W+/W- pairs', 'Photons']
            result['particles'] = ['γ', 'e-', 'e+', 'μ-', 'μ+', 'τ-', 'τ+']
            result['energy_release'] = energy_value * 0.9  # 90% of collision energy
            
        # Update reaction information
        self.reaction_text.clear()
        self.reaction_text.append(f"<b>High-Energy Collision Results:</b><br>")
        self.reaction_text.append(f"<b>Collision Type:</b> {COLLISION_MODES[mode_id]['name']}<br>")
        self.reaction_text.append(f"<b>Energy:</b> {energy_value} {energy_scale}<br>")
        self.reaction_text.append(f"<b>Main Products:</b> {', '.join(result['products'])}<br>")
        
        # Update particle emissions
        self.emission_text.clear()
        self.emission_text.append("<b>Detected Particles:</b><br>")
        for particle in result['particles']:
            self.emission_text.append(f"• {particle}<br>")
        
        # Update energy output
        self.energy_text.clear()
        self.energy_text.append(f"<b>Total Energy:</b> {energy_value} {energy_scale}<br>")
        self.energy_text.append(f"<b>Energy Converted:</b> {result['energy_release']:.2f} {energy_scale}<br>")
        
        # Calculate luminosity (simplified)
        luminosity = 1e34  # typical LHC luminosity in cm^-2 s^-1
        if mode_id == 'PbPb':
            luminosity = 1e27
        elif mode_id == 'pPb':
            luminosity = 1e29
            
        self.energy_text.append(f"<b>Luminosity:</b> {luminosity:.1e} cm⁻² s⁻¹<br>")
        
        return result


if __name__ == '__main__':
    # Initialize GLUT for 3D shapes
    import sys
    print("Starting Fusion Collider application...")
    
    # This is needed for GLUT
    try:
        glutInit(sys.argv)
        print("GLUT initialized successfully")
    except Exception as e:
        print(f"Error initializing GLUT: {e}")
    
    # Create the Qt Application
    app = QApplication(sys.argv)
    print("QApplication created")
    
    # Create and show the main window
    window = FusionCollider3DGUI()
    print("Main window created, size:", window.size().width(), "x", window.size().height())
    window.show()
    print("Window show() called")
    window.raise_()  # Bring window to front
    window.activateWindow()  # Set focus to the window
    
    # Run the event loop
    print("Starting Qt event loop...")
    sys.exit(app.exec_())
