import numpy as np
import cv2 as cv
import time
import glob

def Cam_index_test():
    #### input camera index #####
    index = 4
    #############################

    cap1 = cv.VideoCapture(index)
    width = cap1.get(cv.CAP_PROP_FRAME_WIDTH)
    height = cap1.get(cv.CAP_PROP_FRAME_HEIGHT)
    print("재생할 파일 넓이, 높이 : %d, %d"%(width, height))

    fourcc = cv.VideoWriter_fourcc(*'DIVX')
    out = cv.VideoWriter('index '+str(index)+' camera output.avi', fourcc, 15.0, (int(width), int(height)))
    cnt = 0
    while(cap1.isOpened()):
        ret1, frame1 = cap1.read()    # Read 결과와 frame
        cnt+=1
        if(ret1 == False) : 
            break;   
        print(cnt)
        #cv.imshow('frame_color',frame1)
        out.write(frame1)
        if(cnt == 100):
            break
        if cv.waitKey(1) == ord('q'):
            
            break
     
    cap1.release()    
    out.release()   



def Capture_and_Save():
    cap1 = cv.VideoCapture(1)
    
    cnt =1
    while(cap1.isOpened()):
        ret1, frame1 = cap1.read()    # Read 결과와 frame
        
        if(ret1) :   
            cv.imshow('frame_color',frame1)
            
            if cv.waitKey(1) == ord('s'):
                
                cv.imwrite('./data2/chess'+str(cnt) +'.jpg',frame1)
                cnt+=1
            
        if cv.waitKey(1) == ord('q'):
            break
     
    cap1.release()       


def Make_Calibration_params():
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((8*6,3), np.float32)
    objp[:,:2] = np.mgrid[0:6,0:8].T.reshape(-1,2)
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    images = glob.glob('./data2/*.jpg')
    for fname in images:
        
        img = cv.imread(fname)
        gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
       
        
        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, (6,8),None)
        # If found, add object points, image points (after refining them)
        print(ret)
        if ret == True:
            
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners2)
            # Draw and display the corners
            img = cv.drawChessboardCorners(img, (6,8), corners2,ret)
            cv.imshow('img',img)
            #cv.imwrite('img',img)
            cv.waitKey(1000)
    cv.destroyAllWindows()  
    
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
    # cap1 = cv.VideoCapture(1)
    # ret1, img = cap1.read()    # Read 결과와 frame
    
    np.savez('calibration_parameters.npz',ret=ret, mtx=mtx, dist=dist)
    print("Calibration_done")
    
    ## testing real time calibration images ##
    # cap1 = cv.VideoCapture(1)
    # ret1, img = cap1.read()    # Read 결과와 frame
    
def Testing_calibration_imgaes():    
    calib_parms = np.load('calibration_parameters.npz')
    mtx = calib_parms['mtx']
    dist = calib_parms['dist']
    img = cv.imread('./data2/chess1.jpg')
    h,  w = img.shape[:2]
    
    newcameramtx, roi=cv.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
    print(h,w)
    ## testing saved images ##
    for i in range(1,5):
        img = cv.imread('./data2/chess'+str(i)+'.jpg')
        dst = cv.undistort(img, mtx, dist, None, newcameramtx)
        # print(mtx)
        # print(dist)
        # print(newcameramtx)
        x,y,w,h = roi
        dst = dst[y:y+h, x:x+w]
        cv.imwrite('./data_after_calib/after_calib_result_chess'+str(i) + '.png',dst)
        print(dst.shape)
    print("Images_calibration_done")
    
    
def Testing_calibration_video():
    calib_parms = np.load('calibration_parameters.npz')
    mtx = calib_parms['mtx']
    dist = calib_parms['dist']
    img = cv.imread('./data2/chess1.jpg')
    h,  w = img.shape[:2]
    newcameramtx, roi=cv.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
    
    #### input camera index #####
    index = 0
    #############################

    cap1 = cv.VideoCapture(index)
    width = cap1.get(cv.CAP_PROP_FRAME_WIDTH)
    height = cap1.get(cv.CAP_PROP_FRAME_HEIGHT)
    print("재생할 파일 넓이, 높이 : %d, %d"%(width, height))

    fourcc = cv.VideoWriter_fourcc(*'DIVX')
    out = cv.VideoWriter('calibation_video_output.avi', fourcc, 15.0, (int(width), int(height)))
    cnt = 0
    while(cap1.isOpened()):
        ret1, frame1 = cap1.read()    # Read 결과와 frame
        cnt+=1
        if(ret1 == False) : 
            break;     
        print(frame1.shape)
        dst = cv.undistort(frame1, mtx, dist, None, newcameramtx)
        x,y,w,h = roi
        dst = dst[y:y+h, x:x+w]
        
        #dst = cv.resize(dst, dsize=(640, 480), interpolation=cv.INTER_LINEAR)
        print("after",dst.shape)
        #cv.imshow('frame_color',dst)
        out.write(dst)
        if(cnt == 100):
            break
        if cv.waitKey(1) == ord('q'):
            
            break
     
    cap1.release()    
    out.release()   
    
#Capture_and_Save()
#Make_Calibration_params()
#Cam_index_test()
#Multi_Cam_test()
Testing_calibration_imgaes()
#Testing_calibration_video()