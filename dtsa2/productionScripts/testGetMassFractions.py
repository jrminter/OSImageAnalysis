# -*- coding: utf-8 -*-
"""
DTSA-II Script - J. R. Minter - 2016-10-12

testGetMassFractions.py

  Date      Who  Comment
----------  ---  -----------------------------------------------
2016-10-12  JRM  Mass fractions the easy way...

Elapse: 0:00:00.0  ROCPW7ZC5C42

"""

import sys
sys.packageManager.makeJavaPackage("gov.nist.microanalysis.NISTMonte.Gen3", "CharacteristicXRayGeneration3, BremsstrahlungXRayGeneration3,FluorescenceXRayGeneration3, XRayTransport3", None)

import os
import gov.nist.microanalysis.EPQLibrary as epq
import dtsa2.jmGen as jmg

def getMassFractions(compound, elemList, iDigits):
    """"
    getMassFractions(compound, elemList, iDigits)

    A utility function to compute the mass fractions for a compound

    Parameters
    ----------

    compound - string
        The stoichiometry as a molecular formula
    elemList = a list of type epq.element.symbol
        the elements in the compound
    iDigits - integer
        decimal places to round

    Returns
    -------
    A dictionary of {Symbol : mass-fraction}

    Example
    -------
    elements = [epq.Element.Al, epq.Element.Zn, epq.Element.O]
    massFra = getMassFractions("Al2Zn98O100", 5.61, elements, 5)
    """
    mat = material(compound)
    mf = {}
    for el in elemList:
        wf = round(mat.weightFractionU(el, True).doubleValue(), iDigits)
        mf[el.toAbbrev().encode('ascii','ignore')] = wf
    
    return(mf)

elements = [epq.Element.Al, epq.Element.Zn, epq.Element.O]
# AZO-2
# strCmpd = "Al2Zn98O100"
# strName = "AZO-2"

# AZO-2
strCmpd = "Al5Zn95O100"
strName = "AZO-5"

# elements = [epq.Element.Zn, epq.Element.C, epq.Element.O, epq.Element.H]
# elements = [epq.Element.Al, epq.Element.N, epq.Element.O, epq.Element.H]

# test call from jmGen.py v 0.0.7


# strCmpd = "ZnC4O6H10"

# AF2400
# elements = [epq.Element.C, epq.Element.O, epq.Element.F]
# strName = "AF2400"
# strCmpd = "C461O174F748"
# 
# AF1600
# elements = [epq.Element.C, epq.Element.O, epq.Element.F]
# strName = "AF1600"
# strCmpd = "C395O130F660"
#
# PTFE
# elements = [epq.Element.C, epq.Element.F]
# strName = "PTFE"
# strCmpd = "C2F4"
# Fe3O4
# elements = [epq.Element.Fe, epq.Element.O]
# strName = "Fe3O4"
# strCmpd = "Fe3O4"
# TiO2
# elements = [epq.Element.Ti, epq.Element.O]
# strName = "TiO2"
# strCmpd = "TiO2"

# elements = [epq.Element.Zn, epq.Element.O]
# strName = "ZnO"
# strCmpd = "ZnO"


massFra = jmg.getMassFractions(strCmpd, elements, 5)


print(strName, strCmpd, massFra)

