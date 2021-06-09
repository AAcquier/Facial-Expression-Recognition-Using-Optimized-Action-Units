
import numpy as np

def get_FE(aus):

    # "a0" == dummy value
    anger = ["a0", "a4", "a5", "a7", "a23"]
    disgust = ["a0", "a9", "a15", "a16"]
    fear = ["a0", "a1", "a2", "a4", "a20", "a26"]
    happy = ["a0", "a6", "a12"]
    sad = ["a0", "a1", "a4", "a15"]                    
    surprise = ["a0", "a1", "a2", "a5", "a26"]      
      
    # if all(x in aus for x in anger):
    #     fe = 1
    if all(x in aus for x in disgust):
        fe = 2
    elif all(x in aus for x in fear):
        fe = 3
    elif all(x in aus for x in happy):
        fe = 4
    elif all(x in aus for x in sad):
        fe = 5
    # elif all(x in aus for x in surprise):
    #     fe = 6
    else:
        fe = 0

    return fe


def list_fes(labels):

    fe_list = []

    if 0 in labels:
        fe_list.append(0)
    if 1 in labels:
        fe_list.append(1)
    if 2 in labels:
        fe_list.append(2)
    if 3 in labels:
        fe_list.append(3)
    if 4 in labels:
        fe_list.append(4)
    if 5 in labels:
        fe_list.append(5)
    if 6 in labels:
        fe_list.append(6)


    return fe_list


def missing_aus(fe, res):

    anger = ["a0", "a4", "a5", "a7", "a23"]
    disgust = ["a0", "a9", "a15", "a16"]
    fear = ["a0", "a1", "a2", "a4", "a20", "a26"]
    happy = ["a0", "a6", "a12"]
    sad = ["a0", "a1", "a4", "a15"]
    surprise = ["a0", "a1", "a2", "a5", "a26"]

    if fe == 1:
        missing = np.setdiff1d(anger, res)
    elif fe == 2:
        missing = np.setdiff1d(disgust, res)
    elif fe == 3:
        missing = np.setdiff1d(fear, res)
    elif fe == 4:
        missing = np.setdiff1d(happy, res)
    elif fe == 5:
        missing = np.setdiff1d(sad, res)
    elif fe == 6:
        missing = np.setdiff1d(surprise, res)

    return missing
