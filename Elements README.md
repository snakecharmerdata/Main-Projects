# 3D Periodic Table Viewer

An interactive 3D application that visualizes all 118 chemical elements, allowing users to explore their atomic structures, properties, and real-world applications. The program renders each element as a 3D atomic model with its electrons and nucleus, while providing comprehensive information about its composition, uses, and significance in a user-friendly interface.

## Features

- **Complete Periodic Table**: Access to all 118 elements with accurate data
- **Interactive 3D Visualization**: View atomic models with nucleus and electron shells
- **Comprehensive Information**: Details on each element's properties, uses, and atomic structure
- **Customizable View**: Rotate, zoom, and auto-rotate the 3D models
- **Educational Content**: In-depth descriptions and atomic structure information

## Screenshots

*[Screenshots would be placed here]*

## Installation

### Prerequisites

- Python 3.7+
- PyQt5
- PyOpenGL
- NumPy

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/3d-periodic-table.git
   cd 3d-periodic-table
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python main.py
   ```

## Usage

- Use the dropdown menu to select different elements
- View element information in the sidebar panel
- Rotate the 3D model using mouse or sliders
- Click "Start Auto-Rotation" for automatic animation
- Zoom in/out using the slider or mouse wheel
- Read detailed descriptions and atomic structure information

## Project Structure

- `main.py`: Application entry point
- `periodic_table_window.py`: Main application window and UI
- `element_3d_view.py`: 3D visualization using OpenGL
- `element_list.py`: Complete dataset of all elements
- `element_data_adapter.py`: Adapter for element data compatibility
- `element_descriptions.py`: Detailed textual descriptions
- `element_atomic_structure.py`: Atomic structure calculations

## Implementation Details

The application is built using:

- **PyQt5** for the user interface
- **PyOpenGL** for 3D rendering
- **NumPy** for numerical calculations

The 3D visualization represents:
- Protons (red) and neutrons (blue) in the nucleus
- Electron shells arranged according to the Bohr model
- Color-coding based on element categories

## License

[Your License Information]

## Acknowledgments

- Periodic Table data from [Data Source]
- Element descriptions compiled from various scientific sources
- Built with inspiration from educational chemistry resources