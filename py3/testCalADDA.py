# -*- coding: utf-8 -*-
"""
testCalADDA.py

Test a function to calculate the mm/pix for a Soft Imaging Systems
ADDA-II from a measured calibration.

Modifications:

Date        Who                What
----------  ---  -------------------------------------------------------
2016-03-18  JRM  Initial prototype

"""

def calc_adda_mm_per_px(px_per_unit, x_px=1024, unit_fact=1.0e-9):
    """calc_adda_mm_per_px(px_per_unit, x_px=1024, unit_fact=1.0e-9)
    """
    adda_max = 4096 # Max pix size for ADDA-II
    scale_fact = adda_max/x_px
    un_per_px = px_per_unit /scale_fact
    mm_per_px = un_per_px*1000.*unit_fact
    px_per_mm = 1.0/mm_per_px
    return(round(px_per_mm, 3))

print("800X: X= ", calc_adda_mm_per_px(150.92)," Y= ", calc_adda_mm_per_px(148.77))

