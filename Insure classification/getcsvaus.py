

def au1(kpts1, kpts2, kpts6, kpts7, fil4):   

    au1 = 0
    
    if (kpts1 < -0.09 and kpts2 > 0.23) or (kpts6 < -0.13 and kpts7 > 0) or fil4 > 0.07:
        au1 = "a1"             # M1, M4 and M22

    return au1


def au2(kpts3, kpts4):        

    au2 = 0

    if kpts3 > 0.01 and kpts4 < 0:    #M2
        au2 = "a2"

    return au2


def au4(kpts1, kpts2, kpts6, kpts7, kpts5, fil5):    
    au4 = 0

    if ((kpts1 < -0.09 and kpts2 > 0.33) or (kpts6 < -0.68 and kpts7 < -0.02)) and (kpts5 < -0.22 or fil5 > 0.01):

        au4 = "a4"  # M1, M4, M3 and M23_1

    return au4


def au5(kpts8, kpts9, kpts10):

    au5 = 0

    if (kpts8 < 0 and kpts9 < 0) and kpts10 > 0:
        au5 = "a5"  #M5, M6

    return au5


def au6(kpts7, kpts8, kpts12, fil1, fil2, fil3):                                    
    #AU NOT IN THE ORIGINAL PAPER EXTRAPOLATED FROM TABLE 4 MEASUREMENT FOR HAPPY
    au6 = 0

    if (kpts7 > 0 and kpts8 < 0) and kpts12 < -0.02 and fil1 < 0 and fil2 < 0 and fil3 < 0:
        au6 = "a6"  #M5, M9, M21_1, M21_2 and M21_3

    return au6


def au7(kpts7, kpts8, kpts9):         

    au7 = 0

    if (kpts7 > 0 and kpts8 > 0.09) and kpts9 > 0.13:
        au7 = "a7" #M5, M6

    return au7


def au9(fil6, fil7, fil8, fil9, fil10, fil11, fil12, kpts5, kpts6, fil5, kpts4, kpts10, kpts11):        
    NW1 = 0
    NW2 = 0

    if fil6 > 0.02:
        NW1 += 1
    if fil7 < -0.01:
        NW1 += 1
    if fil8 < -0.01:
        NW1 += 1

    if fil9 < -0.01:
        NW2 += 1
    if fil10 > 0.05:
        NW2 += 1
    if fil11 < -0.01:
        NW2 += 1
    if fil12 < -0.01:
        NW2 += 1

    if kpts5 < -0.01 and kpts6 < -0.01:
        c1 = 1
    else:
        c1 = 0

    if fil5 > 0.01 or kpts4 < -0.01:
        c2 = 1
    else:
        c2 = 0

    if NW1 >= 2 and NW2 >= 3:
        c3_1 = 1
    else:
        c3_1 = 0

    if NW1 >= 2 and (kpts10 > 0.01 or kpts11 < -0.01):
        c3_2 = 1
    else:
        c3_2 = 0

    if NW2 >= 3 and (kpts10 > 0.01 or kpts11 < -0.01):
        c3_3 = 1
    else:
        c3_3 = 0

    if c1 == c2 == 1 and (c3_1 == 1 or c3_2 == 1 or c3_3 == 1):
        au9 = "a9"
    else:
        au9 = 0

    return au9


def au12(kpts13, kpts14, kpts19, kpts20, kpts18):           
    au12 = 0

    if kpts13 < -0.01 and kpts14 < 0 and (kpts19 < -0.01 and kpts20 < -0.01) and kpts18 < -0.01:
        au12 = "a12"    #M11, M12, M17, M16

    return au12


def au15(kpts16, kpts14, kpts21, kpts22, kpts23):                 
    au15 = 0
    if kpts16 < 0 and kpts14 < -4 and (kpts21 < -0.21 and kpts22 < -0.31) and kpts23 < -0.16:

        au15 = "a15"     #M14, M12, M17, M19

    return au15


def au16(fil1, fil2, fil3):                                
    # AU NOT IN THE ORIGINAL PAPER EXTRAPOLATED FROM TABLE 4 MEASUREMENT FOR DISGUST
    au16 =0
    cl = 0

    if fil1 < -0.18:
        cl += 1

    if fil2 > 0:
        cl += 1

    if fil3 < 0:
        cl += 1

    if cl >= 2:
        au16 = "a16"       #M21_1, M21_2 and M21_3

    return au16


def au20(kpts15):                                           
    # AU NOT IN THE ORIGINAL PAPER EXTRAPOLATED MYSELF
    au20 = 0

    if kpts15 < -0.19:
        au20 = "a20"    #M13

    return au20


def au23(kpts26, kpts27, kpts28):
    # AU NOT IN THE ORIGINAL PAPER EXTRAPOLATED MYSELF
    au23 = 0

    if kpts26 < 0 and kpts27 < 0 and kpts28 < 0:
        au23 = "a23"        #M21

    return au23


def au26(kpts17, kpts25, kpts24):                
    au26 = 0

    if kpts17 < 0 and kpts25 < -0.39 and kpts24 < -0.17:
        au26 = "a26"    #M14, M20, M19

    return au26
