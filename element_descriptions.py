"""
Detailed descriptions of chemical elements for the 3D Periodic Table Viewer.
This module provides in-depth information about each element's properties,
history, applications, and interesting facts.
"""
from element_atomic_structure import get_atomic_structure_text

# Dictionary of detailed element descriptions
ELEMENT_DESCRIPTIONS = {
    1: """
Hydrogen is the lightest and most abundant chemical element in the universe, 
constituting roughly 75% of all normal matter. It has the symbol H and atomic 
number 1. At standard temperature and pressure, hydrogen is a colorless, 
odorless, tasteless, non-toxic, nonmetallic, highly combustible gas.

Hydrogen plays a particularly important role in acid-base reactions because most 
acid-base reactions involve the exchange of protons (H+ ions) between soluble molecules.
In the universe, hydrogen mainly exists in its plasma state, whose properties are 
quite different from those of atomic hydrogen.

Applications:
- Hydrogen is used in the production of ammonia for fertilizer
- Used as a clean fuel source with only water as a byproduct when burned
- Used in fuel cells to generate electricity
- Liquid hydrogen is used as a rocket fuel
- Used in the chemical industry to make methanol and hydrochloric acid
""",

    2: """
Helium (He) is a colorless, odorless, tasteless, non-toxic, inert, monatomic gas, 
the first in the noble gas group in the periodic table. Its boiling point is the 
lowest among all the elements, and it exists only as a gas except in extreme conditions.

Helium is the second lightest and second most abundant element in the observable 
universe, being present at about 24% of the total elemental mass. It is primarily 
formed by the nuclear fusion of hydrogen in stars.

Applications:
- Helium is used to inflate balloons, blimps, and airships
- Required for cooling superconducting magnets in MRI machines
- Used as a protective gas in growing silicon and germanium crystals
- As a gas mixture for deep-sea divers to prevent nitrogen narcosis
- Used in leak detection due to its high permeability
""",

    6: """
Carbon (C) is a nonmetallic chemical element with atomic number 6. It is one of 
the most abundant elements in the universe, forming a vast number of compounds 
including the complex molecules that make up all known life.

Carbon exists in various allotropic forms, with the most common being graphite 
and diamond. Carbon's ability to form long chains of interconnecting carbon-carbon 
bonds, a property called catenation, enables the existence of nearly ten million 
different carbon compounds.

Applications:
- Essential element in steel production
- Graphite is used in pencils, lubricants, and electrodes
- Diamond is used in cutting tools and jewelry
- Activated carbon is used in filters and adsorption
- Carbon fiber reinforced materials are used in high-performance engineering
- Carbon dating is used to determine the age of archaeological artifacts
""",

    8: """
Oxygen (O) is the chemical element with atomic number 8. It is a member of the 
chalcogen group in the periodic table, a highly reactive nonmetal, and an 
oxidizing agent that readily forms oxides with most elements as well as with 
other compounds.

Oxygen is the third most abundant element in the universe by mass, after hydrogen 
and helium. It makes up almost 21% of Earth's atmosphere by volume and is the 
most abundant element by mass in the Earth's crust.

Applications:
- Essential for respiration in most living organisms
- Used in medical applications for patients with breathing problems
- Used in steel production, welding, and cutting
- Used in wastewater treatment and environmental remediation
- Used in rocket propulsion as a liquid oxidizer
""",

    11: """
Sodium (Na) is a soft, silvery-white, highly reactive metal. Sodium is an alkali 
metal, being in group 1 of the periodic table. It has a single electron in its 
outer shell, which it readily donates, creating a positively charged ion—the Na+ cation.

Sodium's high reactivity makes it rarely found in nature in its elemental form. 
It's instead found in many minerals, most commonly as sodium chloride (table salt).

Applications:
- Sodium chloride (table salt) is essential for human nutrition
- Used in sodium-vapor lamps for efficient street lighting
- Used in nuclear reactors as a coolant
- Important in many chemical industries
- Sodium hydroxide (lye) is used in soap making and as a drain cleaner
""",

    20: """
Calcium (Ca) is a chemical element with atomic number 20. As an alkaline earth 
metal, calcium is a reactive metal that forms a dark oxide-nitride layer when 
exposed to air. It is the fifth most abundant element in Earth's crust and the 
third most abundant metal.

The human body contains more calcium than any other element except oxygen, 
carbon, hydrogen, and nitrogen. Calcium ions play a vital role in neurotransmitter 
release, muscle contraction, and fertilization.

Applications:
- Essential nutrient for building and maintaining bones and teeth
- Calcium carbonate is used in construction materials like cement
- Used in the production of cheese as calcium chloride
- Calcium oxide (quicklime) is used in steelmaking
- Calcium hypochlorite is used as a swimming pool sanitizer
""",

    26: """
Iron (Fe) is a chemical element with atomic number 26. It is a metal that belongs 
to the first transition series and group 8 of the periodic table. It is by mass 
the most common element on Earth, forming much of Earth's outer and inner core.

Iron is abundant in the sun and other stars. In the Earth's crust, iron is the 
fourth most abundant element. Iron is essential for blood production and oxygen 
transport in vertebrates.

Applications:
- The main component of steel, essential for construction and manufacturing
- Cast iron is used for machinery, automotive parts, and cookware
- Wrought iron is used for decorative purposes
- Iron compounds are used as pigments, catalysts, and in medicines
- Iron oxide nanoparticles are used in magnetic storage devices
""",

    29: """
Copper (Cu) is a soft, malleable, and ductile metal with very high thermal and 
electrical conductivity. It has atomic number 29. A freshly exposed surface of 
pure copper has a pinkish-orange color.

Copper is one of the few metals that can occur in nature in a directly usable 
metallic form (native metals). This led to very early human use in several regions, 
from around 8000 BC. Copper, silver, and gold are in group 11 of the periodic table.

Applications:
- Extensively used in electrical wiring and electronics
- Used in plumbing, roofing, and architectural elements
- Copper alloys like brass and bronze have numerous applications
- Used in coinage and decorative art
- Has antimicrobial properties used in healthcare settings
""",

    47: """
Silver (Ag) is a chemical element with atomic number 47. A soft, white, lustrous 
transition metal, it exhibits the highest electrical conductivity, thermal conductivity, 
and reflectivity of any metal.

Silver has long been valued as a precious metal. Silver metal is used in many 
bullion coins, sometimes alongside gold. While it's more abundant than gold, it's 
much less abundant than copper.

Applications:
- Used in jewelry, silverware, and decorative items
- Extensively used in photography before digital imaging
- Used in electrical contacts and conductors
- Silver nanoparticles are used for their antimicrobial properties
- Used in mirrors and solar panels for its high reflectivity
""",

    79: """
Gold (Au) is a chemical element with atomic number 79. It is a bright, slightly 
reddish yellow, dense, soft, malleable, and ductile metal. Chemically, gold is a 
transition metal and a group 11 element.

Gold is resistant to most acids, though it does dissolve in aqua regia, a mixture 
of nitric acid and hydrochloric acid. Gold also dissolves in alkaline solutions 
of cyanide, which are used in mining and electroplating.

Applications:
- Used in jewelry and as a store of value (gold reserves, investment)
- Used in electronics due to its conductivity and corrosion resistance
- Used in aerospace as a reflective coating
- Used in medicine, particularly in dentistry and treatment of rheumatoid arthritis
- Used as a food additive and in luxury cuisine as a decorative ingredient
""",

    92: """
Uranium (U) is a chemical element with atomic number 92. It is a silvery-grey metal 
in the actinide series of the periodic table. Uranium is weakly radioactive because 
all isotopes of uranium are unstable.

Uranium has the highest atomic weight of the naturally occurring elements. Its 
density is about 70% higher than lead's, and slightly lower than gold or tungsten.

Applications:
- The major application of uranium is as fuel in nuclear power plants
- Used in nuclear weapons
- Uranium-238 can be converted into plutonium-239 in breeder reactors
- Depleted uranium is used in armor-piercing projectiles
- Prior to the discovery of radioactivity, uranium was used to color glass yellow
"""
}

