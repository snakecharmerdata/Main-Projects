# particle_data.py
# Contains data structures for the CERN Fusion Collider simulation

# Dictionary of CERN particles with their properties
CERN_PARTICLES = {
    'p': {
        'name': 'Proton',
        'charge': 1,
        'mass': 0.938,  # GeV/c²
        'color': '#FF5733'
    },
    'e': {
        'name': 'Electron',
        'charge': -1,
        'mass': 0.000511,  # GeV/c²
        'color': '#33A1FF'
    },
    'n': {
        'name': 'Neutron',
        'charge': 0,
        'mass': 0.939565,  # GeV/c²
        'color': '#AAAAAA'
    },
    'μ': {
        'name': 'Muon',
        'charge': -1,
        'mass': 0.1057,  # GeV/c²
        'color': '#33FF57'
    },
    'τ': {
        'name': 'Tau',
        'charge': -1,
        'mass': 1.777,  # GeV/c²
        'color': '#9933FF'
    },
    'γ': {
        'name': 'Photon',
        'charge': 0,
        'mass': 0,  # GeV/c²
        'color': '#FFFF33'
    },
    'Z': {
        'name': 'Z Boson',
        'charge': 0,
        'mass': 91.188,  # GeV/c²
        'color': '#33FFFF'
    },
    'W+': {
        'name': 'W+ Boson',
        'charge': 1,
        'mass': 80.379,  # GeV/c²
        'color': '#FF33FF'
    },
    'W-': {
        'name': 'W- Boson',
        'charge': -1,
        'mass': 80.379,  # GeV/c²
        'color': '#FF33AA'
    },
    'H': {
        'name': 'Higgs Boson',
        'charge': 0,
        'mass': 125.10,  # GeV/c²
        'color': '#FFFFFF'
    },
    'Pb': {
        'name': 'Lead Ion',
        'charge': 82,
        'mass': 207.2,  # u (atomic mass units)
        'color': '#555555'
    }
}

# Dictionary of collision modes available in the simulator
COLLISION_MODES = {
    'fusion': {
        'name': 'Nuclear Fusion',
        'description': 'Simulate nuclear fusion reactions between light elements.'
    },
    'pp': {
        'name': 'Proton-Proton',
        'description': 'Simulate high-energy proton-proton collisions as performed at the LHC.'
    },
    'ee': {
        'name': 'Electron-Electron',
        'description': 'Simulate electron-electron collisions for precision electroweak measurements.'
    },
    'PbPb': {
        'name': 'Lead-Lead',
        'description': 'Simulate heavy-ion collisions to create quark-gluon plasma.'
    },
    'pPb': {
        'name': 'Proton-Lead',
        'description': 'Simulate asymmetric collisions between protons and lead ions.'
    }
}

# Periodic table with element properties
PERIODIC_TABLE = {
    'H': {
        'name': 'Hydrogen',
        'atomic_number': 1,
        'mass': 1.008,  # u (atomic mass units)
        'color': '#FFFFFF'
    },
    'D': {
        'name': 'Deuterium',
        'atomic_number': 1,
        'neutrons': 1,
        'mass': 2.014,
        'color': '#EFEFEF'
    },
    'T': {
        'name': 'Tritium',
        'atomic_number': 1,
        'neutrons': 2,
        'mass': 3.016,
        'color': '#E0E0E0'
    },
    'He': {
        'name': 'Helium',
        'atomic_number': 2,
        'mass': 4.0026,
        'color': '#D9FFFF'
    },
    'He-3': {
        'name': 'Helium-3',
        'atomic_number': 2,
        'neutrons': 1,
        'mass': 3.016,
        'color': '#D0FFFF'
    },
    'Li': {
        'name': 'Lithium',
        'atomic_number': 3,
        'mass': 6.94,
        'color': '#CC80FF'
    },
    'Be': {
        'name': 'Beryllium',
        'atomic_number': 4,
        'mass': 9.0122,
        'color': '#C2FF00'
    },
    'B': {
        'name': 'Boron',
        'atomic_number': 5,
        'mass': 10.81,
        'color': '#FFB5B5'
    },
    'C': {
        'name': 'Carbon',
        'atomic_number': 6,
        'mass': 12.011,
        'color': '#909090'
    },
    'N': {
        'name': 'Nitrogen',
        'atomic_number': 7,
        'mass': 14.007,
        'color': '#3050F8'
    },
    'O': {
        'name': 'Oxygen',
        'atomic_number': 8,
        'mass': 15.999,
        'color': '#FF0D0D'
    },
    'F': {
        'name': 'Fluorine',
        'atomic_number': 9,
        'mass': 18.998,
        'color': '#90E050'
    },
    'Ne': {
        'name': 'Neon',
        'atomic_number': 10,
        'mass': 20.180,
        'color': '#B3E3F5'
    },
    'Na': {
        'name': 'Sodium',
        'atomic_number': 11,
        'mass': 22.990,
        'color': '#AB5CF2'
    },
    'Mg': {
        'name': 'Magnesium',
        'atomic_number': 12,
        'mass': 24.305,
        'color': '#8AFF00'
    },
    'Al': {
        'name': 'Aluminum',
        'atomic_number': 13,
        'mass': 26.982,
        'color': '#BFA6A6'
    },
    'Si': {
        'name': 'Silicon',
        'atomic_number': 14,
        'mass': 28.085,
        'color': '#F0C8A0'
    },
    'P': {
        'name': 'Phosphorus',
        'atomic_number': 15,
        'mass': 30.974,
        'color': '#FF8000'
    },
    'S': {
        'name': 'Sulfur',
        'atomic_number': 16,
        'mass': 32.06,
        'color': '#FFFF30'
    },
    'Cl': {
        'name': 'Chlorine',
        'atomic_number': 17,
        'mass': 35.45,
        'color': '#1FF01F'
    },
    'Ar': {
        'name': 'Argon',
        'atomic_number': 18,
        'mass': 39.948,
        'color': '#80D1E3'
    },
    'K': {
        'name': 'Potassium',
        'atomic_number': 19,
        'mass': 39.098,
        'color': '#8F40D4'
    },
    'Ca': {
        'name': 'Calcium',
        'atomic_number': 20,
        'mass': 40.078,
        'color': '#3DFF00'
    },
    'Fe': {
        'name': 'Iron',
        'atomic_number': 26,
        'mass': 55.845,
        'color': '#E06633'
    },
    'Ni': {
        'name': 'Nickel',
        'atomic_number': 28,
        'mass': 58.693,
        'color': '#50D050'
    },
    'Cu': {
        'name': 'Copper',
        'atomic_number': 29,
        'mass': 63.546,
        'color': '#C88033'
    },
    'Zn': {
        'name': 'Zinc',
        'atomic_number': 30,
        'mass': 65.38,
        'color': '#7D80B0'
    },
    'U': {
        'name': 'Uranium',
        'atomic_number': 92,
        'mass': 238.029,
        'color': '#008FFF'
    },
    'Pu': {
        'name': 'Plutonium',
        'atomic_number': 94,
        'mass': 244.0,
        'color': '#006BFF'
    }
}

