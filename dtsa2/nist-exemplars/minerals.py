# -*- coding: utf-8 -*-
# DTSA-II/NISTMonte script - Nicholas W. M. Ritchie - 29-May-2010

"""A simple script to add some basic minerals to the material database."""

import dtsa2.dbTools as dbt

minerals = {
    'Stibnite': material("Sb2S3",4.55),
    'Galena': material("PbS",7.5),
    'Calcite': material('CaCO3', 2.7),
    'Wulfenite': material('PbMoO4', 6.75),
    # ( 'Wolframite': '(Fe,Mn)WO4',
    'Chromite': material('FeCr2O4',4.6),
    'Quartz': material('SiO2', 2.65),
    'Geothite': material('FeO(OH)', 3.8),
    'Anhydrite': material('CaSO4', 2.95),
    'Pyrite': material('FeS2'),
    'Sphalerite': material('ZnS',4.0),
    'Chalcopyrite': material('CuFeS2',4.2),
    'Bornite': material('Cu5FeS4',5.05),
    'Cinnibar': material('HgS',8.1),
    'Realgar': material('AsS', 3.5),
    'Spinel': material('MgAl2O4', 3.8),
    'Hematite': material('Fe2O3',5.1),
    'Magnetite': material('Fe3O4', 5.2),
    'Ilmenite': material('FeTiO3', 4.75),
    'Corundum': material('Al2O3', 4.0),
    'Cassiterite': material('SnO2', 6.95),
    'Rutile': material('TiO2', 4.3),
    'Uraninite': material('UO3', 8.4),
    'Fluorite': material('CaF2', 3.2),
    'Halite': material('NaCl', 2.15),
    'Dolomite': material('CaMg(CO3)2',2.85),
    'Rhodochrosite': material('MnCO3',3.55),
    'Malachite': material('Cu2CO3(OH)2', 3.95),
    'Azurite': material('Cu3(CO3)2(OH)2', 3.85),
    'Borax': material('Na2B4O5(OH)4(H2O)8', 1.7),
    'Chlorapatite': material('Ca5(PO4)3Cl',3.15),
    'Fluorapatite': material('Ca5(PO4)3F',3.15),
    'Hydroxyapatite': material('Ca5(PO4)3(OH)',3.15),
    'Turquoise': material('CuAl6(PO4)4(OH)8(H2O)5',2.7),
    'Carnotite': material('K2(UO2)2(VO4)2(H2O)3', 4.75),
    'Zircon': material('ZrSiO4', 4.65),
    'Andalusite': material('Al2SiO5', 3.15),
    'Kyanute': material('Al2SiO5', 3.6),
    'Topaz': material('Al2SiO4(OH)2', 3.55),
    'Beryl': material('Be3Al2Si6O18', 2.7),
    'Talc': material('Mg3Si4O10(OH)2', 2.7) }

print 'Adding %d minerals to the database' % len(minerals)
for name, comp in minerals.iteritems():
    comp.setName(name)
    dbt.addStandard(comp)

print 'Validating %d minerals' % len(minerals)
for name, comp in minerals.iteritems():
    print material(name).descriptiveString(False)