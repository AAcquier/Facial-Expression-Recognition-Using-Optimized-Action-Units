import os
import cv2
import dlib
import filters
import numpy as np
import register as register
import featuresExtraction
from imutils import face_utils
from datetime import datetime

def get_neutral(pred):

    predictor = dlib.shape_predictor("trained models/" + "pred_full.dat")
    face_cascade = cv2.CascadeClassifier('trained models/haarcascade_frontalface_alt2.xml')
    face_detect = dlib.get_frontal_face_detector()

    check = 0
    cnt = 0
    imgs = sorted(os.listdir("/media/alex/VERBATIM HD/neutral faces mathieu/colour/"))
    dm = sorted(os.listdir("/media/alex/VERBATIM HD/neutral faces mathieu/depth/"))
    all_im_faces = []
    all_img_faces_filters = []
    all_img_faces_features = []
    TS = datetime.now()
    init = int(TS.strftime("%s"))
    for i in range(len(imgs)):
        print i

        img = cv2.imread(os.path.join("/media/alex/VERBATIM HD/neutral faces mathieu/colour/" + str(imgs[i])), cv2.IMREAD_UNCHANGED)
        depth = cv2.bilateralFilter(np.load(os.path.join("/media/alex/VERBATIM HD/neutral faces mathieu/depth/" + str(dm[i]))), 10, 20, 20)

        if int(imgs[i][:-4]) == int(dm[i][:-4]) and int(imgs[i][:-4]) > check:
            check = int(imgs[i][:-4])

            min_depth = depth[depth > 0].min()
            faces = face_cascade.detectMultiScale(img)

            reg = register.apply(depth)

            this_img_faces_filters = []
            this_img_faces_features = []

            if len(faces) > 0:

                those_faces = []

                for (x, y, w, h) in faces:
               
                    those_faces.append([x, y, w, h])
                    dets = []
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    dets.append(dlib.rectangle(x, y, x + w, y + h))  # convert from opencv rectangle to an a dlib

                    for k, d in enumerate(dets):
                        shape = predictor(img, d)
                        fil = filters.filters(shape, img, reg, min_depth)

                        this_img_faces_filters.append(fil)

                        features = featuresExtraction.featureExtraction(shape, reg)
                        this_img_faces_features.append(features)
                all_im_faces.append(those_faces)
            all_img_faces_filters.append(this_img_faces_filters)
            all_img_faces_features.append(this_img_faces_features)

    #This part averages the features
    added_features = np.zeros([len(all_img_faces_features[0]), len(all_img_faces_features[0][0])], dtype=float)
    cnt = 0

    for list in all_img_faces_features:
        for i in range(len(list)):

            added_features[i] += list[i]

    #This part averages the filters
    added_filters = np.zeros([len(all_img_faces_filters[0]), len(all_img_faces_filters[0][0])], dtype=float)

    for list in all_img_faces_filters:

        for i in range(len(list)):
            added_filters[i] += list[i]

    # This calculate the area where faces should be
    x_all = np.zeros([len(all_im_faces[0])], dtype=int)
    y_all = np.zeros([len(all_im_faces[0])], dtype=int)
    w_all = np.zeros([len(all_im_faces[0])], dtype=int)
    h_all = np.zeros([len(all_im_faces[0])], dtype=int)
    token = 0

    for this_im_faces in all_im_faces:

        if len(this_im_faces) == 1:
            face_cnt = 0
            if token != 1:
                x_all[0] = this_im_faces[0][0]
                y_all[0] = this_im_faces[0][1]
                w_all[0] = this_im_faces[0][2]
                h_all[0] = this_im_faces[0][3]
                token = 1
            else:
                x_all[0] += this_im_faces[0][0]
                y_all[0] += this_im_faces[0][1]
                w_all[0] += this_im_faces[0][2]
                h_all[0] += this_im_faces[0][3]

        elif len(this_im_faces) > 1:                    #if there is more than 1 face in the image
            face_cnt = 0
            if token != 1:
                for faces in this_im_faces:
                    x_all[face_cnt] = faces[0]
                    y_all[face_cnt] = faces[1]
                    w_all[face_cnt] = faces[2]
                    h_all[face_cnt] = faces[3]
                    face_cnt = face_cnt + 1
                token = 1
            else:
                for faces in this_im_faces:
                    x_all[face_cnt] += faces[0]
                    y_all[face_cnt] += faces[1]
                    w_all[face_cnt] += faces[2]
                    h_all[face_cnt] += faces[3]
                    face_cnt = face_cnt + 1

    x_av = x_all/len(all_im_faces)
    y_av = y_all/len(all_im_faces)
    w_av = w_all/len(all_im_faces)
    h_av = h_all/len(all_im_faces)

    face_ROI = np.zeros([len(x_av), 4], dtype=int)
    for i in range(len(x_av)):
        face_ROI[i][0] = x_av[i]
        face_ROI[i][1] = y_av[i]
        face_ROI[i][2] = w_av[i]
        face_ROI[i][3] = h_av[i]

    return face_ROI, added_filters/len(all_img_faces_filters),  added_features/len(all_img_faces_features)


