import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QComboBox, 
                             QSlider, QGroupBox, QGridLayout, QTabWidget,
                             QSplitter, QFrame, QSizePolicy, QTextEdit)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor

# Import our custom modules
from physics_engine import NuclearPhysics
from visualization import CollisionVisualizer
from particle_data import CERN_PARTICLES, COLLISION_MODES, PERIODIC_TABLE, ISOTOPES

class CERNFusionColliderGUI(QMainWindow):
    """
    Main application window for CERN Fusion Collider simulation
    """
    def __init__(self):
        super().__init__()
        
        print("Initializing CERN Fusion Collider GUI...")
        
        # Initialize physics engine
        self.physics = NuclearPhysics()
        print("Physics engine initialized")
        
        # Set up UI
        self.init_ui()
        print("UI initialization complete")
        
    def init_ui(self):
        self.setWindowTitle('CERN Fusion Collider Simulation')
        self.setGeometry(100, 100, 1200, 800)
        print(f"Window geometry set to: {self.geometry().x()}, {self.geometry().y()}, {self.geometry().width()}x{self.geometry().height()}")
        
        # Main layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        # Split the window into control panel and visualization
        splitter = QSplitter(Qt.Horizontal)
        
        # Control panel
        control_panel = self.create_control_panel()
        splitter.addWidget(control_panel)
        
        # Tab widget for different views
        tab_widget = QTabWidget()
        
        # Visualization widget
        self.visualizer = CollisionVisualizer()
        tab_widget.addTab(self.visualizer, "Collision Visualization")
        
        # Reaction data panel
        self.reaction_panel = self.create_reaction_panel()
        tab_widget.addTab(self.reaction_panel, "Reaction Data")
        
        splitter.addWidget(tab_widget)
        
        # Set initial splitter sizes (30% controls, 70% visualization)
        splitter.setSizes([300, 700])
        
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
        param_layout.addWidget(QLabel("Collision Energy:"), 0, 0)
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
            
        # Update energy label
        self.update_energy_label()
        
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
            energy_keV = energy_value if energy_scale == "keV" else energy_value * 1000
            
            # Set up particles for visualization
            particles = [
                {
                    'symbol': isotope1,
                    'name': atom1_data['name'],
                    'atomic_number': atom1_data['atomic_number'],
                    'neutrons': atom1_data.get('neutrons', atom1_data['atomic_number']),
                    'mass': atom1_data['mass'],
                    'color': atom1_data['color']
                },
                {
                    'symbol': isotope2,
                    'name': atom2_data['name'],
                    'atomic_number': atom2_data['atomic_number'],
                    'neutrons': atom2_data.get('neutrons', atom2_data['atomic_number']),
                    'mass': atom2_data['mass'],
                    'color': atom2_data['color']
                }
            ]
            
            # Simulate fusion reaction
            reaction = self.physics.simulate_fusion_reaction(isotope1, isotope2, energy_keV)
            
            # Set up visualization
            self.visualizer.set_particles(particles)
            self.visualizer.set_collision_angle(angle_deg)
            self.visualizer.set_energy(energy_value, energy_scale)
            self.visualizer.set_reaction_result(reaction)
            
            # Show initial fusion reaction equation
            self.reaction_text.clear()
            self.reaction_text.append(f"<b>Initial Reaction:</b><br>{isotope1} + {isotope2} → ?<br>")
            self.reaction_text.append(f"<b>Atomic Numbers:</b> {atom1_data['atomic_number']} + {atom2_data['atomic_number']}<br>")
            self.reaction_text.append(f"<b>Masses:</b> {atom1_data['mass']} u + {atom2_data['mass']} u<br>")
            
            # Calculate theoretical collision probability
            probability = self.physics.fusion_probability(isotope1, isotope2, energy_keV)
            self.energy_text.clear()
            self.energy_text.append(f"<b>Collision Energy:</b> {energy_value} {energy_scale}<br>")
            self.energy_text.append(f"<b>Theoretical Fusion Probability:</b> {probability:.4%}<br>")
            
        else:
            # CERN mode - use particles
            particle1 = self.particle1.currentData()
            particle2 = self.particle2.currentData()
            
            if not particle1 or not particle2:
                print("Error: No particles selected")
                return
                
            print(f"Selected particles: {particle1} and {particle2}")
                
            # Get particle data
            p1_data = CERN_PARTICLES[particle1]
            p2_data = CERN_PARTICLES[particle2]
            
            # For CERN collisions, use TeV
            energy_TeV = energy_value if energy_scale == "TeV" else energy_value / 1000
            
            # Set up particles for visualization
            particles = [
                {
                    'symbol': particle1,
                    'name': p1_data['name'],
                    'charge': p1_data['charge'],
                    'mass': p1_data['mass'],
                    'color': p1_data['color']
                },
                {
                    'symbol': particle2,
                    'name': p2_data['name'],
                    'charge': p2_data['charge'],
                    'mass': p2_data['mass'],
                    'color': p2_data['color']
                }
            ]
            
            # Simulate high-energy collision
            collision = self.physics.simulate_high_energy_collision(particle1, particle2, energy_TeV)
            
            # Set up visualization
            self.visualizer.set_particles(particles)
            self.visualizer.set_collision_angle(angle_deg)
            self.visualizer.set_energy(energy_value, energy_scale)
            self.visualizer.set_collision_result(collision)
            
            # Show CERN collision information
            self.reaction_text.clear()
            self.reaction_text.append(f"<b>CERN Collision Mode:</b> {COLLISION_MODES[mode_id]['name']}<br>")
            self.reaction_text.append(f"<b>Particles:</b> {particle1} + {particle2}<br>")
            self.reaction_text.append(f"<b>Charges:</b> {p1_data['charge']} + {p2_data['charge']}<br>")
            self.reaction_text.append(f"<b>Masses:</b> {p1_data['mass']} GeV/c² + {p2_data['mass']} GeV/c²<br>")
            
            # Energy information for CERN collisions
            self.energy_text.clear()
            self.energy_text.append(f"<b>Collision Energy:</b> {energy_value} {energy_scale}<br>")
            
            # Calculate center-of-mass energy
            m1 = p1_data['mass']
            m2 = p2_data['mass']
            cm_energy = np.sqrt(2 * m1 * m2 + 2 * energy_value * (m1 + m2))
            self.energy_text.append(f"<b>Center-of-Mass Energy:</b> {cm_energy:.2f} {energy_scale}<br>")
        
        # Start simulation
        print("Starting visualization...")
        self.visualizer.start_simulation()
        
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
        
        if mode_id == 'fusion':
            # Handle fusion reaction results
            if data['fusion_occurred']:
                # Update reaction information
                self.reaction_text.clear()
                self.reaction_text.append("<b>Fusion Reaction Occurred!</b><br>")
                self.reaction_text.append(f"<b>Reactants:</b> {' + '.join(data['reactants'])}<br>")
                self.reaction_text.append(f"<b>Products:</b> {', '.join(data['products'])}<br>")
                self.reaction_text.append(f"<b>Probability:</b> {data['probability']:.4%}<br>")
                
                # Update particle emissions
                self.emission_text.clear()
                self.emission_text.append("<b>Emitted Particles:</b><br>")
                if 'particles' in data and data['particles']:
                    for particle in data['particles']:
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
                self.energy_text.append(f"<b>Energy Released:</b> {data['energy_release']:.3f} MeV<br>")
                energy_joules = data['energy_release'] * 1.602176634e-13  # MeV to joules
                self.energy_text.append(f"<b>Energy in Joules:</b> {energy_joules:.3e} J<br>")
                
                # Calculate equivalent energy
                tnt_equivalent = energy_joules / 4.184e9  # Joules to tons of TNT
                self.energy_text.append(f"<b>TNT Equivalent:</b> {tnt_equivalent:.3e} tons<br>")
                
            else:
                # No fusion occurred
                self.reaction_text.clear()
                self.reaction_text.append("<b>No Fusion Reaction Occurred</b><br>")
                self.reaction_text.append("<i>The atoms collided but did not fuse due to insufficient energy or other factors.</i><br>")
                self.reaction_text.append(f"<b>Probability:</b> {data['probability']:.4%}<br>")
        else:
            # Handle high-energy collision results
            self.reaction_text.clear()
            self.reaction_text.append(f"<b>High-Energy Collision Results:</b><br>")
            self.reaction_text.append(f"<b>Collision Type:</b> {COLLISION_MODES[mode_id]['name']}<br>")
            
            if 'products' in data:
                products = data['products'] if isinstance(data['products'], list) else [data['products']]
                self.reaction_text.append(f"<b>Main Products:</b> {', '.join(products)}<br>")
            
            # Update particle emissions
            self.emission_text.clear()
            self.emission_text.append("<b>Detected Particles:</b><br>")
            
            if 'particles_produced' in data:
                self.emission_text.append(f"<b>Total particles:</b> {data['particles_produced']}<br><br>")
                
            if 'products' in data and isinstance(data['products'], list):
                for product in data['products'][:10]:  # Show first 10 products
                    self.emission_text.append(f"• {product}<br>")
                if len(data['products']) > 10:
                    self.emission_text.append(f"<i>...and {len(data['products'])-10} more particles</i><br>")
            
            # Update energy output
            self.energy_text.clear()
            energy_value = self.energy_slider.value()
            energy_scale = self.energy_scale.currentText()
            self.energy_text.append(f"<b>Total Energy:</b> {energy_value} {energy_scale}<br>")
            
            if 'energy_released' in data:
                self.energy_text.append(f"<b>Energy Converted:</b> {data['energy_released']:.2f} {energy_scale}<br>")
            
            # Calculate luminosity (simplified)
            luminosity = 1e34  # typical LHC luminosity in cm^-2 s^-1
            if mode_id == 'PbPb':
                luminosity = 1e27
            elif mode_id == 'pPb':
                luminosity = 1e29
                
            self.energy_text.append(f"<b>Luminosity:</b> {luminosity:.1e} cm⁻² s⁻¹<br>")
            
            if 'cross_section_mb' in data:
                self.energy_text.append(f"<b>Cross-section:</b> {data['cross_section_mb']:.2f} mb<br>")


if __name__ == '__main__':
    print("Starting CERN Fusion Collider application...")
    
    # Create the Qt Application
    app = QApplication(sys.argv)
    print("QApplication created")
    
    # Create and show the main window
    window = CERNFusionColliderGUI()
    print("Main window created, size:", window.size().width(), "x", window.size().height())
    window.show()
    print("Window show() called")
    window.raise_()  # Bring window to front
    window.activateWindow()  # Set focus to the window
    
    # Run the event loop
    print("Starting Qt event loop...")
    sys.exit(app.exec_())