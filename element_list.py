"""
Complete list of all periodic table elements with basic properties.
This provides a simpler alternative to the full detailed element data.
"""

# Color mapping for element categories
ELEMENT_COLORS = {
    "noble gas": (0.7, 0.9, 0.9),
    "alkali metal": (0.7, 0.1, 0.1),
    "alkaline earth metal": (0.9, 0.5, 0.1),
    "transition metal": (0.7, 0.7, 0.5),
    "post-transition metal": (0.4, 0.5, 0.6),
    "metalloid": (0.4, 0.6, 0.4),
    "nonmetal": (0.2, 0.8, 0.2),
    "halogen": (0.9, 0.9, 0.1),
    "lanthanide": (0.5, 0.2, 0.9),
    "actinide": (0.5, 0.0, 0.5),
    "unknown": (0.7, 0.7, 0.7)
}

# Complete list of all 118 elements with basic properties
ALL_ELEMENTS = [
    {"atomic_number": 1, "symbol": "H", "name": "Hydrogen", "category": "nonmetal", "mass": 1.008},
    {"atomic_number": 2, "symbol": "He", "name": "Helium", "category": "noble gas", "mass": 4.0026},
    {"atomic_number": 3, "symbol": "Li", "name": "Lithium", "category": "alkali metal", "mass": 6.94},
    {"atomic_number": 4, "symbol": "Be", "name": "Beryllium", "category": "alkaline earth metal", "mass": 9.0122},
    {"atomic_number": 5, "symbol": "B", "name": "Boron", "category": "metalloid", "mass": 10.81},
    {"atomic_number": 6, "symbol": "C", "name": "Carbon", "category": "nonmetal", "mass": 12.011},
    {"atomic_number": 7, "symbol": "N", "name": "Nitrogen", "category": "nonmetal", "mass": 14.007},
    {"atomic_number": 8, "symbol": "O", "name": "Oxygen", "category": "nonmetal", "mass": 15.999},
    {"atomic_number": 9, "symbol": "F", "name": "Fluorine", "category": "halogen", "mass": 18.998},
    {"atomic_number": 10, "symbol": "Ne", "name": "Neon", "category": "noble gas", "mass": 20.180},
    {"atomic_number": 11, "symbol": "Na", "name": "Sodium", "category": "alkali metal", "mass": 22.990},
    {"atomic_number": 12, "symbol": "Mg", "name": "Magnesium", "category": "alkaline earth metal", "mass": 24.305},
    {"atomic_number": 13, "symbol": "Al", "name": "Aluminum", "category": "post-transition metal", "mass": 26.982},
    {"atomic_number": 14, "symbol": "Si", "name": "Silicon", "category": "metalloid", "mass": 28.085},
    {"atomic_number": 15, "symbol": "P", "name": "Phosphorus", "category": "nonmetal", "mass": 30.974},
    {"atomic_number": 16, "symbol": "S", "name": "Sulfur", "category": "nonmetal", "mass": 32.06},
    {"atomic_number": 17, "symbol": "Cl", "name": "Chlorine", "category": "halogen", "mass": 35.45},
    {"atomic_number": 18, "symbol": "Ar", "name": "Argon", "category": "noble gas", "mass": 39.948},
    {"atomic_number": 19, "symbol": "K", "name": "Potassium", "category": "alkali metal", "mass": 39.098},
    {"atomic_number": 20, "symbol": "Ca", "name": "Calcium", "category": "alkaline earth metal", "mass": 40.078},
    {"atomic_number": 21, "symbol": "Sc", "name": "Scandium", "category": "transition metal", "mass": 44.956},
    {"atomic_number": 22, "symbol": "Ti", "name": "Titanium", "category": "transition metal", "mass": 47.867},
    {"atomic_number": 23, "symbol": "V", "name": "Vanadium", "category": "transition metal", "mass": 50.942},
    {"atomic_number": 24, "symbol": "Cr", "name": "Chromium", "category": "transition metal", "mass": 51.996},
    {"atomic_number": 25, "symbol": "Mn", "name": "Manganese", "category": "transition metal", "mass": 54.938},
    {"atomic_number": 26, "symbol": "Fe", "name": "Iron", "category": "transition metal", "mass": 55.845},
    {"atomic_number": 27, "symbol": "Co", "name": "Cobalt", "category": "transition metal", "mass": 58.933},
    {"atomic_number": 28, "symbol": "Ni", "name": "Nickel", "category": "transition metal", "mass": 58.693},
    {"atomic_number": 29, "symbol": "Cu", "name": "Copper", "category": "transition metal", "mass": 63.546},
    {"atomic_number": 30, "symbol": "Zn", "name": "Zinc", "category": "transition metal", "mass": 65.38},
    {"atomic_number": 31, "symbol": "Ga", "name": "Gallium", "category": "post-transition metal", "mass": 69.723},
    {"atomic_number": 32, "symbol": "Ge", "name": "Germanium", "category": "metalloid", "mass": 72.63},
    {"atomic_number": 33, "symbol": "As", "name": "Arsenic", "category": "metalloid", "mass": 74.922},
    {"atomic_number": 34, "symbol": "Se", "name": "Selenium", "category": "nonmetal", "mass": 78.971},
    {"atomic_number": 35, "symbol": "Br", "name": "Bromine", "category": "halogen", "mass": 79.904},
    {"atomic_number": 36, "symbol": "Kr", "name": "Krypton", "category": "noble gas", "mass": 83.798},
    {"atomic_number": 37, "symbol": "Rb", "name": "Rubidium", "category": "alkali metal", "mass": 85.468},
    {"atomic_number": 38, "symbol": "Sr", "name": "Strontium", "category": "alkaline earth metal", "mass": 87.62},
    {"atomic_number": 39, "symbol": "Y", "name": "Yttrium", "category": "transition metal", "mass": 88.906},
    {"atomic_number": 40, "symbol": "Zr", "name": "Zirconium", "category": "transition metal", "mass": 91.224},
    {"atomic_number": 41, "symbol": "Nb", "name": "Niobium", "category": "transition metal", "mass": 92.906},
    {"atomic_number": 42, "symbol": "Mo", "name": "Molybdenum", "category": "transition metal", "mass": 95.95},
    {"atomic_number": 43, "symbol": "Tc", "name": "Technetium", "category": "transition metal", "mass": 98},
    {"atomic_number": 44, "symbol": "Ru", "name": "Ruthenium", "category": "transition metal", "mass": 101.07},
    {"atomic_number": 45, "symbol": "Rh", "name": "Rhodium", "category": "transition metal", "mass": 102.91},
    {"atomic_number": 46, "symbol": "Pd", "name": "Palladium", "category": "transition metal", "mass": 106.42},
    {"atomic_number": 47, "symbol": "Ag", "name": "Silver", "category": "transition metal", "mass": 107.87},
    {"atomic_number": 48, "symbol": "Cd", "name": "Cadmium", "category": "transition metal", "mass": 112.41},
    {"atomic_number": 49, "symbol": "In", "name": "Indium", "category": "post-transition metal", "mass": 114.82},
    {"atomic_number": 50, "symbol": "Sn", "name": "Tin", "category": "post-transition metal", "mass": 118.71},
    {"atomic_number": 51, "symbol": "Sb", "name": "Antimony", "category": "metalloid", "mass": 121.76},
    {"atomic_number": 52, "symbol": "Te", "name": "Tellurium", "category": "metalloid", "mass": 127.60},
    {"atomic_number": 53, "symbol": "I", "name": "Iodine", "category": "halogen", "mass": 126.90},
    {"atomic_number": 54, "symbol": "Xe", "name": "Xenon", "category": "noble gas", "mass": 131.29},
    {"atomic_number": 55, "symbol": "Cs", "name": "Cesium", "category": "alkali metal", "mass": 132.91},
    {"atomic_number": 56, "symbol": "Ba", "name": "Barium", "category": "alkaline earth metal", "mass": 137.33},
    {"atomic_number": 57, "symbol": "La", "name": "Lanthanum", "category": "lanthanide", "mass": 138.91},
    {"atomic_number": 58, "symbol": "Ce", "name": "Cerium", "category": "lanthanide", "mass": 140.12},
    {"atomic_number": 59, "symbol": "Pr", "name": "Praseodymium", "category": "lanthanide", "mass": 140.91},
    {"atomic_number": 60, "symbol": "Nd", "name": "Neodymium", "category": "lanthanide", "mass": 144.24},
    {"atomic_number": 61, "symbol": "Pm", "name": "Promethium", "category": "lanthanide", "mass": 145},
    {"atomic_number": 62, "symbol": "Sm", "name": "Samarium", "category": "lanthanide", "mass": 150.36},
    {"atomic_number": 63, "symbol": "Eu", "name": "Europium", "category": "lanthanide", "mass": 151.96},
    {"atomic_number": 64, "symbol": "Gd", "name": "Gadolinium", "category": "lanthanide", "mass": 157.25},
    {"atomic_number": 65, "symbol": "Tb", "name": "Terbium", "category": "lanthanide", "mass": 158.93},
    {"atomic_number": 66, "symbol": "Dy", "name": "Dysprosium", "category": "lanthanide", "mass": 162.50},
    {"atomic_number": 67, "symbol": "Ho", "name": "Holmium", "category": "lanthanide", "mass": 164.93},
    {"atomic_number": 68, "symbol": "Er", "name": "Erbium", "category": "lanthanide", "mass": 167.26},
    {"atomic_number": 69, "symbol": "Tm", "name": "Thulium", "category": "lanthanide", "mass": 168.93},
    {"atomic_number": 70, "symbol": "Yb", "name": "Ytterbium", "category": "lanthanide", "mass": 173.05},
    {"atomic_number": 71, "symbol": "Lu", "name": "Lutetium", "category": "lanthanide", "mass": 174.97},
    {"atomic_number": 72, "symbol": "Hf", "name": "Hafnium", "category": "transition metal", "mass": 178.49},
    {"atomic_number": 73, "symbol": "Ta", "name": "Tantalum", "category": "transition metal", "mass": 180.95},
    {"atomic_number": 74, "symbol": "W", "name": "Tungsten", "category": "transition metal", "mass": 183.84},
    {"atomic_number": 75, "symbol": "Re", "name": "Rhenium", "category": "transition metal", "mass": 186.21},
    {"atomic_number": 76, "symbol": "Os", "name": "Osmium", "category": "transition metal", "mass": 190.23},
    {"atomic_number": 77, "symbol": "Ir", "name": "Iridium", "category": "transition metal", "mass": 192.22},
    {"atomic_number": 78, "symbol": "Pt", "name": "Platinum", "category": "transition metal", "mass": 195.08},
    {"atomic_number": 79, "symbol": "Au", "name": "Gold", "category": "transition metal", "mass": 196.97},
    {"atomic_number": 80, "symbol": "Hg", "name": "Mercury", "category": "transition metal", "mass": 200.59},
    {"atomic_number": 81, "symbol": "Tl", "name": "Thallium", "category": "post-transition metal", "mass": 204.38},
    {"atomic_number": 82, "symbol": "Pb", "name": "Lead", "category": "post-transition metal", "mass": 207.2},
    {"atomic_number": 83, "symbol": "Bi", "name": "Bismuth", "category": "post-transition metal", "mass": 208.98},
    {"atomic_number": 84, "symbol": "Po", "name": "Polonium", "category": "post-transition metal", "mass": 209},
    {"atomic_number": 85, "symbol": "At", "name": "Astatine", "category": "halogen", "mass": 210},
    {"atomic_number": 86, "symbol": "Rn", "name": "Radon", "category": "noble gas", "mass": 222},
    {"atomic_number": 87, "symbol": "Fr", "name": "Francium", "category": "alkali metal", "mass": 223},
    {"atomic_number": 88, "symbol": "Ra", "name": "Radium", "category": "alkaline earth metal", "mass": 226},
    {"atomic_number": 89, "symbol": "Ac", "name": "Actinium", "category": "actinide", "mass": 227},
    {"atomic_number": 90, "symbol": "Th", "name": "Thorium", "category": "actinide", "mass": 232.04},
    {"atomic_number": 91, "symbol": "Pa", "name": "Protactinium", "category": "actinide", "mass": 231.04},
    {"atomic_number": 92, "symbol": "U", "name": "Uranium", "category": "actinide", "mass": 238.03},
    {"atomic_number": 93, "symbol": "Np", "name": "Neptunium", "category": "actinide", "mass": 237},
    {"atomic_number": 94, "symbol": "Pu", "name": "Plutonium", "category": "actinide", "mass": 244},
    {"atomic_number": 95, "symbol": "Am", "name": "Americium", "category": "actinide", "mass": 243},
    {"atomic_number": 96, "symbol": "Cm", "name": "Curium", "category": "actinide", "mass": 247},
    {"atomic_number": 97, "symbol": "Bk", "name": "Berkelium", "category": "actinide", "mass": 247},
    {"atomic_number": 98, "symbol": "Cf", "name": "Californium", "category": "actinide", "mass": 251},
    {"atomic_number": 99, "symbol": "Es", "name": "Einsteinium", "category": "actinide", "mass": 252},
    {"atomic_number": 100, "symbol": "Fm", "name": "Fermium", "category": "actinide", "mass": 257},
    {"atomic_number": 101, "symbol": "Md", "name": "Mendelevium", "category": "actinide", "mass": 258},
    {"atomic_number": 102, "symbol": "No", "name": "Nobelium", "category": "actinide", "mass": 259},
    {"atomic_number": 103, "symbol": "Lr", "name": "Lawrencium", "category": "actinide", "mass": 266},
    {"atomic_number": 104, "symbol": "Rf", "name": "Rutherfordium", "category": "transition metal", "mass": 267},
    {"atomic_number": 105, "symbol": "Db", "name": "Dubnium", "category": "transition metal", "mass": 268},
    {"atomic_number": 106, "symbol": "Sg", "name": "Seaborgium", "category": "transition metal", "mass": 269},
    {"atomic_number": 107, "symbol": "Bh", "name": "Bohrium", "category": "transition metal", "mass": 270},
    {"atomic_number": 108, "symbol": "Hs", "name": "Hassium", "category": "transition metal", "mass": 277},
    {"atomic_number": 109, "symbol": "Mt", "name": "Meitnerium", "category": "unknown", "mass": 278},
    {"atomic_number": 110, "symbol": "Ds", "name": "Darmstadtium", "category": "unknown", "mass": 281},
    {"atomic_number": 111, "symbol": "Rg", "name": "Roentgenium", "category": "unknown", "mass": 282},
    {"atomic_number": 112, "symbol": "Cn", "name": "Copernicium", "category": "transition metal", "mass": 285},
    {"atomic_number": 113, "symbol": "Nh", "name": "Nihonium", "category": "unknown", "mass": 286},
    {"atomic_number": 114, "symbol": "Fl", "name": "Flerovium", "category": "unknown", "mass": 289},
    {"atomic_number": 115, "symbol": "Mc", "name": "Moscovium", "category": "unknown", "mass": 290},
    {"atomic_number": 116, "symbol": "Lv", "name": "Livermorium", "category": "unknown", "mass": 293},
    {"atomic_number": 117, "symbol": "Ts", "name": "Tennessine", "category": "unknown", "mass": 294},
    {"atomic_number": 118, "symbol": "Og", "name": "Oganesson", "category": "unknown", "mass": 294}
]

# Convert list to dictionary for easier lookup by atomic number
ELEMENTS_BY_NUMBER = {element["atomic_number"]: element for element in ALL_ELEMENTS}

# Helper function to get a specific element by atomic number
def get_element(atomic_number):
    """Get element data by atomic number"""
    return ELEMENTS_BY_NUMBER.get(atomic_number)

# Helper function to get elements by category
def get_elements_by_category(category):
    """Get all elements in a specific category"""
    return [element for element in ALL_ELEMENTS if element["category"] == category]

# Helper function to get element by symbol
def get_element_by_symbol(symbol):
    """Get element data by symbol"""
    for element in ALL_ELEMENTS:
        if element["symbol"] == symbol:
            return element
    return None