
import randomize_data
import getNeutralFeatures
import dlib
import cv2
import register
from imutils import face_utils
import numpy as np
import csv
import filters
import featuresExtraction
import time

path ="/media/alex/VERBATIM HD/FE 4 testing Am&Gw/"
files = randomize_data.shuffled_data(path)
pred = "pred_full.dat"

ROI_pts, fil_arr, kpt_arr = getNeutralFeatures.get_neutral(pred)

predictor = dlib.shape_predictor("trained models/" + pred)
face_detect = dlib.get_frontal_face_detector()
face_cascade = cv2.CascadeClassifier('trained models/haarcascade_frontalface_alt2.xml')
start_time = time.time()

with open('measurements_Am&Gw_time_test.csv', 'w') as meas_list:

    meas = csv.writer(meas_list, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for file in files:
        print file
        img = cv2.imread(path + file[0] + "/colour/" + file[1] + ".png")
        depth = cv2.bilateralFilter(np.load(path + file[0] + "/depth/" + file[1] + ".npy"), 10, 20, 20)

        min_depth = depth[depth > 0].min()
        rects = face_detect(img, 1)
        faces = face_cascade.detectMultiScale(img)
        reg = register.apply(depth)

        for (x, y, w, h) in faces:

            if x in range(int(ROI_pts[0][0] - (0.5 * ROI_pts[0][0])), int(ROI_pts[0][0] + (0.5 *  ROI_pts[0][0]))) and \
                    y in range(int(ROI_pts[0][1] - (0.5 * ROI_pts[0][1])), int(ROI_pts[0][1] + (0.5 *  ROI_pts[0][1]))) and \
                    w in range(int(ROI_pts[0][2] - (0.5 *  ROI_pts[0][2])), int(ROI_pts[0][2] + ( 0.5 * ROI_pts[0][2]))) and \
                    h in range(int(ROI_pts[0][3] - (0.5 * ROI_pts[0][3])), int(ROI_pts[0][3] + ( 0.5 * ROI_pts[0][3]))):

                dets1 = []
                dets1.append(dlib.rectangle(x, y, x + w, y + h))  # convert from opencv rectangle to an a dlib

                for k, d in enumerate(dets1):
                    shape = predictor(img, d)

                    fil = filters.filters(shape, img, reg, min_depth)
                    features = featuresExtraction.featureExtraction(shape, reg)
                    print "face1"
                    meas.writerow([file[0] + file[1], 1, file[2], ((fil[0] - fil_arr[0][0]) / fil_arr[0][0]), \
                    ((fil[1] - fil_arr[0][1]) / fil_arr[0][1]), ((fil[2] - fil_arr[0][2]) / fil_arr[0][2]), \
                    ((fil[3] - fil_arr[0][3]) / fil_arr[0][3]), ((fil[4] - fil_arr[0][4]) / fil_arr[0][4]), \
                    ((fil[5] - fil_arr[0][5]) / fil_arr[0][5]), ((fil[6] - fil_arr[0][6]) / fil_arr[0][6]), \
                    ((fil[7] - fil_arr[0][7]) / fil_arr[0][7]), ((fil[8] - fil_arr[0][8]) / fil_arr[0][8]), \
                    ((fil[9] - fil_arr[0][9]) / fil_arr[0][9]), ((fil[10] - fil_arr[0][10]) / fil_arr[0][10]), \
                    ((fil[11] - fil_arr[0][11]) / fil_arr[0][11]), ((features[0]-kpt_arr[0][0])/kpt_arr[0][0]), \
                    ((features[1] - kpt_arr[0][1]) / kpt_arr[0][1]), ((features[2]-kpt_arr[0][2])/kpt_arr[0][2]), \
                    ((features[3] - kpt_arr[0][3]) / kpt_arr[0][3]), ((features[4] - kpt_arr[0][4]) / kpt_arr[0][4]), \
                    ((features[5] - kpt_arr[0][5]) / kpt_arr[0][5]), ((features[6] - kpt_arr[0][6]) / kpt_arr[0][6]), \
                    ((features[7] - kpt_arr[0][7]) / kpt_arr[0][7]), ((features[8] - kpt_arr[0][8]) / kpt_arr[0][8]), \
                    ((features[9] - kpt_arr[0][9]) / kpt_arr[0][9]), ((features[10] - kpt_arr[0][10]) / kpt_arr[0][10]), \
                    ((features[11] - kpt_arr[0][11]) / kpt_arr[0][11]), ((features[12] - kpt_arr[0][12]) / kpt_arr[0][12]), \
                    ((features[13] - kpt_arr[0][13]) / kpt_arr[0][13]), ((features[14] - kpt_arr[0][14])), \
                    ((features[15] - kpt_arr[0][15]) / kpt_arr[0][15]), ((features[16] - kpt_arr[0][16])), \
                    ((features[17] - kpt_arr[0][17]) / kpt_arr[0][17]), ((features[18] - kpt_arr[0][18]) / kpt_arr[0][18]), \
                    ((features[19] - kpt_arr[0][19]) / kpt_arr[0][19]), ((features[20] - kpt_arr[0][20]) / kpt_arr[0][20]), \
                    ((features[21] - kpt_arr[0][21]) / kpt_arr[0][21]), ((features[22] - kpt_arr[0][22]) / kpt_arr[0][22]),
                    ((features[23] - kpt_arr[0][23]) / kpt_arr[0][23]), ((features[24] - kpt_arr[0][24]) / kpt_arr[0][24]), \
                    ((features[25] - kpt_arr[0][25]) / kpt_arr[0][25]), ((features[26] - kpt_arr[0][26]) / kpt_arr[0][26]), \
                    ((features[27] - kpt_arr[0][27]) / kpt_arr[0][27])])

            if x in range(int(ROI_pts[1][0] - (0.6 * ROI_pts[1][0])), int(ROI_pts[1][0] + (0.6 * ROI_pts[1][0]))) and \
                    y in range(int(ROI_pts[1][1] - (0.6 * ROI_pts[1][1])), int(ROI_pts[1][1] + (0.6 * ROI_pts[1][1]))) and \
                    w in range(int(ROI_pts[1][2] - (0.6 * ROI_pts[1][2])), int(ROI_pts[1][2] + (0.6 * ROI_pts[1][2]))) and \
                    h in range(int(ROI_pts[1][3] - (0.6 * ROI_pts[1][3])), int(ROI_pts[1][3] + (0.6 * ROI_pts[1][3]))):

                dets2 = []
                dets2.append(dlib.rectangle(x, y, x + w, y + h))  # convert from opencv rectangle to an a dlib

                for k, d in enumerate(dets2):
                    shape = predictor(img, d)

                    fil = filters.filters(shape, img, reg, min_depth)
                    features = featuresExtraction.featureExtraction(shape, reg)
                    print "face2"
                    meas.writerow([file[0] + file[1], 2, file[3], ((fil[0] - fil_arr[1][0]) / fil_arr[1][0]), \
                                   ((fil[1] - fil_arr[1][1]) / fil_arr[1][1]), ((fil[2] - fil_arr[1][2]) / fil_arr[1][2]), \
                                   ((fil[3] - fil_arr[1][3]) / fil_arr[1][3]), ((fil[4] - fil_arr[1][4]) / fil_arr[1][4]), \
                                   ((fil[5] - fil_arr[1][5]) / fil_arr[1][5]), ((fil[6] - fil_arr[1][6]) / fil_arr[1][6]), \
                                   ((fil[7] - fil_arr[1][7]) / fil_arr[1][7]), ((fil[8] - fil_arr[1][8]) / fil_arr[1][8]), \
                                   ((fil[9] - fil_arr[1][9]) / fil_arr[1][9]), ((fil[10] - fil_arr[1][10]) / fil_arr[1][10]), \
                                   ((fil[11] - fil_arr[1][11]) / fil_arr[1][11]), ((features[0] - kpt_arr[1][0]) / kpt_arr[1][0]), \
                                   ((features[1] - kpt_arr[1][1]) / kpt_arr[1][1]), ((features[2] - kpt_arr[1][2]) / kpt_arr[1][2]), \
                                   ((features[3] - kpt_arr[1][3]) / kpt_arr[1][3]), ((features[4] - kpt_arr[1][4]) / kpt_arr[1][4]), \
                                   ((features[5] - kpt_arr[1][5]) / kpt_arr[1][5]), ((features[6] - kpt_arr[1][6]) / kpt_arr[1][6]), \
                                   ((features[7] - kpt_arr[1][7]) / kpt_arr[1][7]), ((features[8] - kpt_arr[1][8]) / kpt_arr[1][8]), \
                                   ((features[9] - kpt_arr[1][9]) / kpt_arr[1][9]), ((features[10] - kpt_arr[1][10]) / kpt_arr[1][10]), \
                                   ((features[11] - kpt_arr[1][11]) / kpt_arr[1][11]),
                                   ((features[12] - kpt_arr[1][12]) / kpt_arr[1][12]), \
                                   ((features[13] - kpt_arr[1][13]) / kpt_arr[1][13]),
                                   ((features[14] - kpt_arr[1][14])), \
                                   ((features[15] - kpt_arr[1][15]) / kpt_arr[1][15]),
                                   ((features[16] - kpt_arr[1][16])), \
                                   ((features[17] - kpt_arr[1][17]) / kpt_arr[1][17]),
                                   ((features[18] - kpt_arr[1][18]) / kpt_arr[1][18]), \
                                   ((features[19] - kpt_arr[1][19]) / kpt_arr[1][19]),
                                   ((features[20] - kpt_arr[1][20]) / kpt_arr[1][20]), \
                                   ((features[21] - kpt_arr[1][21]) / kpt_arr[1][21]),
                                   ((features[22] - kpt_arr[1][22]) / kpt_arr[1][22]),
                                   ((features[23] - kpt_arr[1][23]) / kpt_arr[1][23]),
                                   ((features[24] - kpt_arr[1][24]) / kpt_arr[1][24]), \
                                   ((features[25] - kpt_arr[1][25]) / kpt_arr[1][25]),
                                   ((features[26] - kpt_arr[1][26]) / kpt_arr[1][26]), \
                                   ((features[27] - kpt_arr[1][27]) / kpt_arr[1][27])])
            

print "Am&Gw"
print("--- %s seconds ---" % (time.time() - start_time))