# Dictionary of isotopes for each element
ISOTOPES = {
    'H': ['H', 'D', 'T'],
    'He': ['He', 'He-3'],
    'Li': ['Li-6', 'Li-7'],
    'B': ['B-10', 'B-11'],
    'C': ['C-12', 'C-13', 'C-14'],
    'N': ['N-14', 'N-15'],
    'O': ['O-16', 'O-17', 'O-18'],
    'U': ['U-235', 'U-238']
}

# Add isotope data to periodic table
PERIODIC_TABLE['Li-6'] = {
    'name': 'Lithium-6',
    'atomic_number': 3,
    'neutrons': 3,
    'mass': 6.015,
    'color': '#CC80FF'
}

PERIODIC_TABLE['Li-7'] = {
    'name': 'Lithium-7',
    'atomic_number': 3,
    'neutrons': 4,
    'mass': 7.016,
    'color': '#CC80FF'
}

PERIODIC_TABLE['B-10'] = {
    'name': 'Boron-10',
    'atomic_number': 5,
    'neutrons': 5,
    'mass': 10.013,
    'color': '#FFB5B5'
}

PERIODIC_TABLE['B-11'] = {
    'name': 'Boron-11',
    'atomic_number': 5,
    'neutrons': 6,
    'mass': 11.009,
    'color': '#FFB5B5'
}

PERIODIC_TABLE['C-12'] = {
    'name': 'Carbon-12',
    'atomic_number': 6,
    'neutrons': 6,
    'mass': 12.000,
    'color': '#909090'
}

PERIODIC_TABLE['C-13'] = {
    'name': 'Carbon-13',
    'atomic_number': 6,
    'neutrons': 7,
    'mass': 13.003,
    'color': '#909090'
}

PERIODIC_TABLE['C-14'] = {
    'name': 'Carbon-14',
    'atomic_number': 6,
    'neutrons': 8,
    'mass': 14.003,
    'color': '#909090'
}

PERIODIC_TABLE['N-14'] = {
    'name': 'Nitrogen-14',
    'atomic_number': 7,
    'neutrons': 7,
    'mass': 14.003,
    'color': '#3050F8'
}

PERIODIC_TABLE['N-15'] = {
    'name': 'Nitrogen-15',
    'atomic_number': 7,
    'neutrons': 8,
    'mass': 15.000,
    'color': '#3050F8'
}

PERIODIC_TABLE['O-16'] = {
    'name': 'Oxygen-16',
    'atomic_number': 8,
    'neutrons': 8,
    'mass': 15.995,
    'color': '#FF0D0D'
}

PERIODIC_TABLE['O-17'] = {
    'name': 'Oxygen-17',
    'atomic_number': 8,
    'neutrons': 9,
    'mass': 16.999,
    'color': '#FF0D0D'
}

PERIODIC_TABLE['O-18'] = {
    'name': 'Oxygen-18',
    'atomic_number': 8,
    'neutrons': 10,
    'mass': 17.999,
    'color': '#FF0D0D'
}

PERIODIC_TABLE['U-235'] = {
    'name': 'Uranium-235',
    'atomic_number': 92,
    'neutrons': 143,
    'mass': 235.044,
    'color': '#008FFF'
}

PERIODIC_TABLE['U-238'] = {
    'name': 'Uranium-238',
    'atomic_number': 92,
    'neutrons': 146,
    'mass': 238.051,
    'color': '#008FFF'
}