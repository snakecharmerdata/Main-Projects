"""
3D visualization of atomic elements using PyOpenGL
"""
import sys
import math
import numpy as np
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QSurfaceFormat

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
except ImportError:
    print("PyOpenGL not installed properly. Please install it with:")
    print("pip install PyOpenGL PyOpenGL_accelerate")
    sys.exit(1)

from element_data_adapter import ELEMENT_DATA, ELEMENT_COLORS


class Element3DView(QOpenGLWidget):
    """OpenGL widget for rendering 3D atomic models"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set up OpenGL format for better rendering
        fmt = QSurfaceFormat()
        fmt.setSamples(4)  # Antialiasing
        fmt.setDepthBufferSize(24)
        self.setFormat(fmt)
        
        # Initialize rotation values
        self.x_rot = 30
        self.y_rot = 30
        self.z_rot = 0
        self.zoom = 1.0
        
        # Auto-rotation timer
        self.auto_rotation_timer = QTimer(self)
        self.auto_rotation_timer.timeout.connect(self.update_auto_rotation)
        self.auto_rotating = False
        
        # Track mouse for manual rotation
        self.last_pos = None
        self.setMouseTracking(True)
        
        # Current element
        self.current_element = 1  # Start with Hydrogen
        
    def set_element(self, atomic_number):
        """Set the current element to display"""
        self.current_element = atomic_number
        self.update()
        
    def set_x_rotation(self, angle):
        """Set X-axis rotation"""
        self.x_rot = angle
        self.update()
        
    def set_y_rotation(self, angle):
        """Set Y-axis rotation"""
        self.y_rot = angle
        self.update()
        
    def set_z_rotation(self, angle):
        """Set Z-axis rotation"""
        self.z_rot = angle
        self.update()
        
    def set_zoom(self, zoom_factor):
        """Set zoom level"""
        self.zoom = zoom_factor
        self.update()
        
    def start_auto_rotation(self):
        """Start automatic rotation animation"""
        self.auto_rotating = True
        self.auto_rotation_timer.start(30)  # 30ms refresh
        
    def stop_auto_rotation(self):
        """Stop automatic rotation animation"""
        self.auto_rotating = False
        self.auto_rotation_timer.stop()
        
    def update_auto_rotation(self):
        """Update rotation angles for animation"""
        self.y_rot = (self.y_rot + 1) % 360
        self.update()
        
    def reset_view(self):
        """Reset view to default settings"""
        self.x_rot = 30
        self.y_rot = 30
        self.z_rot = 0
        self.zoom = 1.0
        self.update()
        
    def initializeGL(self):
        """Initialize OpenGL settings"""
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_NORMALIZE)
        
        # Set up lighting
        glLightfv(GL_LIGHT0, GL_POSITION, [10, 10, 10, 1])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1])
        
    def resizeGL(self, width, height):
        """Handle window resize events"""
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        
    def paintGL(self):
        """Render the current element"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Adjust view position
        glTranslatef(0, 0, -8.0 / self.zoom)
        
        # Apply rotations
        glRotatef(self.x_rot, 1.0, 0.0, 0.0)
        glRotatef(self.y_rot, 0.0, 1.0, 0.0)
        glRotatef(self.z_rot, 0.0, 0.0, 1.0)
        
        # Render the atomic model
        self.render_element(self.current_element)
        
    def render_element(self, atomic_number):
        """Render the 3D model of the given element"""
        element = ELEMENT_DATA.get(atomic_number)
        if not element:
            return
            
        # Get properties for visualization
        num_protons = atomic_number
        num_neutrons = round(element['mass']) - num_protons
        num_electrons = num_protons  # Neutral atom
        
        # Draw nucleus
        self.draw_nucleus(num_protons, num_neutrons)
        
        # Draw electron orbitals
        self.draw_electron_orbitals(element)
        
        # Draw element information
        self.renderText(-2, -3, -5, f"{element['symbol']} - {element['name']}")
        
    def draw_nucleus(self, protons, neutrons):
        """Draw the nucleus with protons and neutrons"""
        # Draw protons in red
        glColor3f(1.0, 0.0, 0.0)  # Red for protons
        
        # Simple model: arrange particles in a somewhat random but stable pattern
        total_particles = protons + neutrons
        radius = 0.3 * (total_particles ** (1/3))  # Scale based on particle count
        
        # Place protons
        for i in range(protons):
            phi = 3.14159 * (1 + 5**0.5) * i  # Golden angle
            y = 1 - (i / float(total_particles - 1)) * 2 if total_particles > 1 else 0
            r = radius * math.sqrt(1 - y*y)
            x = math.cos(phi) * r
            z = math.sin(phi) * r
            
            glPushMatrix()
            glTranslatef(x * 0.2, y * 0.2, z * 0.2)
            glutSolidSphere(0.08, 10, 10)
            glPopMatrix()
            
        # Draw neutrons in blue
        glColor3f(0.0, 0.0, 1.0)  # Blue for neutrons
        
        # Place neutrons
        for i in range(neutrons):
            phi = 3.14159 * (1 + 5**0.5) * (i + protons)  # Continue the spiral
            y = 1 - ((i + protons) / float(total_particles - 1)) * 2 if total_particles > 1 else 0
            r = radius * math.sqrt(1 - y*y)
            x = math.cos(phi) * r
            z = math.sin(phi) * r
            
            glPushMatrix()
            glTranslatef(x * 0.2, y * 0.2, z * 0.2)
            glutSolidSphere(0.08, 10, 10)
            glPopMatrix()
            
    def draw_electron_orbitals(self, element):
        """Draw electron orbitals based on element's electron configuration"""
        electron_count = element['atomic_number']
        
        # Get the element's group color
        category = element.get('category', 'unknown')
        r, g, b = ELEMENT_COLORS.get(category, (0.7, 0.7, 0.7))
        
        # Set electron color
        glColor3f(r, g, b)
        
        # Electron shells (simplified Bohr model)
        shells = [2, 8, 18, 32, 32, 18, 8]  # Maximum electrons per shell
        
        current_shell = 0
        electrons_remaining = electron_count
        shell_radius = 1.0  # Base radius for first shell
        
        while electrons_remaining > 0 and current_shell < len(shells):
            # Calculate electrons in this shell
            electrons_in_shell = min(electrons_remaining, shells[current_shell])
            electrons_remaining -= electrons_in_shell
            
            # Draw the shell orbit
            glPushMatrix()
            self.draw_orbit(shell_radius)
            glPopMatrix()
            
            # Draw electrons in this shell
            for i in range(electrons_in_shell):
                angle = 2 * math.pi * i / electrons_in_shell
                x = math.cos(angle) * shell_radius
                y = math.sin(angle) * shell_radius
                
                glPushMatrix()
                glTranslatef(x, y, 0)
                glutSolidSphere(0.05, 8, 8)
                glPopMatrix()
                
            # Move to next shell
            current_shell += 1
            shell_radius += 0.5  # Increase radius for next shell
            
    def draw_orbit(self, radius):
        """Draw a circular orbit at specified radius"""
        glBegin(GL_LINE_LOOP)
        segments = 100
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            glVertex3f(math.cos(angle) * radius, math.sin(angle) * radius, 0)
        glEnd()
        
        # Draw another orbit at a different angle for 3D effect
        glRotatef(60, 1, 0, 0)
        glBegin(GL_LINE_LOOP)
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            glVertex3f(math.cos(angle) * radius, math.sin(angle) * radius, 0)
        glEnd()
        
    def mousePressEvent(self, event):
        """Handle mouse press for manual rotation"""
        self.last_pos = event.pos()
        
    def mouseMoveEvent(self, event):
        """Handle mouse movement for manual rotation"""
        if event.buttons() & Qt.LeftButton:
            if self.last_pos:
                dx = event.x() - self.last_pos.x()
                dy = event.y() - self.last_pos.y()
                
                self.y_rot = (self.y_rot + dx) % 360
                self.x_rot = (self.x_rot + dy) % 360
                
                self.update()
            self.last_pos = event.pos()
            
    def wheelEvent(self, event):
        """Handle mouse wheel for zooming"""
        delta = event.angleDelta().y() / 120  # Each "click" is usually 120 units
        self.zoom = max(0.1, min(5.0, self.zoom + delta * 0.1))
        self.update()
        
    def renderText(self, x, y, z, text):
        """Helper method to render text in the 3D scene"""
        # In newer PyQt versions, renderText is no longer available
        # This is a simple workaround - in a real app, you'd use
        # QOpenGLTextureBlitter or other techniques
        pass
