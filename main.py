import serial
import time
import cv2
import numpy as np

def region_of_interest(image, vertices):
    mask = np.zeros_like(image) 
    if len(image.shape) > 2:
        channel_count = image.shape[2]
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


def process_image(image):
    imshape = image.shape
    # gray
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # binary
    binary = cv2.adaptiveThreshold(gray,127,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,-30)
    # canny
    edges = cv2.Canny(binary,20,100)

    
    # region of interest
    vertices = np.array([[(0 * imshape[1] / 20, 20 * imshape[0] / 20),
                          (0 * imshape[1] / 20, 9 * imshape[0] / 20),
                          (20 * imshape[1] / 20,9* imshape[0] / 20),
                          (20 * imshape[1] / 20,20 * imshape[0]/20)]], dtype=np.int32)
    # draw mask region
    cv2.circle(image,(int(0 * imshape[1]  / 20), int(20* imshape[0]/20)), 2,(0,0,255),0)
    cv2.circle(image,(int(0 * imshape[1]  / 20), int(9* imshape[0]/20)), 20,(0,0,255),0)
    cv2.circle(image,(int(20 * imshape[1]  / 20),int(9* imshape[0]/20)), 20,(0,0,255),0)
    cv2.circle(image,(int(20 * imshape[1]  / 20),int(20*imshape[0]/20)), 20,(0,0,255),0)
    
    masked_edges = region_of_interest(edges, vertices)
    
    lines = cv2.HoughLinesP(masked_edges, 1, np.pi / 180, threshold=50, minLineLength=30, maxLineGap=50)
    return lines
  
def move(lines,frame,triangle):
    # calculate lane angle
    laneAngle = np.deg2rad(90)
    nearestY = 0
    for line in lines: 
        x1, y1, x2, y2 = line[0]
        if y1 > nearestY or y2 > nearestY: # larger Y is lower on screen, nearer to the robot
            laneAngle = np.arctan2(y2-y1, x2-x1)
            nearestY = max(y1, y2)
        if laneAngle < 0:
            laneAngle += np.deg2rad(180)
        deltaX = (int)(100*np.cos(laneAngle))
        deltaY = (int)(100*np.sin(laneAngle))
        cv2.line(frame, (640//2,480), (640//2-deltaX,480-deltaY), color=(0,255,0), thickness=2) 

    print("lane angle",np.rad2deg(laneAngle))

    # move
    if triangle == 1:
        print("left triangle")
        ser.write('6\n'.encode())
    elif triangle == -1:
        print("right triangle")
        ser.write('-6\n'.encode())
    
    elif laneAngle <= np.deg2rad(30):
        print("5")
        ser.write('5\n'.encode())
    elif np.deg2rad(30) < laneAngle <= np.deg2rad(45):
        print("4")
        ser.write('4\n'.encode())
    elif np.deg2rad(45) < laneAngle <= np.deg2rad(60):
        print("3")
        ser.write('3\n'.encode())
    elif np.deg2rad(60) < laneAngle <= np.deg2rad(75):
        print("2")
        ser.write('2\n'.encode())
    elif np.deg2rad(75) < laneAngle <= np.deg2rad(90):
        print("1")
        ser.write('1\n'.encode())
    elif np.deg2rad(90) < laneAngle <= np.deg2rad(105):
        print("-1")
        ser.write('-1\n'.encode())
    elif np.deg2rad(105) < laneAngle <= np.deg2rad(120):
        print("-2")
        ser.write('-2\n'.encode())
    elif np.deg2rad(120) < laneAngle <= np.deg2rad(135):
        print("-3")
        ser.write('-3\n'.encode())
    elif np.deg2rad(135) < laneAngle <= np.deg2rad(157):
        print("-4")
        ser.write('-4\n'.encode())
    elif np.deg2rad(157) < laneAngle:
        print("-5")
        ser.write('-5\n'.encode())
    

          

def find_triangle(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,20,100)
    contours , hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
        if len(approx) == 3 and cv2.contourArea(contour) > 11000:
            cv2.drawContours(image, [approx], 0, (0, 0, 0), 5)           
            if(abs(approx[0][0][0]-approx[1][0][0]) < 20 and abs((approx[0][0][1]+approx[1][0][1])/2 - approx[2][0][1]) < 20):
                print("right triangle")
                triangle = -1
              

            elif(abs(approx[0][0][0]-approx[2][0][0]) < 20 and abs((approx[0][0][1]+approx[2][0][1])/2 - approx[1][0][1]) < 20):
                print("left triangle")
                triangle = 1
    return triangle
                
    


if __name__== '__main__':

    # Arduino
    COM_PORT = '/dev/ttyUSB0'
    BAUD_RATES = 57600
    ser = serial.Serial(COM_PORT, BAUD_RATES)
    time.sleep(2)
    
    # open camera
    cap = cv2.VideoCapture(0)
    if cap.isOpened(): 
        width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  
        print(f"Width: {width}")
        print(f"Height: {height}")
        
    
    ser.write(b'0')
    data_raw = ser.readline()  
    data = data_raw.decode()   
    print(data)
     
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error reading frame.")
            break
        # image process
        lines = process_image(frame)
        # find triangle
        triangle = find_triangle(frame)
        # move
        move(lines,frame,triangle)
            
        cv2.imshow("image", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()





    





