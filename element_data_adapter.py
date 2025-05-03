"""
Adapter module to integrate the complete element list with the existing code.
This provides backward compatibility with code that expects the ELEMENT_DATA format.
"""
from element_list import ALL_ELEMENTS, ELEMENT_COLORS

# Convert the list-based representation to the original dictionary format
def create_element_data_dict():
    """
    Create a dictionary of element data in the original format for compatibility
    """
    element_data = {}
    
    for element in ALL_ELEMENTS:
        atomic_number = element["atomic_number"]
        
        # Add electron configuration if it's not in the basic list
        if "electron_configuration" not in element:
            # Use a placeholder for electron_configuration
            element["electron_configuration"] = "See detailed reference"
            
        element_data[atomic_number] = {
            "name": element["name"],
            "symbol": element["symbol"],
            "mass": element["mass"],
            "category": element["category"],
            "electron_configuration": element["electron_configuration"],
            "atomic_number": atomic_number
        }
    
    return element_data

# Create the ELEMENT_DATA dictionary for compatibility with existing code
ELEMENT_DATA = create_element_data_dict()

# This module can be imported instead of the original element_data.py 
# for backward compatibility