
import numpy as np
import math
import cv2
from matplotlib.path import Path
from scipy.spatial import ConvexHull
from scipy.ndimage import rotate
import pymesh
import register


def auto_canny(image, sigma=0.33):
    # Automatically caclulate the upper and lower thresholds for canny edge filter, see:
    # https://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/

    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged

def mean_intensity_gradient(image):
    # Use of the Sobel filter for mean intensity gradient calculation, see
    # https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_gradients/py_gradients.html

    #Clean noise
    img = cv2.GaussianBlur(image, (3, 3), 0)
    sobel = cv2.Sobel(img,cv2.CV_64F, 1, 1, ksize=3)
    mean_int = np.mean(sobel)
    return mean_int

def rot(image, xy, angle):
    #https://stackoverflow.com/questions/46657423/rotated-image-coordinates-after-scipy-ndimage-interpolation-rotate
    im_rot = rotate(image, angle, reshape = False)              #rotates image
    org_center = (np.array(image.shape[:2][::-1]) - 1) / 2.
    rot_center = (np.array(im_rot.shape[:2][::-1]) - 1) / 2.
    new_pts = np.empty([4,2], dtype=np.uint32)
    idx = 0
    #Calculate the new coordinate in the rotated picture
    for co in xy:
        org = co - org_center
        new = np.array([org[0] * np.cos(angle) + org[1] * np.sin(angle),-org[0] * np.sin(angle) + org[1] * np.cos(angle)])
        new_co = new + rot_center
        new_pts[idx] = [new_co[0], new_co[1]]
        idx =idx+1

    #Insure that the box is rectangle
    if new_pts[0][0] != new_pts[3][0]:
        new_pts[3][0] = new_pts[0][0]

    if new_pts[0][1] != new_pts[1][1]:
        new_pts[1][1] = new_pts[0][1]

    if new_pts[1][0] != new_pts[2][0]:
        new_pts[2][0] = new_pts[1][0]

    if new_pts[2][1] != new_pts[3][1]:
        new_pts[3][1] = new_pts[2][1]

    #Extract the pixels of the region of interest
    roi = im_rot[new_pts[0][1]:new_pts[0][1]+(new_pts[2][1]-new_pts[0][1]), new_pts[0][0]:new_pts[0][0]+(new_pts[2][0]-new_pts[0][0])]

    return roi

def gauss_mean_curv(path_points, undistorted, min_depth):

    # Create an array to store the coordinates in the real world and gets those coordinnates
    depth_tuple_list = []

    for d in path_points:
        depth_tuple = register.getPointXYZ(undistorted, d[0], d[1])

        if np.array(depth_tuple).shape == (3, 1):
            for i in range(len(depth_tuple)):
                depth_tuple[i] = depth_tuple[i][0]

        check = 0

        for x in depth_tuple:
            if np.isnan(x):
                check = 1

        if check == 0:
            depth_tuple = [d for d in depth_tuple]
            depth_tuple[2] -= min_depth
            depth_tuple_list.append(depth_tuple)

    tri = ConvexHull(np.array(depth_tuple_list, dtype=np.float32),  qhull_options= "QbB")  # Compute the convex hull of the shape
    p1_mesh = pymesh.form_mesh(np.array(depth_tuple_list, dtype=np.float32), tri.simplices)  # Form the mesh
    p1_mesh, info = pymesh.remove_degenerated_triangles(p1_mesh)  # Remove degenerate triangle for accurate

    # Generates and gets the the Gaussian and mean curvatures
    p1_mesh.add_attribute("vertex_gaussian_curvature")
    p1_mesh.add_attribute("vertex_mean_curvature")
    gauss = p1_mesh.get_attribute("vertex_gaussian_curvature")
    mean = p1_mesh.get_attribute("vertex_mean_curvature")

    curv = np.array([gauss, mean])
    return curv

#Calculate the max and the min principal curvature based on the roots
def princ_curv(K, H):

    min = np.zeros(len(K))
    max = np.zeros(len(K))
    for i in range(len(K)):
        root = math.sqrt(abs(H[i]**2 - K[i]))
        min_val = H[i] - root
        min[i] = min_val
        max_val = H[i] + root
        max[i] = max_val

    p_curv = np.array([np.mean(min), np.mean(max)])
    return p_curv

