
from __future__ import division
import numpy as np
import math
import sympy as sym
import register


# Calculate the distance of 2 points in a 3D system
def dist2points (x1,x2, y1, y2, z1, z2):

    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

    return abs(dist)

# Calculate the slope of a line
def getslope(x1,y1,x2,y2):

    s = (y2 - y1) / (x2 - x1)

    if math.isnan(s):
        s= 0.001

    return s

#Calculate the equation of the curve
def curveequation(points):

    x = points[:, 0]
    y = points[:, 1]

    eq = np.polyfit(x, y, 2)

    return eq

def featureExtraction(shape, registered ):

    # Store coordinates of kpts in np array
    kptsVec = np.empty([44, 2], dtype=int)
    for p in range(44):
        kptsVec[p][0] = shape.part(p).x
        kptsVec[p][1] = shape.part(p).y

    #Measure M1
    M1_1_1 = register.getPointXYZ(registered, kptsVec[12][0], kptsVec[12][1])
    M1_1_2 = register.getPointXYZ(registered, kptsVec[43][0], kptsVec[43][1])
    M1_2_1 = register.getPointXYZ(registered, kptsVec[23][0], kptsVec[23][1])
    M1_2_2 = register.getPointXYZ(registered, kptsVec[4][0], kptsVec[4][1])

    M1 = [dist2points(M1_1_1[0], M1_1_2[0], M1_1_1[1], M1_1_2[1], M1_1_1[2], M1_1_2[2]),
          dist2points(M1_2_1[0], M1_2_2[0], M1_2_1[1], M1_2_2[1], M1_2_1[2], M1_2_2[2])]

    #Measure M2
    M2_1_1 = register.getPointXYZ(registered, kptsVec[1][0], kptsVec[1][1])
    M2_1_2 = register.getPointXYZ(registered, kptsVec[40][0], kptsVec[40][1])
    M2_2_1 = register.getPointXYZ(registered, kptsVec[34][0], kptsVec[34][1])
    M2_2_2 = register.getPointXYZ(registered, kptsVec[3][0], kptsVec[3][1])

    M2 = [dist2points(M2_1_1[0], M2_1_2[0], M2_1_1[1], M2_1_2[1], M2_1_1[2], M2_1_2[2]),
          dist2points(M2_2_1[0], M2_2_2[0], M2_2_1[1], M2_2_2[1], M2_2_1[2], M2_2_2[2])]

   # Measure M3
    M3_1_1 = register.getPointXYZ(registered, kptsVec[12][0], kptsVec[12][1])
    M3_1_2 = register.getPointXYZ(registered, kptsVec[23][0], kptsVec[23][1])
    M3 = dist2points(M3_1_1[0], M3_1_2[0], M3_1_1[1], M3_1_2[1], M3_1_1[2], M3_1_2[2])

    # Measure M4
    M4_1_1 = register.getPointXYZ(registered, kptsVec[12][0], kptsVec[12][1])
    M4_1_2 = register.getPointXYZ(registered, kptsVec[8][0], kptsVec[8][1])
    M4_2_1 = register.getPointXYZ(registered, kptsVec[23][0], kptsVec[23][1])
    M4_2_2 = register.getPointXYZ(registered, kptsVec[17][0], kptsVec[17][1])

    M4 = [dist2points(M4_1_1[0], M4_1_2[0], M4_1_1[1], M4_1_2[1], M4_1_1[2], M4_1_2[2]),
          dist2points(M4_2_1[0], M4_2_2[0], M4_2_1[1], M4_2_2[1], M4_2_1[2], M4_2_2[2])]

    # Measure M5
    M5_1_1 = register.getPointXYZ(registered, kptsVec[42][0], kptsVec[42][1])
    M5_1_2 = register.getPointXYZ(registered, kptsVec[2][0], kptsVec[2][1])
    M5_2_1 = register.getPointXYZ(registered, kptsVec[5][0], kptsVec[5][1])
    M5_2_2 = register.getPointXYZ(registered, kptsVec[7][0], kptsVec[7][1])

    M5 = [dist2points(M5_1_1[0], M5_1_2[0], M5_1_1[1], M5_1_2[1], M5_1_1[2], M5_1_2[2]),
          dist2points(M5_2_1[0], M5_2_2[0], M5_2_1[1], M5_2_2[1], M5_2_1[2], M5_2_2[2])]

    # Measure M6
    M6_1_1 = register.getPointXYZ(registered, kptsVec[42][0], kptsVec[42][1])
    M6_1_2 = register.getPointXYZ(registered, kptsVec[2][0], kptsVec[2][1])
    M6_2_1 = register.getPointXYZ(registered, kptsVec[41][0], kptsVec[41][1])
    M6_2_2 = register.getPointXYZ(registered, kptsVec[43][0], kptsVec[43][1])

    M6 = dist2points(M6_1_1[0], M6_1_2[0], M6_1_1[1], M6_1_2[1], M6_1_1[2], M6_1_2[2]) / \
         dist2points(M6_2_1[0], M6_2_2[0], M6_2_1[1], M6_2_2[1], M6_2_1[2], M6_2_2[2])

    # Measure M7
    M7_1_1 = register.getPointXYZ(registered, kptsVec[8][0], kptsVec[8][1])
    M7_1_2 = register.getPointXYZ(registered, kptsVec[9][0], kptsVec[9][1])
    M7_2_1 = register.getPointXYZ(registered, kptsVec[17][0], kptsVec[17][1])
    M7_2_2 = register.getPointXYZ(registered, kptsVec[16][0], kptsVec[16][1])

    M7 = (dist2points(M7_1_1[0], M7_1_2[0], M7_1_1[1], M7_1_2[1], M7_1_1[2], M7_1_2[2]) +
          dist2points(M7_2_1[0], M7_2_2[0], M7_2_1[1], M7_2_2[1], M7_2_1[2], M7_2_2[2]))/2

    # Measure M8
    M8_1_1 = register.getPointXYZ(registered, kptsVec[9][0], kptsVec[9][1])
    M8_1_2 = register.getPointXYZ(registered, kptsVec[16][0], kptsVec[26][1])

    M8 = dist2points(M8_1_1[0], M8_1_2[0], M8_1_1[1], M8_1_2[1], M8_1_1[2], M8_1_2[2])

   # Measure M9
    sl9_1 = getslope(kptsVec[10][0], kptsVec[10][1], kptsVec[19][0], kptsVec[19][1])
    sl9_2 = getslope(kptsVec[15][0], kptsVec[15][1], kptsVec[21][0], kptsVec[21][1])

    M9 = math.degrees(math.atan((sl9_1 + sl9_2)/(1 + (sl9_1 * sl9_2))))

    if math.isnan(M9):
        M9 = 0.0
    #Measure M10 not taken as not used

    #Measure M11
    M11_1 = register.getPointXYZ(registered, kptsVec[22][0], kptsVec[22][1])
    M11_2 = register.getPointXYZ(registered, kptsVec[34][0], kptsVec[34][1])
    M11_3 = register.getPointXYZ(registered, kptsVec[36][0], kptsVec[36][1])
    M11_4 = register.getPointXYZ(registered, kptsVec[35][0], kptsVec[35][1])
    M11_5 = register.getPointXYZ(registered, kptsVec[27][0], kptsVec[27][1])

    M11 = dist2points(M11_1[0], M11_2[0], M11_1[1], M11_2[1], M11_1[2], M11_2[2]) + \
          dist2points(M11_2[0], M11_3[0], M11_2[1], M11_3[1], M11_2[2], M11_3[2]) + \
          dist2points(M11_3[0], M11_4[0], M11_3[1], M11_4[1], M11_3[2], M11_4[2]) + \
          dist2points(M11_4[0], M11_5[0], M11_4[1], M11_5[1], M11_4[2], M11_5[2])

    #Measure M12
    M12_1 = (kptsVec[22][0], kptsVec[22][1])
    M12_2 = (kptsVec[37][0], kptsVec[37][1])
    M12_3 = (kptsVec[36][0], kptsVec[36][1])
    M12_4 = (kptsVec[35][0], kptsVec[35][1])
    M12_5 = (kptsVec[27][0], kptsVec[27][1])

    points = np.array([M12_1, M12_2, M12_3, M12_4, M12_5])
    equ = curveequation(points)
    x = sym.Symbol('x')
    sl12_1 = sym.diff(equ[0]*x**2 + equ[1]*x + equ[2],x).subs(x, M12_2[0]).doit()
    sl12_2 = getslope(M12_1[0], M12_1[1], M12_2[0], M12_2[1])

    M12 = math.degrees(math.atan((sl12_1 + sl12_2) / (1 + (sl12_1 * sl12_2))))

    if math.isnan(M12):
        M12 = 0.0

    #Measure M13
    M13_1 = register.getPointXYZ(registered, kptsVec[22][0], kptsVec[22][1])
    M13_2 = register.getPointXYZ(registered, kptsVec[27][0], kptsVec[27][1])

    M13 = dist2points(M13_1[0], M13_2[0], M13_1[1], M13_2[1], M13_1[2], M13_2[2])

    #Measure M14
    M14_1 = register.getPointXYZ(registered, kptsVec[32][0], kptsVec[32][1])
    M14_2 = register.getPointXYZ(registered, kptsVec[36][0], kptsVec[36][1])

    M14 = dist2points(M14_1[0], M14_2[0], M14_1[1], M14_2[1], M14_1[2], M14_2[2])

    #Measure M15
    M15_1 = register.getPointXYZ(registered, kptsVec[32][0], kptsVec[32][1])
    M15_2 = register.getPointXYZ(registered, kptsVec[36][0], kptsVec[36][1])
    M15_3 = register.getPointXYZ(registered, kptsVec[22][0], kptsVec[22][1])
    M15_4 = register.getPointXYZ(registered, kptsVec[27][0], kptsVec[27][1])

    M15 = dist2points(M15_1[0], M15_2[0], M15_1[1], M15_2[1], M15_1[2], M15_2[2]) / \
          dist2points(M15_3[0], M15_4[0], M15_3[1], M15_4[1], M15_3[2], M15_4[2])

    # Measure M16
    sl16_1 = getslope(kptsVec[11][0], kptsVec[11][1], kptsVec[22][0], kptsVec[22][1])
    sl16_2 = getslope(kptsVec[14][0], kptsVec[14][1], kptsVec[27][0], kptsVec[27][1])

    M16 = math.degrees(math.atan((sl16_1 + sl16_2)/(1 + (sl16_1 * sl16_2))))

    if math.isnan(M16):
        M16 = 0.0

    # Measure M17
    M17_1_1 = register.getPointXYZ(registered, kptsVec[40][0], kptsVec[40][1])
    M17_1_2 = register.getPointXYZ(registered, kptsVec[22][0], kptsVec[22][1])
    M17_2_1 = register.getPointXYZ(registered, kptsVec[3][0], kptsVec[3][1])
    M17_2_2 = register.getPointXYZ(registered, kptsVec[27][0], kptsVec[27][1])

    M17 = [dist2points(M17_1_1[0], M17_1_2[0], M17_1_1[1], M17_1_2[1], M17_1_1[2], M17_1_2[2]),
           dist2points(M17_2_1[0], M17_2_2[0], M17_2_1[1], M17_2_2[1], M17_2_1[2], M17_2_2[2])]

    # Measure M18
    M18_1_1 = register.getPointXYZ(registered, kptsVec[13][0], kptsVec[13][1])
    M18_1_2 = register.getPointXYZ(registered, kptsVec[22][0], kptsVec[22][1])
    M18_2_1 = register.getPointXYZ(registered, kptsVec[13][0], kptsVec[13][1])
    M18_2_2 = register.getPointXYZ(registered, kptsVec[27][0], kptsVec[27][1])

    M18 = [dist2points(M18_1_1[0], M18_1_2[0], M18_1_1[1], M18_1_2[1], M18_1_1[2], M18_1_2[2]),
           dist2points(M18_2_1[0], M18_2_2[0], M18_2_1[1], M18_2_2[1], M18_2_1[2], M18_2_2[2])]

    #Measure M19
    M19_1 = register.getPointXYZ(registered, kptsVec[25][0], kptsVec[25][1])
    M19_2 = register.getPointXYZ(registered, kptsVec[13][0], kptsVec[13][1])

    M19 = dist2points(M19_1[0], M19_2[0], M19_1[1], M19_2[1], M19_1[2], M19_2[2])

    #Measure M20
    M20_1 = register.getPointXYZ(registered, kptsVec[36][0], kptsVec[36][1])
    M20_2 = register.getPointXYZ(registered, kptsVec[13][0], kptsVec[13][1])

    M20 = dist2points(M20_1[0], M20_2[0], M20_1[1], M20_2[1], M20_1[2], M20_2[2])

    #MY MEASUREMENT FROM THERE ON
    M21_1_1 = register.getPointXYZ(registered, kptsVec[24][0], kptsVec[24][1])
    M21_1_2 = register.getPointXYZ(registered, kptsVec[30][0], kptsVec[30][1])
    M21_2_1 = register.getPointXYZ(registered, kptsVec[25][0], kptsVec[25][1])
    M21_2_2 = register.getPointXYZ(registered, kptsVec[29][0], kptsVec[29][1])
    M21_3_1 = register.getPointXYZ(registered, kptsVec[26][0], kptsVec[26][1])
    M21_3_2 = register.getPointXYZ(registered, kptsVec[28][0], kptsVec[28][1])

    M21 = [dist2points(M21_1_1[0], M21_1_2[0], M21_1_1[1], M21_1_2[1], M21_1_1[2], M21_1_2[2]),
           dist2points(M21_2_1[0], M21_2_2[0], M21_2_1[1], M21_2_2[1], M21_2_1[2], M21_2_2[2]),
           dist2points(M21_3_1[0], M21_3_2[0], M21_3_1[1], M21_3_2[1], M21_3_1[2], M21_3_2[2])]


    measurements_list = [M1[0], M1[1], M2[0], M2[1], M3, M4[0], M4[1], M5[0], M5[1], M6, M7, M8, M9, M11, M12, M13, M14, #17 elements
                         M15, M16, M17[0], M17[1], M18[0], M18[1], M19, M20, M21[0], M21[1], M21[2]]#28 elements total

    return measurements_list
