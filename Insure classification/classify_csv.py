
import csv
import getcsvausd2s2
import getcsvaus_or_ratio
import assign_fes
from sklearn.metrics import confusion_matrix
from collections import Counter
import numpy as np
from scipy.stats import itemfreq
import time

csv_files = ["measurements_d2s2.csv"]
txt_files = ["test 29-03-2021/resd2s2.txt"]
idx = 0

for idx in range(2):

    start_time = time.time()

    with open(csv_files[idx]) as meas:
        csv_reader = csv.reader(meas, delimiter=",")
        cnt = 0
        all_faces_pred_labels = []
        all_faces_act_labels = []
        pred1_labels = []
      	pred2_labels = []
        act1_labels = []
        act2_labels = []

        # Stores the missing AUs for the FEs
        anger = []
        disgust = []
        fear = []
        happy = []
        sad = []
        surprise = []

        an = 0
        di = 0
        fe = 0
        ha = 0
        sa = 0
        su = 0

        for row in csv_reader:

            if cnt > 1:
                for i in range(len(row)):
                    if i > 2:
                        row[i] = float(row[i])

                #print row
                if idx == 0:
                    # a1 = getcsvausd1s2.au1(row[15], row[16], row[20], row[21], row[6])
                    # a2 = getcsvausd1s2.au2(row[17], row[18])
                    # a4 = getcsvausd1s2.au4(row[15], row[16], row[20], row[21], row[19], row[7])
                    #a5 = getcsvausd1s1.au5(row[22], row[23], row[24])
                    a6 = getcsvausd2s2.au6(row[22], row[23], row[27], row[3], row[4], row[5])
                    # a7 = getcsvausd1s2.au7(row[22], row[23], row[24])
                    a9 = getcsvausd2s2.au9(row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[20],row[21], row[7], row[19], row[25], row[26])
                    a12 = getcsvausd2s2.au12(row[28], row[29], row[34], row[35], row[33])
                    a15 = getcsvausd2s2.au15(row[31], row[29], row[36], row[37], row[38])
                    a16 = getcsvausd2s2.au16(row[3], row[4], row[5])
                    # a20 = getcsvausd1s2.au20(row[30])
                    # # a23 = getcsvaus.au23(row[40], row[41], row[42])
                    # a26 = getcsvausd1s2.au26(row[31], row[39], row[38])
                    a0 = "a0"   #Dummy value

                    # res = [a0, a1, a2, a4, a6, a7, a9, a12, a15, a16, a20, a26]
                    res = [a0, a6, a9, a12, a15, a16]
                    
                    prediction = assign_fes.get_FE(res)
                    if prediction == 6:
                        print "Allarm"
                  
                else:

                    a1_or = getcsvaus_or_ratio.au1(row[15], row[16], row[20], row[21], row[6])
                    a2_or = getcsvaus_or_ratio.au2(row[17], row[18])
                    a4_or = getcsvaus_or_ratio.au4(row[15], row[16], row[20], row[21], row[19], row[7])
                    a5_or = getcsvaus_or_ratio.au5(row[22], row[23], row[24])
                    a6_or = getcsvaus_or_ratio.au6(row[22], row[23], row[27], row[3], row[4], row[5])
                    a9_or = getcsvaus_or_ratio.au9(row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[20],
                                                   row[21], row[7], row[19], row[25], row[26])
                    a12_or = getcsvaus_or_ratio.au12(row[28], row[29], row[34], row[35], row[33])
                    a15_or = getcsvaus_or_ratio.au15(row[31], row[29], row[36], row[37], row[38])
                    a16_or = getcsvaus_or_ratio.au16(row[3], row[4], row[5])
                    a26_or = getcsvaus_or_ratio.au26(row[31], row[39], row[38])
                    a0_or = "a0"  # Dummy value

                    res = [a0_or, a1_or, a2_or, a4_or, a5_or, a6_or, a9_or, a12_or, a15_or, a16_or, a26_or]
                    prediction = assign_fes.get_FE(res)

                if int(row[2]) == 1 and prediction != 1:
                    anger.append(assign_fes.missing_aus(int(row[2]), res))
                elif int(row[2]) == 2 and prediction != 2:
                    disgust.append(assign_fes.missing_aus(int(row[2]), res))
                elif int(row[2]) == 3 and prediction != 3:
                    fear.append(assign_fes.missing_aus(int(row[2]), res))
                elif int(row[2]) == 4 and prediction != 4:
                    happy.append(assign_fes.missing_aus(int(row[2]), res))
                elif int(row[2]) == 5 and prediction != 5:
                    sad.append(assign_fes.missing_aus(int(row[2]), res))
                elif int(row[2]) == 6 and prediction != 6:
                    surprise.append(assign_fes.missing_aus(int(row[2]), res))



                if int(row[2]) == 1:
                        an = an + 1
                elif int(row[2]) == 2:
                    di = di + 1
                elif int(row[2]) == 3:
                    fe = fe + 1
                elif int(row[2]) == 4:
                    ha = ha + 1
                elif int(row[2]) == 5:
                    sa = sa + 1
                elif int(row[2]) == 6:
                    su = su + 1


                if int(row[2]) != 7:
                    all_faces_pred_labels.append(prediction)
                    all_faces_act_labels.append(int(row[2]))

                if int(row[1]) == 1 and int(row[2]) != 7:
                    if int(row[2]) == 7:
                        print "Error1"
                    pred1_labels.append(prediction)
                    act1_labels.append(int(row[2]))

            cnt = cnt +1

        c4 = 0
        c5 = 0
        c7 = 0
        c23 = 0
        for entry in anger:
            au_list = itemfreq(entry)

            for aus in au_list:
                if aus[0] == "a4":
                    c4 = c4 + 1
                elif aus[0] == "a5":
                    c5 = c5 + 1
                elif aus[0] == "a7":
                    c7 = c7 + 1
                elif aus[0] == "a23":
                    c23 = c23 + 1

        print "Anger: ","a4: ", c4, ", a5: ", c5, ", a7: ", c7, ", a23: ", c23, ", tot: ", an

        c9 = 0
        c15 = 0
        c16 = 0
        for entry in disgust:
            au_list = itemfreq(entry)

            for aus in au_list:
                if aus[0] == "a9":
                    c9 = c9 + 1
                elif aus[0] == "a15":
                    c15 = c15 + 1
                elif aus[0] == "a16":
                    c16 = c16 + 1

        print "Disgust: ", "a9: ", c9, ", a15: ", c15, ", a16: ", c16, ", tot: ", di

        c1 = 0
        c2 = 0
        c4 = 0
        c7 = 0
        c20 = 0
        c26 = 0
        for entry in fear:
            au_list = itemfreq(entry)

            for aus in au_list:
                if aus[0] == "a1":
                    c1 = c1 + 1
                elif aus[0] == "a2":
                    c2 = c2 + 1
                elif aus[0] == "a7":
                    c7 = c7 + 1
                elif aus[0] == "a20":
                    c20 = c20 + 1
                elif aus[0] == "a26":
                    c26 = c26 + 1
        print "Fear: ", "a1: ", c1, ", a2: ", c2, ", a7: ", c7, ", a20: ", c20, ", a26: ", c26, ", tot: ", fe

        c6 = 0
        c12 = 0
        for entry in happy:
            au_list = itemfreq(entry)

            for aus in au_list:
                if aus[0] == "a6":
                    c6 = c6 + 1
                elif aus[0] == "a12":
                    c12 = c12 + 1
        print "Happy: ", "a6: ", c6, ", a12: ", c12, ", tot: ", ha

        c1 = 0
        c4 = 0
        c15 = 0
        for entry in sad:
            au_list = itemfreq(entry)

            for aus in au_list:
                if aus[0] == "a4":
                    c4 = c4 + 1
                elif aus[0] == "a1":
                    c1 = c1 + 1
                elif aus[0] == "a15":
                    c15 = c15 + 1
        print "Sad: ", "a1: ", c1, "a4: ", c4, ", a15: ", c15, ", tot: ", sa

        c1 = 0
        c2 = 0
        c5 = 0
        c26 = 0
        for entry in surprise:
            au_list = itemfreq(entry)

            for aus in au_list:
                if aus[0] == "a1":
                    c1 = c1 + 1
                elif aus[0] == "a2":
                    c2 = c2 + 1
                elif aus[0] == "a5":
                    c5 = c5 + 1
                elif aus[0] == "a26":
                    c26 = c26 + 1
        print "Surprise: ",  "a1: ", c1, ", a2: ", c2, ", a5: ", c5, ", a26: ", c26, ", tot: ", su

        print txt_files[idx]

        out = open(txt_files[idx], "w")

        print>> out, "All faces"
        cm1 = confusion_matrix(all_faces_act_labels, all_faces_pred_labels)
        ll1 = assign_fes.list_fes(all_faces_pred_labels)
        al1 =  assign_fes.list_fes(all_faces_act_labels)
        print>> out, "Pred: ", ll1
        print>> out, "Act: ", al1
        print>> out, "###############################################"
        print>> out, cm1
        print>> out

        print>> out, "Face1"
        cm2 = confusion_matrix(act1_labels, pred1_labels)
        ll2 = assign_fes.list_fes(pred1_labels)
        al2 = assign_fes.list_fes(act1_labels)
        print>> out, "Pred: ", ll2
        print>> out, "Act: ", al2
        print>> out, "###############################################"
        print>> out, cm2
        print>> out

        print>> out, "Face2"
        cm3 = confusion_matrix(act2_labels, pred2_labels)
        ll3 = assign_fes.list_fes(pred2_labels)
        al3 = assign_fes.list_fes(act2_labels)
        print>> out, "Pred: ", ll3
        print>> out, "Act: ", al3
        print>> out, "###############################################"
        print>> out, cm3
        print>> out

        out.close()

        print csv_files[idx]
        print time.time() -start_time
        print
        idx = idx + 1