def unionise(arr1, arr2):
    arr1_shape = arr1.shape
    arr2_shape = arr2.shape

    size1 = 0
    size2 = 0

    for i in range(len(arr1_shape)):

        if i == 0:
            size1 = arr1_shape[0]
            size2 = arr2_shape[0]
        else:
            size1 = size1 * arr1_shape[i]
            size2 = size2 * arr2_shape[i]

    if size1 > size2:
        res = np.resize(arr2, arr1_shape)
        union = np.concatenate((arr1, res))
    else:
        res = np.resize(arr1, arr2_shape)
        union = np.concatenate((arr2, res))

    return union


def filters(shape, color, undistorted, min_depth):

    # Store coordinates of kpts in np array
    kptsVec = np.empty([44, 2], dtype=int)
    for p in range(44):
        kptsVec[p][0] = shape.part(p).x
        kptsVec[p][1] = shape.part(p).y

    #All coordinates updated to the self generate kpts model 24-01-2019
    #This set the box p1
    x11 = kptsVec[11][0]
    y11 = kptsVec[11][1]
    x19 = kptsVec[19][0]
    y19 = kptsVec[19][1]
    p1dist = int(math.sqrt(((x11 - x19) ** 2) + ((y19 - y11) ** 2)))  # Distance points between 10 and 19
    rad1 = 30 * math.pi / 180
    rad2 = 60 * math.pi / 180
    x18 = kptsVec[18][0]
    y18 = kptsVec[18][1] - p1dist * 0.4
    p1x_topR = x18 + ((4 * p1dist / 5) * math.cos(rad1))
    p1y_topR = y18 + ((4 * p1dist / 5) * math.sin(rad1))
    p1x_botL = x18 - ((4 * p1dist / 3) * math.cos(rad2))
    p1y_botL = y18 + ((4 * p1dist / 3) * math.sin(rad2))
    p1bot_right = math.sqrt(((4 * p1dist / 3) ** 2) + ((4 * p1dist / 5) ** 2))
    p1_pts = np.array([[x18, y18], [p1x_topR, p1y_topR], [ x18, y18 + p1bot_right], [p1x_botL, p1y_botL]], np.int32)

    #Calculate the mean intensity gradient for p1
    p1_pix_val = rot(color, p1_pts, rad1)
    p1_int = mean_intensity_gradient(p1_pix_val)

    #To find the list of pixels in the bounded area for the different curvatures for p1
    p1_path = Path(p1_pts)
    x, y = np.mgrid[:color.shape[1], :color.shape[0]]      #Create a grid for the whole image
    points = np.vstack((x.ravel(), y.ravel())).T       # list o all the pixels in the image
    p1_mask = p1_path.contains_points(points)             # extract the points where the mask is located
    p1_path_points = points[np.where(p1_mask)]            # extract the pixels coordinates of the mask
    p1_gmc = gauss_mean_curv(p1_path_points, undistorted, min_depth)


    #This set the box p2
    x14 = kptsVec[14][0]
    y14 = kptsVec[14][1]
    x21 = kptsVec[21][0]
    y21 = kptsVec[21][1]
    p2dist = int(math.sqrt(((x21 - x14) ** 2) + ((y21 - y14) ** 2)))  # Distance points between 15 and 21
    x20 = kptsVec[20][0]
    y20 = kptsVec[20][1] - p2dist*0.4
    p2x_topL = x20 - ((4 * p2dist / 5) * math.cos(rad1))
    p2y_topL = y20 + ((4 * p2dist / 5) * math.sin(rad1))
    p2x_botR = x20 + ((4 * p2dist / 3) * math.cos(rad2))
    p2y_botR = y20 + ((4 * p2dist / 3) * math.sin(rad2))
    p2bot_left = math.sqrt(((4 * p2dist / 3) ** 2) + ((4 * p2dist / 5) ** 2))
    p2_pts = np.array([[p2x_topL, p2y_topL], [x20, y20], [p2x_botR, p2y_botR], [x20, y20 + p2bot_left]], np.int32)

    # Calculate the mean intensity gradient for p2
    p2_pix_val = rot(color, p2_pts, -rad1)
    p2_int = mean_intensity_gradient(p2_pix_val)
    p1p2_int = (p1_int + p2_int)/2

    # To find the list of pixels in the bounded area for the different curvatures for p2
    p2_path = Path(p2_pts)
    p2_mask = p2_path.contains_points(points)  # extract the points where the mask is located
    p2_path_points = points[np.where(p2_mask)]  # extract the pixels coordinates of the mask

    # Calculate the Gaussian and mean curvatures for p2
    p2_gmc = gauss_mean_curv(p2_path_points, undistorted, min_depth)
    p1p2_gc = (np.mean(abs(p1_gmc[0])) + np.mean(abs(p2_gmc[0])))/2
    p1p2_mc = (np.mean(abs(p1_gmc[1])) + np.mean(abs(p2_gmc[1])))/2


    #This set the box p3
    x1 = kptsVec[1][0]
    y1 = kptsVec[1][1]
    x34 = kptsVec[34][0]
    y34 = kptsVec[34][1]
    p3dist = x34 - x1
    p3y_topL = y1 - p3dist / 3
    p3y_topR = y34 - p3dist / 3
    p3_pts = np.array([[x1, p3y_topL], [x34, p3y_topR], [x34, y34], [x1, y1]], np.int32)
    p3_pix_val = color[p3_pts[0][1]:p3_pts[0][1]+(p3_pts[3][1]-p3_pts[0][1]), p3_pts[0][0]:p3_pts[0][0]+(p3_pts[1][0]-p3_pts[0][0])]
    p3_canny = auto_canny(p3_pix_val)
    p3_out = float(np.count_nonzero(p3_canny == 255)) /float(p3_canny.shape[0]*p3_canny.shape[1])*100 #M22


    #This set box p4
    x12 = kptsVec[12][0]
    y12 = kptsVec[12][1]
    x23 = kptsVec[23][0]
    y23 = kptsVec[23][1]
    p4dist = x23 - x12
    p4_pts = np.array([[x12, y12 - p4dist / 2], [x23, y23 - p4dist / 2], [x23, y23 + p4dist / 2], [x12, y12 + p4dist / 2]],np.int32)
    p4_pix_val = color[p4_pts[0][1]:p4_pts[0][1]+(p4_pts[3][1]-p4_pts[0][1]), p4_pts[0][0]:p4_pts[0][0]+(p4_pts[1][0]-p4_pts[0][0])]
    p4_canny = auto_canny(p4_pix_val)
    p4_out = float(np.count_nonzero(p4_canny == 255)) / float(p4_canny.shape[0] * p4_canny.shape[1])*100 #M1_23


    # This set up box p5
    x8 = kptsVec[8][0]
    y8 = kptsVec[8][1]
    x17 = kptsVec[17][0]
    y17 = kptsVec[17][1]
    p5dist = x17 - x8
    x10 = kptsVec[10][0]
    y10 = kptsVec[10][1]
    rad3 = 15 * math.pi / 180
    rad4 = 105 * math.pi / 180
    red_p5dist = (2 * p5dist / 3) / 2
    red_p5dist2 = 3 * (math.sqrt((x8 - x10) ** 2 + (y11 - y8) ** 2)) / 4
    p5x_topL = x12 - red_p5dist * math.cos(rad3)
    p5y_topL = y12 - red_p5dist * math.sin(rad3)
    p5x_topR = x12 + red_p5dist * math.cos(rad3)
    p5y_topR = y12 + red_p5dist * math.sin(rad3)
    p5x_botL = p5x_topL + red_p5dist2 * math.cos(rad4)
    p5y_botL = p5y_topL + red_p5dist2 * math.sin(rad4)
    p5x_botR = p5x_topR + red_p5dist2 * math.cos(rad4)
    p5y_botR = p5y_topR + red_p5dist2 * math.sin(rad4)
    p5_pts = np.array([[p5x_topL, p5y_topL], [p5x_topR, p5y_topR], [p5x_botR, p5y_botR], [x10, y10], [p5x_botL, p5y_botL]],np.int32)

    # To find the list of pixels in the bounded area for the different curvatures for p5
    p5_path = Path(p5_pts)
    p5_mask = p5_path.contains_points(points)  # extract the points where the mask is located
    p5_path_points = points[np.where(p5_mask)]  # extract the pixels coordinates of the mask
    p5_gmc = gauss_mean_curv(p5_path_points, undistorted, min_depth)
    p5_pc = princ_curv(p5_gmc[0], p5_gmc[1])

    # This set up box p6
    p6dist = x17 - x8
    x15 = kptsVec[15][0]
    y15 = kptsVec[15][1]
    red_p6dist = (2 * p6dist / 3) / 2
    red_p6dist2 = 3 * (math.sqrt((x17 - x15) ** 2 + (y15 - y17) ** 2)) / 4
    p6x_topL = x17 + red_p6dist * math.cos(rad3)
    p6y_topL = y17 + red_p6dist * math.sin(rad3)
    p6x_topR = x17 - red_p6dist * math.cos(rad3)
    p6y_topR = y17 - red_p6dist * math.sin(rad3)
    p6x_botL = p6x_topL - red_p6dist2 * math.cos(rad4)
    p6y_botL = p6y_topL + red_p6dist2 * math.sin(rad4)
    p6x_botR = p6x_topR - red_p6dist2 * math.cos(rad4)
    p6y_botR = p6y_topR + red_p6dist2 * math.sin(rad4)
    p6_pts = np.array([[p6x_topL, p6y_topL], [p6x_topR, p6y_topR], [p6x_botR, p6y_botR], [x15, y15], [p6x_botL, p6y_botL]],np.int32)

    # To find the list of pixels in the bounded area for the different curvatures for p6
    p6_path = Path(p6_pts)
    p6_mask = p6_path.contains_points(points)  # extract the points where the mask is located
    p6_path_points = points[np.where(p6_mask)]  # extract the pixels coordinates of the mask

    # Calculate the Gaussian and mean curvatures for p6
    p6_gmc = gauss_mean_curv(p6_path_points, undistorted, min_depth)
    p6_pc = princ_curv(p6_gmc[0],  p6_gmc[1])

    #Calculate the common output of boxes p5 and p6
    p5p6_gc = (np.mean(abs(p5_gmc[0])) + np.mean(abs(p6_gmc[0])))/2#M2_23
    p5p6_mc = (np.mean(abs(p5_gmc[1])) + np.mean(abs(p6_gmc[1])))/2#M3_23
    p5p6_pc_max = (p5_pc[1] + p6_pc[1])/2#M4_23


    # This set up box p7
    x9 = kptsVec[9][0]
    y9 = kptsVec[9][1]
    p7dist = x17 - x8
    p7y_topR = y8 + p7dist / 5
    p7x_ext = x8 - p7dist
    p7_pts = np.array([[x18, y18], [x10, y10], [x9, y9], [x8, p7y_topR], [p7x_ext, p7y_topR]], np.int32)

    # To find the list of pixels in the bounded area for the different curvatures for p7
    p7_path = Path(p7_pts)
    p7_mask = p7_path.contains_points(points)  # extract the points where the mask is located
    p7_path_points = points[np.where(p7_mask)]  # extract the pixels coordinates of the mask
    p7_gmc = gauss_mean_curv(p7_path_points, undistorted, min_depth)
    p7_pc = princ_curv(p7_gmc[0], p7_gmc[1])

    # This set up box p8
    x16 = kptsVec[16][0]
    y16 = kptsVec[16][1]
    p8dist = x17 - x8
    p8y_topR = y17 + p8dist / 5
    p8x_ext = x17 + p8dist
    p8_pts = np.array([[x20, y20], [x15, y15], [x16, y16], [x17, p8y_topR], [p8x_ext, p8y_topR]], np.int32)

    # To find the list of pixels in the bounded area for the different curvatures for p8
    p8_path = Path(p8_pts)
    p8_mask = p8_path.contains_points(points)  # extract the points where the mask is located
    p8_path_points = points[np.where(p8_mask)]  # extract the pixels coordinates of the mask

    # Calculate the Gaussian and mean curvatures for p8
    p8_gmc = gauss_mean_curv(p8_path_points, undistorted, min_depth)
    p8_pc = princ_curv(p8_gmc[0], p8_gmc[1])

    # Calculate the common output of boxes p7 and p8
    p7p8_gc = (np.mean(abs(p7_gmc[0])) + np.mean(abs(p8_gmc[0])))/2 #M5_23
    p7p8_mc = (np.mean(abs(p7_gmc[1])) + np.mean(abs(p8_gmc[1])))/2 #M6_23
    p7p8_pc_min = (p7_pc[0] + p8_pc[0])/2#M7_23
    p7p8_pc_max = (p7_pc[1] + p8_pc[1])/2#M823

    # Gather the outputs
    filters_result = [p1p2_int, p1p2_gc, p1p2_mc, p3_out, p4_out, p5p6_gc, p5p6_mc, p5p6_pc_max, p7p8_gc, p7p8_mc, p7p8_pc_min, p7p8_pc_max]

    return filters_result
