"""
Detailed atomic structure information for chemical elements.
This module provides data about the subatomic particles and electronic
configuration of elements for the 3D Periodic Table Viewer.
"""

# Function to generate atomic structure details
def get_atomic_structure(atomic_number, mass_number=None):
    """
    Calculate and return detailed atomic structure information for an element
    
    Parameters:
        atomic_number (int): The element's atomic number
        mass_number (float, optional): The element's mass number, if None will use average mass
        
    Returns:
        dict: A dictionary containing atomic structure details
    """
    from element_list import ELEMENTS_BY_NUMBER
    
    element = ELEMENTS_BY_NUMBER.get(atomic_number)
    if not element:
        return None
    
    # Number of protons equals the atomic number
    protons = atomic_number
    
    # For electrons, in a neutral atom, electrons equals protons
    electrons = protons
    
    # For neutrons, if mass_number is provided, use it, otherwise estimate from mass
    if mass_number:
        neutrons = mass_number - protons
    else:
        # Estimate neutrons from average mass (rounded)
        neutrons = round(element['mass']) - protons
    
    # Generate electron shell configuration
    electron_shells = calculate_electron_shells(atomic_number)
    
    # Format electron configuration into standard notation
    electron_configuration = format_electron_configuration(electron_shells)
    
    return {
        "protons": protons,
        "neutrons": neutrons,
        "electrons": electrons,
        "electron_shells": electron_shells,
        "electron_configuration": electron_configuration,
        "mass_number": round(element['mass']),
        "atomic_mass": element['mass']
    }

def calculate_electron_shells(atomic_number):
    """
    Calculate the electron shell distribution according to the Aufbau principle
    
    Parameters:
        atomic_number (int): The element's atomic number
        
    Returns:
        dict: Dictionary with shells (K, L, M, etc.) and their electrons
    """
    # Max electrons per shell according to 2n² rule
    shells = {
        'K': 2,    # n=1: 2 electrons (1s)
        'L': 8,    # n=2: 8 electrons (2s, 2p)
        'M': 18,   # n=3: 18 electrons (3s, 3p, 3d)
        'N': 32,   # n=4: 32 electrons (4s, 4p, 4d, 4f)
        'O': 32,   # n=5: 32 electrons (5s, 5p, 5d, 5f)
        'P': 18,   # n=6: 18 electrons (6s, 6p, 6d)
        'Q': 8     # n=7: 8 electrons (7s, 7p)
    }
    
    # Special cases and electron filling order adjustments
    special_configs = {
        24: {'K': 2, 'L': 8, 'M': 13, 'N': 1},  # Cr: [Ar] 3d⁵ 4s¹
        29: {'K': 2, 'L': 8, 'M': 18, 'N': 1},  # Cu: [Ar] 3d¹⁰ 4s¹
        41: {'K': 2, 'L': 8, 'M': 18, 'N': 12, 'O': 1},  # Nb
        42: {'K': 2, 'L': 8, 'M': 18, 'N': 13, 'O': 1},  # Mo
        44: {'K': 2, 'L': 8, 'M': 18, 'N': 15, 'O': 1},  # Ru
        45: {'K': 2, 'L': 8, 'M': 18, 'N': 16, 'O': 1},  # Rh
        46: {'K': 2, 'L': 8, 'M': 18, 'N': 18, 'O': 0},  # Pd
        47: {'K': 2, 'L': 8, 'M': 18, 'N': 18, 'O': 1},  # Ag
        # Add more special cases as needed
    }
    
    if atomic_number in special_configs:
        return special_configs[atomic_number]
    
    # Normal filling order
    result = {}
    remaining = atomic_number
    
    for shell, max_electrons in shells.items():
        electrons_in_shell = min(remaining, max_electrons)
        if electrons_in_shell > 0:
            result[shell] = electrons_in_shell
            remaining -= electrons_in_shell
        
        if remaining == 0:
            break
            
    return result

def format_electron_configuration(electron_shells):
    """
    Format electron shell configuration to standard notation
    
    Parameters:
        electron_shells (dict): Dictionary with electron shell distribution
        
    Returns:
        str: Formatted electron configuration
    """
    shell_to_orbitals = {
        'K': ['1s'],
        'L': ['2s', '2p'],
        'M': ['3s', '3p', '3d'],
        'N': ['4s', '4p', '4d', '4f'],
        'O': ['5s', '5p', '5d', '5f'],
        'P': ['6s', '6p', '6d'],
        'Q': ['7s', '7p']
    }
    
    # Orbital capacities
    orbital_capacity = {
        's': 2,
        'p': 6,
        'd': 10,
        'f': 14
    }
    
    # Filling order of orbitals (Aufbau principle)
    orbital_filling_order = [
        '1s', '2s', '2p', '3s', '3p', '4s', '3d', '4p', '5s', '4d', 
        '5p', '6s', '4f', '5d', '6p', '7s', '5f', '6d', '7p'
    ]
    
    # For common notation, we won't generate detailed configurations
    # Just show shell distribution
    parts = []
    for shell, count in electron_shells.items():
        parts.append(f"{shell}: {count}")
    
    return ", ".join(parts)

def get_atomic_structure_text(atomic_number):
    """
    Generate a formatted text description of the element's atomic structure
    
    Parameters:
        atomic_number (int): The element's atomic number
        
    Returns:
        str: A formatted text describing the atomic structure
    """
    structure = get_atomic_structure(atomic_number)
    if not structure:
        return "Atomic structure data not available."
    
    text = f"""
ATOMIC STRUCTURE:
----------------
Protons: {structure['protons']}
Neutrons: {structure['neutrons']}
Electrons: {structure['electrons']}

Mass Number (A): {structure['mass_number']}
Atomic Mass: {structure['atomic_mass']} u

Electron Configuration:
"""
    
    # Add electron shells information
    for shell, count in structure['electron_shells'].items():
        text += f"  Shell {shell}: {count} electrons\n"
    
    return text