# Extend with descriptions for more elements
ELEMENT_DESCRIPTIONS.update({
    3: """
Lithium (Li) is a soft, silvery-white alkali metal with atomic number 3. Under 
standard conditions, it is the lightest metal and the lightest solid element. 
Like all alkali metals, lithium is highly reactive and flammable, and must be 
stored in mineral oil.

Lithium has a low density and is the least dense of all metals. It can float on water, 
though it reacts with water to produce hydrogen gas and lithium hydroxide.

Applications:
- Lithium-ion batteries power mobile phones, laptops, and electric vehicles
- Used in treatment of bipolar disorder and depression
- Lithium stearate is used as an all-purpose high-temperature lubricant
- Used in air conditioning and industrial drying systems
- Lithium hydride is used as a means of storing hydrogen for fuel cells
""",

    7: """
Nitrogen (N) is a chemical element with atomic number 7. At standard temperature 
and pressure, nitrogen is a colorless, odorless, tasteless gas. Nitrogen is a common 
element in the universe, estimated at seventh in total abundance in the Milky Way and 
Solar System.

Nitrogen makes up about 78% of Earth's atmosphere, where it exists as a diatomic 
molecule, N₂. It is an essential element for life, being a constituent of DNA, RNA,
and proteins.

Applications:
- Used to create an inert atmosphere for food packaging, electronics manufacturing
- Liquid nitrogen is used as a refrigerant for extremely low temperatures
- Used in the production of ammonia, which is vital for fertilizers
- Used in the food industry for freezing and food preservation
- Used in the petroleum industry to maintain pressure in oil wells
""",

    13: """
Aluminum (Al) is a chemical element with atomic number 13. It is a silvery-white, 
soft, non-magnetic and ductile metal in the boron group. By mass, aluminum makes up 
about 8% of the Earth's crust, where it is the third most abundant element after 
oxygen and silicon and the most abundant metal.

Because of aluminum's high chemical reactivity, native specimens of the metal are 
rare. Instead, it is found combined in over 270 different minerals.

Applications:
- Widely used in transportation (automobiles, airplanes, trains)
- Used in construction for windows, doors, and building structures
- Extensively used in packaging (cans, foil, food containers)
- Used in electrical transmission lines because of its light weight
- Common in household items from cooking utensils to furniture
""",

    14: """
Silicon (Si) is a chemical element with atomic number 14. It is a hard, brittle 
crystalline solid with a blue-grey metallic lustre, and is a tetravalent metalloid 
and semiconductor. Silicon is the eighth most common element in the universe by mass.

Silicon is an essential element in biology, although only tiny traces are required 
by animals. It is much more important to the biochemistry of plants and microscopic organisms.

Applications:
- The primary component in semiconductor devices and integrated circuits
- Silicon dioxide (silica) is the main constituent of glass
- Silicones are widely used in lubricants, cooking utensils, and medical applications
- Used in photovoltaic cells for solar energy
- Silicon carbide is used as an abrasive and in cutting tools
""",

    15: """
Phosphorus (P) is a chemical element with atomic number 15. Elemental phosphorus 
exists in two major forms, white phosphorus and red phosphorus, but because it is 
highly reactive, phosphorus is never found as a free element on Earth.

Phosphorus is essential for life. It is a component of DNA, RNA, ATP, and phospholipids, 
which form cell membranes. Elemental phosphorus was first isolated from human urine.

Applications:
- Essential component in fertilizers
- Used in manufacturing safety matches
- Used in steel production to improve strength and corrosion resistance
- Used in incendiary weapons and smoke grenades
- Phosphoric acid is used in soft drinks and food additives
""",

    16: """
Sulfur (S) is a chemical element with atomic number 16. It is abundant, multivalent, 
and nonmetallic. Under normal conditions, sulfur atoms form cyclic octatomic molecules 
with a chemical formula S₈.

Elemental sulfur is a bright yellow, crystalline solid at room temperature. Sulfur 
is present in many types of meteorites, and it is an essential element for all life.

Applications:
- Used in the production of sulfuric acid, a fundamental chemical in industry
- Used in the vulcanization of rubber
- Component in black gunpowder
- Used in fungicides and pesticides
- Used in the production of fertilizers
""",

    17: """
Chlorine (Cl) is a chemical element with atomic number 17. It is a yellow-green gas 
at room temperature that is a member of the halogen group of elements. Chlorine has 
the highest electron affinity and the third-highest electronegativity of all the elements.

Chlorine is a powerful oxidant and is used in bleaching and disinfectants. As a common 
disinfectant, chlorine compounds are used in swimming pools to keep them clean and sanitary.

Applications:
- Used in water treatment and sanitation
- Used in the production of paper and textiles as a bleaching agent
- Used in the production of a wide range of products including plastics, solvents, and medicines
- Used as a disinfectant in swimming pools and drinking water
- Important in organic chemistry as a reagent
""",

    19: """
Potassium (K) is a chemical element with atomic number 19. It is a silvery-white metal 
that is soft enough to be cut with a knife with little force. Potassium is the seventh 
most abundant element in the Earth's crust.

In nature, potassium is found only in ionic salts. Potassium ions are necessary for the 
function of all living cells, and are especially important in plant growth.

Applications:
- Essential nutrient for plants and animals
- Potassium chloride is used as a fertilizer
- Used in the production of potassium hydroxide and potassium nitrate
- Used in medicine for treating potassium deficiency
- Potassium compounds are used in soaps and detergents
""",

    82: """
Lead (Pb) is a chemical element with atomic number 82. It is a heavy metal that is 
denser than most common materials. Lead is soft and malleable, and also has a relatively 
low melting point.

Lead has been used by humans for at least 7,000 years, because it is widespread, easy to 
extract, and easy to work with. However, lead is a neurotoxin that accumulates in soft 
tissues and bones.

Applications:
- Historically used in plumbing, construction, and lead-acid batteries
- Used as radiation shielding around X-ray equipment and nuclear reactors
- Used in ammunition
- Used in certain alloys and solders
- Due to toxicity concerns, many applications have been phased out
""",

    83: """
Bismuth (Bi) is a chemical element with atomic number 83. It is a pentavalent post-transition 
metal and one of the heaviest stable elements, similar to lead in physical properties.

Bismuth is the most naturally diamagnetic element, and has one of the lowest values of 
thermal conductivity among metals. It is rarely found in its native form, but is often 
found in minerals.

Applications:
- Used in pharmaceuticals, particularly for treating digestive disorders
- Used in cosmetics as bismuth oxychloride
- Used in low-melting alloys for fire detection and safety devices
- Used in pigments in the paint industry
- Used in nuclear reactors as a carrier for uranium-235 or uranium-233 fuel
""",

    88: """
Radium (Ra) is a chemical element with atomic number 88. It is a radionuclide that occurs 
naturally as a decay product of uranium and thorium. All isotopes of radium are highly radioactive.

Radium was discovered by Marie and Pierre Curie in 1898, who extracted it from uraninite, 
and was frequently used in the early 20th century in cancer treatment and luminous paint.

Applications:
- Historically used in luminous paints for watches, aircraft switches, clocks, and instrument dials
- Previously used in medicine for cancer treatment (now largely replaced by other radioisotopes)
- Used in the production of radon gas for cancer treatment
- Used in radiography in industrial settings
- Due to high radioactivity, most applications have been discontinued
""",

    94: """
Plutonium (Pu) is a radioactive chemical element with atomic number 94. It is an actinide 
metal of silvery-gray appearance that tarnishes when exposed to air. The element normally 
exhibits six allotropes and four oxidation states.

Plutonium was first produced and isolated in December 1940 by a deuteron bombardment of uranium-238. 
It is the element used in several nuclear weapons.

Applications:
- Primary material used in certain types of nuclear weapons
- Used as fuel in some nuclear reactors
- Used in radioisotope thermoelectric generators for space missions
- Plutonium-238 has been used to power heart pacemakers
- Used in research for nuclear physics and materials science
"""
})

# Function to get description by atomic number
def get_element_description(atomic_number):
    """Returns the detailed description for an element by atomic number"""
    description = ELEMENT_DESCRIPTIONS.get(atomic_number, "No detailed description available for this element.")
    
    # Add atomic structure information
    atomic_structure = get_atomic_structure_text(atomic_number)
    
    # Combine the descriptive text with the atomic structure
    return f"{description}\n\n{atomic_structure}"
